# שיעור 9: Design Patterns ב-C# — Singleton, Factory, Repository

**סדרת הכנה לראיונות הייטק | מסלול C# & .NET | TechAI Explained**

---

## מבוא

Design Patterns הם "פתרונות מוכחים לבעיות חוזרות". כל מפתח בכיר מצפה שתכיר לפחות את הפטרנים הנפוצים.  
בראיון, לא מספיק לדעת את ה-pattern — צריך להסביר **מתי ולמה** להשתמש בו, ואת המחסרונות שלו.

---

## Singleton Pattern

מבטיח שמחלקה תיצור **instance אחד בלבד** לאורך חיי האפליקציה.

### Singleton הבסיסי (Thread-Safe)

```csharp
public class ConfigurationManager
{
    private static ConfigurationManager? _instance;
    private static readonly object _lock = new object();
    
    private ConfigurationManager()
    {
        // Private constructor — מונע יצירה חיצונית
        LoadConfiguration();
    }
    
    public static ConfigurationManager Instance
    {
        get
        {
            if (_instance == null)
            {
                lock (_lock) // Double-check locking
                {
                    _instance ??= new ConfigurationManager();
                }
            }
            return _instance;
        }
    }
    
    public string GetValue(string key) => /* ... */ "";
    
    private void LoadConfiguration() { }
}

// שימוש
var config = ConfigurationManager.Instance;
var value = config.GetValue("ConnectionString");
```

### Singleton מודרני עם Lazy\<T\>

```csharp
public class AppCache
{
    private static readonly Lazy<AppCache> _lazy =
        new Lazy<AppCache>(() => new AppCache());
    
    public static AppCache Instance => _lazy.Value;
    
    private AppCache() { }
}
```

### ⚠️ בעיות של Singleton
- קשה לבדיקה (unit tests)
- מסתיר dependencies
- בעיות ב-multi-threading אם לא מיושם נכון

---

## Factory Pattern

**Factory** מפריד בין יצירת אובייקטים לבין השימוש בהם.

### Simple Factory

```csharp
public abstract class Notification
{
    public abstract void Send(string message);
}

public class EmailNotification : Notification
{
    public override void Send(string message) =>
        Console.WriteLine($"Email: {message}");
}

public class SmsNotification : Notification
{
    public override void Send(string message) =>
        Console.WriteLine($"SMS: {message}");
}

public class NotificationFactory
{
    public static Notification Create(string type) => type switch
    {
        "email" => new EmailNotification(),
        "sms" => new SmsNotification(),
        _ => throw new ArgumentException($"Unknown type: {type}")
    };
}

// שימוש
var notification = NotificationFactory.Create("email");
notification.Send("Hello!"); // Email: Hello!
```

### Abstract Factory

```csharp
public interface IUiFactory
{
    IButton CreateButton();
    ICheckbox CreateCheckbox();
}

public class WindowsUiFactory : IUiFactory
{
    public IButton CreateButton() => new WindowsButton();
    public ICheckbox CreateCheckbox() => new WindowsCheckbox();
}

public class MacUiFactory : IUiFactory
{
    public IButton CreateButton() => new MacButton();
    public ICheckbox CreateCheckbox() => new MacCheckbox();
}
```

---

## Repository Pattern

**Repository** מסתיר את פרטי גישת הנתונים מה-business logic.

```csharp
public interface IUserRepository
{
    Task<User?> GetByIdAsync(int id);
    Task<IEnumerable<User>> GetAllAsync();
    Task<User> AddAsync(User user);
    Task UpdateAsync(User user);
    Task DeleteAsync(int id);
}

public class UserRepository : IUserRepository
{
    private readonly AppDbContext _context;
    
    public UserRepository(AppDbContext context)
    {
        _context = context;
    }
    
    public async Task<User?> GetByIdAsync(int id)
        => await _context.Users.FindAsync(id);
    
    public async Task<IEnumerable<User>> GetAllAsync()
        => await _context.Users.ToListAsync();
    
    public async Task<User> AddAsync(User user)
    {
        _context.Users.Add(user);
        await _context.SaveChangesAsync();
        return user;
    }
    
    public async Task UpdateAsync(User user)
    {
        _context.Users.Update(user);
        await _context.SaveChangesAsync();
    }
    
    public async Task DeleteAsync(int id)
    {
        var user = await GetByIdAsync(id);
        if (user != null)
        {
            _context.Users.Remove(user);
            await _context.SaveChangesAsync();
        }
    }
}

// Service משתמש ב-Interface, לא ב-implementation
public class UserService
{
    private readonly IUserRepository _repository;
    
    public UserService(IUserRepository repository) // DI
    {
        _repository = repository;
    }
    
    public async Task<User?> GetUserAsync(int id)
        => await _repository.GetByIdAsync(id);
}
```

---

## Observer Pattern

```csharp
// .NET מספק IObserver<T> ו-IObservable<T>
public class StockMarket : IObservable<decimal>
{
    private readonly List<IObserver<decimal>> _observers = new();
    
    public IDisposable Subscribe(IObserver<decimal> observer)
    {
        _observers.Add(observer);
        return new Unsubscriber(_observers, observer);
    }
    
    public void UpdatePrice(decimal price)
    {
        foreach (var observer in _observers)
            observer.OnNext(price);
    }
}
```

---

## שאלות ראיון נפוצות

### שאלה 1: "מה ה-pattern המתאים ל-DbContext?"
**תשובה נכונה:** Repository Pattern (לגישת נתונים) יחד עם Unit of Work Pattern (לניהול transactions).

### שאלה 2: "מה החסרונות של Singleton?"
**תשובה נכונה:** קשה ל-unit testing (צריך dependency injection במקום), מסתיר dependencies, בעיות thread safety אם לא מיושם נכון.

### שאלה 3: "מה ההבדל בין Factory Method לAbstract Factory?"
**תשובה נכונה:** Factory Method יוצר product אחד. Abstract Factory יוצר **משפחת products** שעובדים יחד.

---

## סיכום

| Pattern | בעיה שפותר | מתי להשתמש |
|---------|-----------|------------|
| Singleton | Instance יחיד | Config, Cache, Logger |
| Factory | הסתרת יצירת אובייקטים | יצירה מותנית |
| Repository | הפרדת data access | ניגשים ל-DB |
| Observer | event broadcasting | real-time notifications |

---

*TechAI Explained | מסלול C# & .NET | שיעור 9 מתוך 10*
