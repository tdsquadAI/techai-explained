# שיעור 4: Dependency Injection — DI Containers ו-Lifetime Scopes

**סדרת הכנה לראיונות הייטק | מסלול C# & .NET | TechAI Explained**

---

## מבוא

Dependency Injection הוא אחד העקרונות הכי נשאלים בראיונות .NET.  
כמעט כל חברה שמשתמשת ב-ASP.NET Core תשאל עליו.  
הבנה טובה של DI, הclifetimes והcontainers מראה שאתם מבינים **ארכיטקטורה נכונה**.

---

## מה הוא Dependency Injection?

**Dependency Injection** הוא עיקרון שבו אובייקט מקבל את ה-**dependencies** שלו מבחוץ, במקום ליצור אותם בעצמו.

```csharp
// ❌ ללא DI — קשה לבדוק, קשה לשנות
public class OrderService
{
    private readonly EmailService _emailService;
    
    public OrderService()
    {
        _emailService = new EmailService(); // תלות ישירה!
    }
}

// ✅ עם DI — גמיש וניתן לבדיקה
public class OrderService
{
    private readonly IEmailService _emailService;
    
    public OrderService(IEmailService emailService) // מוזרק מבחוץ
    {
        _emailService = emailService;
    }
}
```

---

## Registration ב-ASP.NET Core

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// רישום services
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddTransient<IEmailService, EmailService>();
builder.Services.AddSingleton<IConfiguration>(config);

var app = builder.Build();
```

---

## שלושת ה-Lifetimes — הנושא הכי נשאל!

### 1. Transient — כל פעם instance חדש

```csharp
builder.Services.AddTransient<IEmailService, EmailService>();
```

- **Instance חדש** בכל פעם שמבקשים
- מתאים לservices **stateless** וקלות
- **זהירות:** אם מוזרק ל-Singleton — נשמר!

```csharp
public class Controller
{
    // כל HTTP request יקבל EmailService חדש
    public Controller(IEmailService email1, IEmailService email2)
    {
        // email1 != email2 — שני instances שונים!
    }
}
```

### 2. Scoped — instance אחד לbag scope

```csharp
builder.Services.AddScoped<IOrderService, OrderService>();
```

- **Instance אחד** לכל HTTP request (ב-web)
- משותף בתוך אותו request
- **מתאים ל:** DbContext, Unit of Work

```csharp
// באותו request — אותו instance
public class ServiceA
{
    public ServiceA(IOrderService orders) { }
}

public class ServiceB
{
    public ServiceB(IOrderService orders) { } // אותו orders כמו ServiceA!
}
```

### 3. Singleton — instance אחד לכל חיי האפליקציה

```csharp
builder.Services.AddSingleton<ICacheService, CacheService>();
```

- **Instance אחד** לכל חיי האפליקציה
- **זהירות:** חייב להיות thread-safe!
- **מתאים ל:** Cache, Configuration, Logger factories

---

## Captive Dependency — הבאג הנפוץ

```csharp
// ❌ בעיה! — Singleton מחזיק Scoped dependency
builder.Services.AddSingleton<MyService>();
builder.Services.AddScoped<IDbContext, AppDbContext>();

public class MyService
{
    // ❌ DbContext הוא Scoped, אבל MyService הוא Singleton
    // DbContext ראשון ייתפס לנצח ב-MyService!
    public MyService(IDbContext dbContext) { }
}
```

**הכלל:** Singleton לא יכול להחזיק dependency עם חיים קצרים יותר.

```
Singleton > Scoped > Transient
```

---

## IServiceProvider ו-Factory Pattern

```csharp
// כשצריך ליצור service דינמית
public class OrderProcessor
{
    private readonly IServiceProvider _serviceProvider;
    
    public OrderProcessor(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }
    
    public void ProcessOrder(OrderType type)
    {
        // יצירה דינמית לפי סוג
        using var scope = _serviceProvider.CreateScope();
        var handler = scope.ServiceProvider.GetRequiredService<IOrderHandler>();
        handler.Handle(type);
    }
}
```

---

## Named Services וKeyed DI (C# 8+ / .NET 8)

```csharp
// .NET 8 — Keyed Services
builder.Services.AddKeyedScoped<INotificationService, EmailService>("email");
builder.Services.AddKeyedScoped<INotificationService, SmsService>("sms");

public class NotificationManager
{
    public NotificationManager(
        [FromKeyedServices("email")] INotificationService emailService,
        [FromKeyedServices("sms")] INotificationService smsService)
    { }
}
```

---

## שאלות ראיון נפוצות

### שאלה 1: "מה ההבדל בין Transient, Scoped ו-Singleton?"
**תשובה נכונה:**
- **Transient:** חדש בכל הזרקה — stateless services
- **Scoped:** חדש בכל request — DbContext, Unit of Work  
- **Singleton:** אחד לאפליקציה — Cache, Config

### שאלה 2: "מה הוא Captive Dependency?"
**תשובה נכונה:** כשservice בעל חיים ארוכים מחזיק תלות בעלת חיים קצרים יותר. Singleton שמחזיק Scoped dependency — ה-Scoped לא יתחדש.

### שאלה 3: "למה DI עדיף על new?"
**תשובה נכונה:**
- **Testability:** אפשר להזריק מocks בבדיקות
- **Loose Coupling:** תלות בinterface, לא ב-implementation
- **Lifecycle Management:** ה-container מנהל חיים ושחרור

---

## סיכום

| Lifetime | יצירה | שחרור | שימוש |
|----------|-------|-------|-------|
| Transient | בכל הזרקה | בסוף scope | Stateless utilities |
| Scoped | בכל request | בסוף request | DbContext, UoW |
| Singleton | פעם אחת | סגירת app | Cache, Config |

---

*TechAI Explained | מסלול C# & .NET | שיעור 4 מתוך 10*
