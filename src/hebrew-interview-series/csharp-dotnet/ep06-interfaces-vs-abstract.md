# שיעור 6: Interfaces vs Abstract Classes — מתי להשתמש בכל אחד?

**סדרת הכנה לראיונות הייטק | מסלול C# & .NET | TechAI Explained**

---

## מבוא

"מה ההבדל בין Interface לAbstract Class?" — שאלה קלאסית שנשמעת פשוטה.  
אבל המראיין לא מחפש רק הגדרות. הוא רוצה לדעת שאתם מבינים **מתי** ולמה לבחור בכל אחד.  
בשיעור הזה נלמד את ההבדלים, את הכללים ואת ה-default interface methods שמשנים את המשחק.

---

## Interface — הגדרה

**Interface** מגדיר **חוזה** (contract) — מה מחלקה יכולה לעשות, ללא implementation.

```csharp
public interface IAnimal
{
    string Name { get; }
    void MakeSound();
    
    // Default implementation (C# 8+)
    void Describe() => Console.WriteLine($"I am {Name}");
}

public class Dog : IAnimal
{
    public string Name => "Dog";
    
    public void MakeSound() => Console.WriteLine("Woof!");
    // Describe() — משתמשים ב-default implementation
}
```

---

## Abstract Class — הגדרה

**Abstract Class** מגדיר **בסיס חלקי** — יכול להכיל implementation, fields, constructors.

```csharp
public abstract class Animal
{
    protected string _name;
    
    public Animal(string name) // Constructor — לא אפשרי ב-Interface
    {
        _name = name;
    }
    
    public abstract void MakeSound(); // חייב להיות ממומש
    
    public virtual void Sleep() // אפשר לoverride
    {
        Console.WriteLine($"{_name} is sleeping");
    }
    
    public void Breathe() // implementation קבועה
    {
        Console.WriteLine($"{_name} is breathing");
    }
}

public class Dog : Animal
{
    public Dog() : base("Dog") { }
    
    public override void MakeSound() => Console.WriteLine("Woof!");
}
```

---

## השוואה מלאה

| מאפיין | Interface | Abstract Class |
|--------|-----------|----------------|
| Multiple inheritance | ✅ כן | ❌ לא |
| Fields/State | ❌ לא | ✅ כן |
| Constructor | ❌ לא | ✅ כן |
| Access modifiers | ✅ כן (C# 8+) | ✅ כן |
| Default implementation | ✅ כן (C# 8+) | ✅ כן |
| "Is-a" relationship | לרוב לא | כן |
| "Can-do" relationship | כן | לפעמים |

---

## מתי להשתמש בכל אחד?

### Interface — כשמגדירים יכולת (capability)

```csharp
// כלי שניתן לשמור
public interface ISaveable
{
    Task SaveAsync();
}

// כלי שניתן לייצא
public interface IExportable
{
    byte[] Export();
}

// מחלקה יכולה לממש שניהם!
public class Document : ISaveable, IExportable
{
    public async Task SaveAsync() { /* ... */ }
    public byte[] Export() { /* ... */ }
}
```

### Abstract Class — כשיש קוד משותף

```csharp
// כל ה-Repositories חולקים את אותה logique בסיסית
public abstract class RepositoryBase<T>
{
    protected readonly DbContext _context;
    
    protected RepositoryBase(DbContext context)
    {
        _context = context;
    }
    
    public abstract Task<T?> GetByIdAsync(int id);
    
    // shared implementation
    public async Task<List<T>> GetAllAsync()
    {
        return await _context.Set<T>().ToListAsync();
    }
    
    public async Task AddAsync(T entity)
    {
        await _context.Set<T>().AddAsync(entity);
        await _context.SaveChangesAsync();
    }
}

public class UserRepository : RepositoryBase<User>
{
    public UserRepository(DbContext context) : base(context) { }
    
    public override async Task<User?> GetByIdAsync(int id)
        => await _context.Users.FindAsync(id);
}
```

---

## Default Interface Methods (C# 8+)

מאפשרים הוספת implementation לinterface ללא שבירת מחלקות קיימות:

```csharp
public interface ILogger
{
    void Log(string message);
    
    // default implementation — backwards compatible
    void LogError(string message) => Log($"[ERROR] {message}");
    void LogInfo(string message) => Log($"[INFO] {message}");
}

// מחלקה ישנה לא שוברת
public class ConsoleLogger : ILogger
{
    public void Log(string message) => Console.WriteLine(message);
    // LogError ו-LogInfo עובדים ע"י default!
}
```

---

## שאלות ראיון נפוצות

### שאלה 1: "מה ההבדל העיקרי?"
**תשובה מלאה:**
- Interface = חוזה, מגדיר "מה", multiple inheritance, ללא state
- Abstract class = בסיס חלקי, מגדיר "מה + איך חלקי", single inheritance, יכול להכיל state

### שאלה 2: "מתי תבחר Interface?"
**תשובה:** כשרוצים להגדיר יכולת (capability) שמחלקות שונות ממשות, ובמיוחד כשצריך multiple inheritance.

### שאלה 3: "מתי תבחר Abstract Class?"
**תשובה:** כשיש קוד משותף (shared logic) שרוצים לחלוק בין מחלקות, ויש קשר "is-a" אמיתי.

---

## הכלל האצבע

```
Use Interface when:
  ✓ Multiple implementations with no shared code
  ✓ Multiple inheritance needed
  ✓ Defining capabilities (IDisposable, IComparable)

Use Abstract Class when:
  ✓ Shared code between related classes
  ✓ "Is-a" relationship (Dog IS-A Animal)
  ✓ Need constructors or instance state
```

---

*TechAI Explained | מסלול C# & .NET | שיעור 6 מתוך 10*
