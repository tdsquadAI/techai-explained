# שיעור 7: Generics ו-Constraints — גמישות עם בטיחות סוגים

**סדרת הכנה לראיונות הייטק | מסלול C# & .NET | TechAI Explained**

---

## מבוא

Generics הם אחד הכלים החזקים ב-C# — מאפשרים כתיבת קוד **גמיש** שעובד עם טיפוסים שונים **בלי לוותר על Type Safety**.  
בראיון, הבנה של Generics, Constraints וCovariance/Contravariance מבדילה בין מפתחים.

---

## Generic Types בסיסיים

```csharp
// ❌ ללא Generics — מאבדים type safety
public class Stack
{
    private object[] _items = new object[100];
    private int _top = 0;
    
    public void Push(object item) => _items[_top++] = item;
    public object Pop() => _items[--_top]; // חייבים casting
}

// ✅ עם Generics — type safe!
public class Stack<T>
{
    private T[] _items = new T[100];
    private int _top = 0;
    
    public void Push(T item) => _items[_top++] = item;
    public T Pop() => _items[--_top]; // ללא casting
}

// שימוש
var intStack = new Stack<int>();
intStack.Push(42);
int value = intStack.Pop(); // int, לא object

var strStack = new Stack<string>();
strStack.Push("Hello");
// strStack.Push(42); ❌ — שגיאת compile!
```

---

## Generic Methods

```csharp
public class Utils
{
    // Generic method
    public static T Max<T>(T a, T b) where T : IComparable<T>
    {
        return a.CompareTo(b) > 0 ? a : b;
    }
    
    public static void Swap<T>(ref T a, ref T b)
    {
        T temp = a;
        a = b;
        b = temp;
    }
}

int max = Utils.Max(3, 7);       // 7
string bigger = Utils.Max("abc", "xyz"); // "xyz"
```

---

## Constraints — הגבלות על Generic Types

### where T : class — Reference Type בלבד
```csharp
public class Repository<T> where T : class
{
    public T? FindById(int id) => null; // T יכול להיות null
}
```

### where T : struct — Value Type בלבד
```csharp
public class ValueHolder<T> where T : struct
{
    private T _value;
    // T לא יכול להיות null
}
```

### where T : new() — חייב להיות constructor ריק
```csharp
public class Factory<T> where T : new()
{
    public T Create() => new T(); // אפשרי כי יש new()
}
```

### where T : BaseClass — חייב לירש מ-BaseClass
```csharp
public class AnimalShelter<T> where T : Animal
{
    public void Feed(T animal) => animal.Eat(); // בטוח!
}
```

### where T : IInterface — חייב לממש Interface
```csharp
public class Printer<T> where T : IPrintable
{
    public void Print(T item) => item.Print();
}
```

### Constraint מרובה
```csharp
public class Manager<T>
    where T : class, IDisposable, IComparable<T>, new()
{
    // T חייב להיות: class, IDisposable, IComparable, ועם new()
}
```

---

## Covariance ו-Contravariance

זהו הנושא המתקדם שמפתח בכיר צריך להבין:

### Covariance — out (יכול להשתמש בתת-סוג)

```csharp
// IEnumerable<T> is covariant — out T
IEnumerable<Dog> dogs = new List<Dog>();
IEnumerable<Animal> animals = dogs; // ✅ אפשרי!

// interface מוגדר כ:
// public interface IEnumerable<out T>
```

### Contravariance — in (יכול להשתמש בסוג-אב)

```csharp
// Action<T> is contravariant — in T
Action<Animal> feedAnimal = (animal) => Console.WriteLine("Feeding");
Action<Dog> feedDog = feedAnimal; // ✅ אפשרי!

// interface מוגדר כ:
// public delegate void Action<in T>(T obj)
```

### הגדרת Covariance/Contravariance עצמית

```csharp
// Covariant — רק מחזיר T (out)
public interface IReader<out T>
{
    T Read();
}

// Contravariant — רק מקבל T (in)
public interface IWriter<in T>
{
    void Write(T value);
}
```

---

## Generic Caching Pattern

```csharp
public class Cache<TKey, TValue>
    where TKey : notnull
    where TValue : class
{
    private readonly Dictionary<TKey, TValue> _store = new();
    
    public TValue? Get(TKey key)
        => _store.TryGetValue(key, out var value) ? value : null;
    
    public void Set(TKey key, TValue value)
        => _store[key] = value;
}

var userCache = new Cache<int, User>();
userCache.Set(1, new User { Id = 1, Name = "Alice" });
User? user = userCache.Get(1);
```

---

## שאלות ראיון נפוצות

### שאלה 1: "למה Generics עדיפים על object?"
**תשובה נכונה:**
- **Type Safety** בcompile-time
- **ביצועים:** ללא boxing/unboxing עבור Value Types
- **קריאות:** קוד ברור יותר

### שאלה 2: "מה הוא Covariance?"
**תשובה נכונה:** Covariance מאפשר להשתמש ב-`IEnumerable<Dog>` כ-`IEnumerable<Animal>` — תת-סוג במקום סוג-אב. מסומן עם `out`.

### שאלה 3: "מה ההבדל בין `where T : class` לבין `where T : struct`?"
**תשובה נכונה:** `class` מגביל ל-Reference Types ומאפשר null. `struct` מגביל ל-Value Types ומונע null.

---

## סיכום Constraints

| Constraint | משמעות |
|------------|--------|
| `where T : class` | Reference Type |
| `where T : struct` | Value Type |
| `where T : new()` | Constructor ריק |
| `where T : BaseClass` | יורש מ-BaseClass |
| `where T : IInterface` | מממש Interface |
| `where T : notnull` | לא null |
| `out T` | Covariant |
| `in T` | Contravariant |

---

*TechAI Explained | מסלול C# & .NET | שיעור 7 מתוך 10*
