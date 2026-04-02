# שיעור 8: Threading ו-Concurrency — Thread, Task, CancellationToken

**סדרת הכנה לראיונות הייטק | מסלול C# & .NET | TechAI Explained**

---

## מבוא

ביצועים בקנה מידה גדול דורשים הבנה של concurrency.  
שאלות על Thread safety, race conditions ו-lock הן שאלות ראיון ברמה גבוהה שמפרידות בין מפתחים.

---

## Thread vs Task

```csharp
// Thread — ניהול ישיר (נדיר היום)
var thread = new Thread(() => {
    Console.WriteLine($"Thread ID: {Thread.CurrentThread.ManagedThreadId}");
});
thread.Start();
thread.Join(); // המתנה לסיום

// Task — ניהול על Thread Pool (מומלץ)
var task = Task.Run(() => {
    Console.WriteLine("Running on Thread Pool");
});
await task;
```

### למה Task עדיף?
- **Thread Pool:** שימוש חוזר ב-Threads קיימים
- **async/await:** תמיכה מלאה
- **Cancellation:** תמיכה ב-CancellationToken
- **Exception handling:** פשוט יותר

---

## Race Condition — הבאג הכי מסוכן

```csharp
// ❌ Race Condition!
private int _counter = 0;

public void IncrementFromMultipleThreads()
{
    Parallel.For(0, 1000, _ => {
        _counter++; // לא thread-safe!
        // Read + Increment + Write — שלושה צעדים לא אטומיים
    });
    Console.WriteLine(_counter); // לא יהיה 1000!
}
```

---

## lock — הפתרון הבסיסי

```csharp
private int _counter = 0;
private readonly object _lockObject = new object(); // dedicated lock object

public void SafeIncrement()
{
    Parallel.For(0, 1000, _ => {
        lock (_lockObject) // רק thread אחד בכל פעם
        {
            _counter++;
        }
    });
    Console.WriteLine(_counter); // 1000 ✅
}
```

---

## Interlocked — אטומי ומהיר

```csharp
private int _counter = 0;

public void AtomicIncrement()
{
    Parallel.For(0, 1000, _ => {
        Interlocked.Increment(ref _counter); // אטומי, ללא lock
    });
    Console.WriteLine(_counter); // 1000 ✅
}

// פעולות Interlocked
Interlocked.Add(ref _total, 10);
int old = Interlocked.Exchange(ref _value, 42);
int result = Interlocked.CompareExchange(ref _value, newValue, expectedValue);
```

---

## SemaphoreSlim — הגבלת concurrency

```csharp
private readonly SemaphoreSlim _semaphore = new SemaphoreSlim(3); // מקסימום 3 בו-זמנית

public async Task ProcessWithLimitAsync(IEnumerable<int> items)
{
    var tasks = items.Select(async item => {
        await _semaphore.WaitAsync();
        try
        {
            await ProcessItemAsync(item);
        }
        finally
        {
            _semaphore.Release();
        }
    });
    
    await Task.WhenAll(tasks);
}
```

---

## CancellationToken — ביטול מנוהל

```csharp
public async Task LongRunningOperationAsync(CancellationToken ct)
{
    for (int i = 0; i < 100; i++)
    {
        ct.ThrowIfCancellationRequested(); // בדיקה ידנית
        
        await Task.Delay(100, ct); // ביטול אוטומטי ב-Delay
        
        Console.WriteLine($"Step {i}");
    }
}

// שימוש עם timeout
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(5));

// שימוש עם ביטול ידני
using var cts = new CancellationTokenSource();
cts.Cancel(); // ביטול מיידי

// חיבור של שני tokens
using var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(ct1, ct2);
```

---

## Parallel.ForEach — עיבוד מקבילי

```csharp
var items = Enumerable.Range(1, 100).ToList();

// עיבוד מקבילי
Parallel.ForEach(items, new ParallelOptions { MaxDegreeOfParallelism = 4 },
    item => {
        ProcessItem(item);
    });

// async version — Channel או Parallel.ForEachAsync (.NET 6+)
await Parallel.ForEachAsync(items, async (item, ct) => {
    await ProcessItemAsync(item, ct);
});
```

---

## volatile — שמירה על ראיות שדות

```csharp
private volatile bool _isRunning = true;

public void Worker()
{
    while (_isRunning) // thread אחר יכול לשנות
    {
        DoWork();
    }
}

public void Stop()
{
    _isRunning = false; // guarantee — ייראה מיד לכל threads
}
```

---

## שאלות ראיון נפוצות

### שאלה 1: "מה הוא Race Condition?"
**תשובה נכונה:** מצב שבו תוצאת תוכנה תלויה בסדר הביצוע של threads. קורה כשמרובה threads ניגשים לנתון משותף ולפחות אחד כותב, ללא synchronization.

### שאלה 2: "מה ההבדל בין lock לבין SemaphoreSlim?"
**תשובה נכונה:** lock מאפשר thread אחד בלבד. SemaphoreSlim מאפשר **מספר מוגדר** של threads בו-זמנית. SemaphoreSlim תומך גם ב-async (`WaitAsync`).

### שאלה 3: "מה הוא Deadlock ואיך מונעים?"
**תשובה נכונה:** שני threads מחכים אחד לשני לנצח. מניעה: תמיד לנעול resources בסדר קבוע, שימוש ב-timeout, הימנעות מנעילה מקוננת.

---

## סיכום

| כלי | שימוש |
|-----|-------|
| `lock` | critical section בסיסי |
| `Interlocked` | פעולות אטומיות על primitives |
| `SemaphoreSlim` | הגבלת concurrency, async-friendly |
| `CancellationToken` | ביטול מנוהל |
| `volatile` | ראיה מיידית של שינויים |
| `Parallel.ForEach` | עיבוד מקבילי |

---

*TechAI Explained | מסלול C# & .NET | שיעור 8 מתוך 10*
