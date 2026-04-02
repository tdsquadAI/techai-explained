# שיעור 7: Dynamic Programming — Memoization ו-Tabulation

**סדרת הכנה לראיונות הייטק | מסלול Algorithms & LeetCode | TechAI Explained**

---

## מבוא

Dynamic Programming (DP) הוא הנושא הכי מרתיע בראיונות — אבל עם הגישה הנכונה, יש pattern ברור.  
כל בעיית DP ניתן לפתור בשלושה שלבים: זיהוי subproblems, הגדרת recurrence, בחירת top-down או bottom-up.

---

## מתי להשתמש ב-DP?

שני תנאים:
1. **Overlapping Subproblems** — אותן תת-בעיות נפתרות שוב ושוב
2. **Optimal Substructure** — הפתרון האופטימלי בנוי מפתרונות אופטימליים של תת-בעיות

---

## Fibonacci — הדוגמה הבסיסית

```csharp
// ❌ רקורסיה נאיבית — O(2^n)
int Fib(int n) => n <= 1 ? n : Fib(n - 1) + Fib(n - 2);

// ✅ Memoization (Top-Down) — O(n)
int FibMemo(int n, Dictionary<int, int> memo)
{
    if (n <= 1) return n;
    if (memo.ContainsKey(n)) return memo[n]; // cache hit
    
    memo[n] = FibMemo(n - 1, memo) + FibMemo(n - 2, memo);
    return memo[n];
}

// ✅ Tabulation (Bottom-Up) — O(n) time, O(1) space
int FibTab(int n)
{
    if (n <= 1) return n;
    int prev2 = 0, prev1 = 1;
    
    for (int i = 2; i <= n; i++)
    {
        int curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

---

## Climbing Stairs — LeetCode 70

```csharp
// מדרגות — אפשר לעלות 1 או 2 בכל פעם
int ClimbStairs(int n)
{
    if (n <= 2) return n;
    int one = 1, two = 2;
    
    for (int i = 3; i <= n; i++)
    {
        int curr = one + two;
        one = two;
        two = curr;
    }
    return two; // O(n) time, O(1) space
}
```

---

## 0/1 Knapsack

```csharp
// בחירת פריטים עם משקל מקסימלי לשקית
int Knapsack(int[] weights, int[] values, int capacity)
{
    int n = weights.Length;
    var dp = new int[n + 1, capacity + 1];
    
    for (int i = 1; i <= n; i++)
    {
        for (int w = 0; w <= capacity; w++)
        {
            // לא לוקחים פריט i
            dp[i, w] = dp[i - 1, w];
            
            // לוקחים פריט i (אם אפשר)
            if (weights[i - 1] <= w)
                dp[i, w] = Math.Max(dp[i, w],
                    dp[i - 1, w - weights[i - 1]] + values[i - 1]);
        }
    }
    return dp[n, capacity]; // O(n*W)
}
```

---

## Longest Common Subsequence (LCS)

```csharp
int LCS(string s1, string s2)
{
    int m = s1.Length, n = s2.Length;
    var dp = new int[m + 1, n + 1];
    
    for (int i = 1; i <= m; i++)
    {
        for (int j = 1; j <= n; j++)
        {
            if (s1[i - 1] == s2[j - 1])
                dp[i, j] = dp[i - 1, j - 1] + 1;
            else
                dp[i, j] = Math.Max(dp[i - 1, j], dp[i, j - 1]);
        }
    }
    return dp[m, n]; // O(m*n)
}
```

---

## Coin Change

```csharp
int CoinChange(int[] coins, int amount)
{
    var dp = new int[amount + 1];
    Array.Fill(dp, amount + 1); // infinity
    dp[0] = 0;
    
    for (int i = 1; i <= amount; i++)
    {
        foreach (int coin in coins)
            if (coin <= i)
                dp[i] = Math.Min(dp[i], dp[i - coin] + 1);
    }
    
    return dp[amount] > amount ? -1 : dp[amount];
}
```

---

## שאלות ראיון נפוצות

### שאלה 1: "מה ההבדל בין Memoization לTabulation?"
**תשובה:**
- **Memoization (Top-Down):** רקורסיה + cache, נוח לכתיבה
- **Tabulation (Bottom-Up):** לולאה + table, יותר space-efficient, ללא stack overflow

### שאלה 2: "איך מזהים בעיית DP?"
**תשובה:** שאל: "האם אפשר לפרק לתת-בעיות חופפות?" ו"האם הפתרון הבנוי מהשתבעיות שלו?" אם כן — DP.

---

## סיכום DP Patterns

| Pattern | דוגמה | State |
|---------|-------|-------|
| Linear | Fibonacci, Stairs | dp[i] |
| 2D Grid | LCS, Edit Distance | dp[i][j] |
| Knapsack | 0/1 Knapsack | dp[i][w] |
| Interval | Matrix Chain | dp[i][j] |

---

*TechAI Explained | מסלול Algorithms | שיעור 7 מתוך 10*
