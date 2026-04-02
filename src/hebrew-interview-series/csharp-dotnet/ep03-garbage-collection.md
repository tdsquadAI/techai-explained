# שיעור 3: Garbage Collection ו-IDisposable — ניהול זיכרון ב-C#

**סדרת הכנה לראיונות הייטק | מסלול C# & .NET | TechAI Explained**

---

## מבוא

"C# מנהלת זיכרון אוטומטית" — אמת, אבל לא כל האמת.  
מפתחים שמבינים את ה-Garbage Collector ויודעים מתי להשתמש ב-`IDisposable` הם מפתחים שכותבים קוד עם **ביצועים טובים יותר** ולא מזליגים משאבים.  
בשיעור הזה נפרק את הנושא לעומק.

---

## מה הוא Garbage Collector?

ה-**Garbage Collector (GC)** הוא מנגנון ב-.NET שמנהל **זיכרון ה-Heap** באופן אוטומטי.  
הוא אחראי לשחרר אובייקטים שאין יותר reference אליהם.

```csharp
void SomeMethod()
{
    var obj = new MyClass(); // אובייקט נוצר ב-Heap
    obj.DoWork();
    // obj יוצא מה-scope — GC ישחרר את הזיכרון בזמן כלשהו
}
```

---

## הדורות של ה-GC (Generations)

ה-GC מחלק אובייקטים ל-3 **דורות (Generations)**:

### Generation 0 — צעירים
- אובייקטים שנוצרו לאחרונה
- נאספים הכי תכופות
- רוב האובייקטים "מתים" כאן

### Generation 1 — ביניים
- אובייקטים ששרדו Collection אחת
- מעבר בין Gen0 לGen2

### Generation 2 — ותיקים
- אובייקטים שחיים הרבה זמן
- נאספים לעתים רחוקות
- Long-lived objects: cache, singletons

```
Gen 0: [🆕 🆕 🆕 🆕 🆕] ← Collection תכופה
Gen 1: [📦 📦]
Gen 2: [🏛️ 🏛️] ← Collection נדירה
```

---

## Large Object Heap (LOH)

אובייקטים **מעל 85,000 בייטים** מוקצים ישירות ל-**Large Object Heap**:
- לא עוברים Compaction (מסיבות ביצועים)
- גורמים ל-**Heap Fragmentation**
- נאספים רק עם Gen2 Collection

```csharp
// ⚠️ יוקצה ב-LOH
var largeArray = new byte[100_000];

// ✅ טוב יותר — שימוש ב-ArrayPool
var buffer = ArrayPool<byte>.Shared.Rent(100_000);
try { /* ... */ }
finally { ArrayPool<byte>.Shared.Return(buffer); }
```

---

## IDisposable — לניהול משאבים לא-מנוהלים

ה-GC מנהל **זיכרון** בלבד. הוא **לא** מנהל:
- חיבורי DB
- File handles
- Network connections
- COM objects

לכן יש את הממשק `IDisposable`:

```csharp
public class DatabaseConnection : IDisposable
{
    private SqlConnection _connection;
    private bool _disposed = false;
    
    public DatabaseConnection(string connectionString)
    {
        _connection = new SqlConnection(connectionString);
        _connection.Open();
    }
    
    public void ExecuteQuery(string sql)
    {
        if (_disposed)
            throw new ObjectDisposedException(nameof(DatabaseConnection));
        // ...
    }
    
    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this); // מונע קריאה כפולה ל-Finalizer
    }
    
    protected virtual void Dispose(bool disposing)
    {
        if (!_disposed)
        {
            if (disposing)
            {
                _connection?.Dispose(); // שחרור managed resources
            }
            _disposed = true;
        }
    }
}

// שימוש עם using — Dispose נקרא אוטומטית
using var db = new DatabaseConnection("...");
db.ExecuteQuery("SELECT 1");
// כאן Dispose נקרא אוטומטית
```

---

## Finalizer — ה-Safety Net

`Finalizer` (ידוע גם כ-Destructor) הוא מנגנון גיבוי:

```csharp
public class ResourceHolder : IDisposable
{
    private IntPtr _nativeHandle;
    
    public ResourceHolder()
    {
        _nativeHandle = NativeLibrary.Allocate();
    }
    
    ~ResourceHolder() // Finalizer
    {
        // נקרא ע"י GC אם Dispose לא נקרא
        Dispose(false);
    }
    
    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this); // ביטול Finalizer — כבר שחררנו
    }
    
    protected virtual void Dispose(bool disposing)
    {
        if (_nativeHandle != IntPtr.Zero)
        {
            NativeLibrary.Free(_nativeHandle);
            _nativeHandle = IntPtr.Zero;
        }
    }
}
```

**⚠️ זכרו:** Finalizers מאטים את ה-GC. תמיד קוראים ל-`Dispose()` ידנית.

---

## using Statement ו-using Declaration

```csharp
// using statement (C# 1+)
using (var reader = new StreamReader("file.txt"))
{
    string content = reader.ReadToEnd();
}
// reader.Dispose() נקרא כאן

// using declaration (C# 8+) — קוד נקי יותר
using var reader = new StreamReader("file.txt");
string content = reader.ReadToEnd();
// reader.Dispose() נקרא בסוף ה-scope
```

---

## IAsyncDisposable — async cleanup

```csharp
public class AsyncResource : IAsyncDisposable
{
    private HttpClient _client = new HttpClient();
    
    public async ValueTask DisposeAsync()
    {
        await FlushAsync(); // עבודה אסינכרונית בעת סגירה
        _client.Dispose();
    }
    
    private async Task FlushAsync() { /* ... */ }
}

// שימוש
await using var resource = new AsyncResource();
```

---

## שאלות ראיון נפוצות

### שאלה 1: "מה ההבדל בין Dispose ל-Finalize?"
**תשובה נכונה:**
- `Dispose` — נקרא **ידנית** (או ע"י `using`), שחרור מיידי ומנוהל
- `Finalize` — נקרא ע"י **ה-GC** כ-safety net, איטי יותר, לא דטרמיניסטי

### שאלה 2: "מתי להשתמש ב-GC.Collect()?"
**תשובה נכונה:** כמעט אף פעם. ה-GC יודע מה הוא עושה. קריאה ידנית ל-`GC.Collect()` בדרך כלל פוגעת בביצועים. מקרה חריג: לאחר ביצוע פעולה גדולה שיצרה הרבה garbage.

### שאלה 3: "מה הם Memory Leaks ב-C#?"
**תשובה נכונה:** ב-C# memory leak קורה כשמחזיקים references לאובייקטים שלא צריך יותר:
- Event handlers שלא בוטלו (`+=` ללא `-=`)
- Static collections שגדלות ללא גבול
- Unmanaged resources ללא `Dispose`

---

## מלכודות נפוצות בראיון

❌ "C# לא יכולה לסבול memory leaks" — יכולה, בגלל references שנשמרים  
❌ "Dispose נקרא אוטומטית על ידי ה-GC" — רק Finalizer נקרא, לא Dispose  
❌ "GC.Collect() יעיל לביצועים" — בדרך כלל להיפך

---

## סיכום

| מונח | תפקיד |
|------|--------|
| GC | שחרור זיכרון Heap אוטומטי |
| Generation 0/1/2 | מנגנון אופטימיזציה של GC |
| IDisposable | שחרור משאבים לא-מנוהלים |
| using | הבטחת קריאה ל-Dispose |
| Finalizer | safety net לשחרור unmanaged |

---

*TechAI Explained | מסלול C# & .NET | שיעור 3 מתוך 10*
