# שיעור 2: async/await ו-Task — הבנה מעמיקה לראיון

**סדרת הכנה לראיונות הייטק | מסלול C# & .NET | TechAI Explained**

---

## מבוא

`async` ו-`await` הן אולי התכונות הנפוצות ביותר ב-C# המודרנית — ואחת הנושאים שהכי הרבה מועמדים מסבירים **לא נכון** בראיון.  
"async זה multi-threading" — שמעתם את זה? זו אחת הטעויות הנפוצות ביותר.  
בשיעור הזה נבין בדיוק מה קורה כשאנחנו כותבים `await`.

---

## הבעיה שאותה async/await פותרת

לפני `async/await`, קוד אסינכרוני נכתב עם callbacks, שגרם לתופעה המפורסמת "callback hell":

```csharp
// קוד סינכרוני — חוסם Thread
var data = File.ReadAllText("bigfile.txt"); // Thread ממתין!
Process(data);
```

כשה-Thread ממתין לקלט/פלט (I/O), הוא **חסום** — אינו יכול לשרת בקשות אחרות.  
`async/await` מאפשר ל-Thread להמשיך לעבוד בזמן שהממשק חוזר.

---

## async/await בפעולה

```csharp
// קוד אסינכרוני — Thread אינו חסום
public async Task<string> ReadFileAsync(string path)
{
    string data = await File.ReadAllTextAsync(path);
    return data.ToUpper();
}
```

מה קורה כאן?
1. הפונקציה מתחילה לרוץ על ה-Thread הנוכחי
2. כשהיא מגיעה ל-`await`, ה-Thread **שוחרר** ויכול לטפל בבקשות אחרות
3. כשהקריאה ל-I/O סיימה, הקוד שאחרי ה-`await` ממשיך — לא בהכרח על אותו Thread

---

## Task vs Task\<T\>

```csharp
// Task — מחזיר void (ללא ערך)
public async Task DoWorkAsync()
{
    await Task.Delay(1000);
    Console.WriteLine("Done!");
}

// Task<T> — מחזיר ערך
public async Task<int> GetCountAsync()
{
    await Task.Delay(1000);
    return 42;
}

// שימוש
int count = await GetCountAsync();
```

---

## async void — מתי וכמה לא להשתמש

```csharp
// ❌ BAD — Exception תחמוק!
public async void BadMethod()
{
    await Task.Delay(1000);
    throw new Exception("Lost exception!");
}

// ✅ GOOD — Exception ניתן לטיפול
public async Task GoodMethod()
{
    await Task.Delay(1000);
    throw new Exception("Caught exception!");
}
```

`async void` מיועד **רק** לאירועים (event handlers). בכל מקרה אחר — תמיד `async Task`.

---

## Deadlock — המלכודת הנפוצה ביותר

זהו אחד הנושאים הכי נשאלים בראיון:

```csharp
// ❌ Deadlock! — אל תעשו את זה ב-ASP.NET
public string GetResult()
{
    return GetResultAsync().Result; // חוסם ומחכה
}

public async Task<string> GetResultAsync()
{
    await Task.Delay(1000); // מנסה לחזור ל-SynchronizationContext
    return "Done";
}
```

**למה זה Deadlock?**  
ב-ASP.NET הישן וב-UI threads, יש `SynchronizationContext`.  
כש-`GetResult()` קורא ל-`.Result`, הוא חוסם את ה-Thread הנוכחי.  
`await` מנסה לחזור לאותו Thread (SynchronizationContext) — אבל הוא חסום.  
**תוצאה:** Deadlock.

**הפתרון הנכון:**
```csharp
// ✅ Option 1: async all the way
public async Task<string> GetResultAsync()
{
    return await GetResultInternalAsync();
}

// ✅ Option 2: ConfigureAwait(false) — ב-Libraries
public async Task<string> LibraryMethodAsync()
{
    await Task.Delay(1000).ConfigureAwait(false); // לא חוזר ל-SynchronizationContext
    return "Done";
}
```

---

## ValueTask — האופטימיזציה המתקדמת

```csharp
// Task — תמיד יוצר allocation ב-Heap
public async Task<int> GetCachedValue()
{
    if (_cache != null)
        return _cache; // עדיין יוצר Task object!
    
    return await FetchFromDb();
}

// ValueTask — ללא allocation כשיש ערך מיידי
public async ValueTask<int> GetCachedValueOptimized()
{
    if (_cache != null)
        return _cache; // ללא allocation!
    
    return await FetchFromDb();
}
```

---

## WhenAll ו-WhenAny

```csharp
// ריצה מקבילית של מספר tasks
var task1 = FetchUserAsync(1);
var task2 = FetchUserAsync(2);
var task3 = FetchUserAsync(3);

// המתנה לכולם
var users = await Task.WhenAll(task1, task2, task3);

// המתנה לראשון שמסיים
var firstResult = await Task.WhenAny(task1, task2, task3);
```

---

## CancellationToken — תמיד תעבירו אותו

```csharp
public async Task<string> FetchDataAsync(CancellationToken cancellationToken = default)
{
    using var client = new HttpClient();
    
    // העברת token לכל קריאה אסינכרונית
    var response = await client.GetAsync("https://api.example.com", cancellationToken);
    return await response.Content.ReadAsStringAsync(cancellationToken);
}

// ביטול לאחר 5 שניות
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(5));
var data = await FetchDataAsync(cts.Token);
```

---

## שאלות ראיון נפוצות

### שאלה 1: "האם async/await יוצר Threads חדשים?"
**תשובה נכונה:** לא בהכרח. `async/await` הוא מנגנון לניהול **המשכיות קוד** (continuation), לא ליצירת Threads. עבור I/O-bound operations, לא נוצר Thread חדש — ה-Thread הקיים שוחרר.

### שאלה 2: "מה ההבדל בין Task.Run לבין await?"
**תשובה נכונה:**
- `Task.Run` — מריץ קוד על Thread Pool Thread (לעבודה CPU-bound)
- `await` — ממתין לסיום Task, משחרר ה-Thread הנוכחי

### שאלה 3: "מתי להשתמש ב-ConfigureAwait(false)?"
**תשובה נכונה:** ב-libraries ו-backend code שאינם צריכים לחזור ל-UI thread — לשיפור ביצועים ומניעת deadlocks.

---

## מלכודות נפוצות בראיון

❌ "async זה multi-threading" — לא נכון. async הוא concurrency, לא parallelism.  
❌ "async void זה בסדר" — רק לאירועים!  
❌ ".Result ו-.Wait() הם בסדר" — גורמים לדדלוקים.

---

## סיכום

| מונח | הסבר |
|------|------|
| `async` | מסמן שהמתודה אסינכרונית |
| `await` | ממתין ל-Task, משחרר ה-Thread |
| `Task` | מייצג פעולה אסינכרונית |
| `CancellationToken` | מאפשר ביטול פעולות |
| Deadlock | חסימה הדדית — `.Result` + `SynchronizationContext` |

---

*TechAI Explained | מסלול C# & .NET | שיעור 2 מתוך 10*
