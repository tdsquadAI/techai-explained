# שיעור 10: Entity Framework Core — Migrations, N+1 ואופטימיזציה

**סדרת הכנה לראיונות הייטק | מסלול C# & .NET | TechAI Explained**

---

## מבוא

Entity Framework Core הוא ה-ORM הנפוץ ביותר ב-.NET.  
בראיון, מועמדים שמבינים את בעיית ה-N+1, יודעים לעשות migrations ומבינים את ההבדל בין Eager, Lazy ו-Explicit Loading — מרשימים.

---

## DbContext — הלב של EF Core

```csharp
public class AppDbContext : DbContext
{
    public DbSet<User> Users { get; set; }
    public DbSet<Order> Orders { get; set; }
    
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options) { }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Email).IsRequired().HasMaxLength(256);
            entity.HasMany(e => e.Orders).WithOne(o => o.User);
        });
    }
}

// Registration
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(connectionString));
```

---

## Migrations — ניהול סכמת DB

```bash
# יצירת migration חדש
dotnet ef migrations add AddUserTable

# החלת migrations ל-DB
dotnet ef database update

# ביטול migration אחרון
dotnet ef migrations remove

# הצגת SQL שייווצר
dotnet ef migrations script
```

```csharp
// Migration שנוצר אוטומטית
public partial class AddUserTable : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "Users",
            columns: table => new
            {
                Id = table.Column<int>(nullable: false)
                    .Annotation("SqlServer:Identity", "1, 1"),
                Email = table.Column<string>(maxLength: 256, nullable: false),
                Name = table.Column<string>(maxLength: 100, nullable: true)
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_Users", x => x.Id);
            });
    }
    
    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable(name: "Users");
    }
}
```

---

## N+1 Problem — הבעיה הכי נפוצה!

```csharp
// ❌ N+1 Problem!
var orders = await _context.Orders.ToListAsync(); // 1 שאילתה

foreach (var order in orders) // N שאילתות!
{
    Console.WriteLine(order.User.Name); // Lazy Load — שאילתה לכל order!
}
// סה"כ: 1 + N שאילתות!
```

### Eager Loading — הפתרון

```csharp
// ✅ Eager Loading — שאילתה אחת עם JOIN
var orders = await _context.Orders
    .Include(o => o.User)           // JOIN על Users
    .Include(o => o.Items)          // JOIN על Items
        .ThenInclude(i => i.Product) // JOIN על Products
    .ToListAsync();
// סה"כ: שאילתה אחת!
```

### Explicit Loading — לפי הצורך

```csharp
var order = await _context.Orders.FindAsync(id);

// טעינה מפורשת כשצריך
await _context.Entry(order)
    .Reference(o => o.User)
    .LoadAsync();

await _context.Entry(order)
    .Collection(o => o.Items)
    .LoadAsync();
```

---

## AsNoTracking — שיפור ביצועים

```csharp
// ❌ עם tracking (ברירת מחדל) — שומר snapshot לשינויים
var users = await _context.Users.ToListAsync();

// ✅ ללא tracking — מהיר יותר לread-only
var users = await _context.Users
    .AsNoTracking() // ללא Change Tracking
    .ToListAsync();
```

---

## Raw SQL וFromSqlRaw

```csharp
// Raw SQL כשצריך ביצועים גבוהים
var users = await _context.Users
    .FromSqlRaw("SELECT * FROM Users WHERE Email LIKE {0}", "%@company.com")
    .ToListAsync();

// Stored Procedures
var result = await _context.Database
    .ExecuteSqlRawAsync("EXEC UpdateUserStatus @UserId = {0}", userId);
```

---

## Transactions

```csharp
using var transaction = await _context.Database.BeginTransactionAsync();

try
{
    var order = new Order { UserId = 1, Total = 100 };
    _context.Orders.Add(order);
    await _context.SaveChangesAsync();
    
    var payment = new Payment { OrderId = order.Id, Amount = 100 };
    _context.Payments.Add(payment);
    await _context.SaveChangesAsync();
    
    await transaction.CommitAsync();
}
catch
{
    await transaction.RollbackAsync();
    throw;
}
```

---

## Compiled Queries — ביצועים מקסימליים

```csharp
// שאילתה שמתorגמת פעם אחת ונשמרת
private static readonly Func<AppDbContext, int, Task<User?>> GetUserById =
    EF.CompileAsyncQuery((AppDbContext context, int id) =>
        context.Users.FirstOrDefault(u => u.Id == id));

// שימוש — מהיר יותר כי אין צורך לparse שוב
var user = await GetUserById(_context, 1);
```

---

## שאלות ראיון נפוצות

### שאלה 1: "מה הוא N+1 Problem?"
**תשובה נכונה:** כשמביאים N אובייקטים ואז מבצעים עוד N שאילתות לrelated entities. פותרים עם `Include` (Eager Loading).

### שאלה 2: "מה ההבדל בין Eager, Lazy ו-Explicit Loading?"
**תשובה נכונה:**
- Eager: טוען related data בשאילתה הראשית (`Include`)
- Lazy: טוען כשניגשים ל-property (גורם N+1)
- Explicit: טוענים ידנית כשצריך (`LoadAsync`)

### שאלה 3: "מתי להשתמש ב-AsNoTracking?"
**תשובה נכונה:** כשלא צריך לעדכן את האובייקטים — read-only scenarios. משפר ביצועים כי EF לא עוקב אחרי שינויים.

---

## סיכום

| נושא | הכלי |
|------|------|
| N+1 | `Include` + `ThenInclude` |
| Read performance | `AsNoTracking` |
| Schema changes | `migrations add` + `database update` |
| Complex queries | `FromSqlRaw` |
| Atomic operations | `BeginTransaction` |
| Repeated queries | Compiled Queries |

---

*TechAI Explained | מסלול C# & .NET | שיעור 10 מתוך 10*
