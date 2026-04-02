# שיעור 1: Big O Notation — מדידת סיבוכיות אלגוריתמים

**סדרת הכנה לראיונות הייטק | מסלול Algorithms & LeetCode | TechAI Explained**

---

## מבוא

Big O Notation הוא הבסיס לכל שיחה על ביצועים בראיון.  
"מה הסיבוכיות של הפתרון שלך?" — זו שאלה שתשמע בכל ראיון אלגוריתמי.  
בשיעור הזה נלמד לזהות ולחשב Big O במהירות.

---

## מה הוא Big O?

Big O מתאר איך **זמן הריצה (Time Complexity)** או **שימוש הזיכרון (Space Complexity)** של אלגוריתם גדל ביחס לגודל הקלט.

הסימנים הנפוצים:

| Big O | שם | דוגמה |
|-------|-----|-------|
| O(1) | Constant | גישה למערך בindex |
| O(log n) | Logarithmic | Binary Search |
| O(n) | Linear | Linear Search |
| O(n log n) | Log-linear | Merge Sort |
| O(n²) | Quadratic | Bubble Sort |
| O(2^n) | Exponential | Fibonacci רקורסיבי |

---

## O(1) — Constant Time

```csharp
// גישה ישירה — לא משנה כמה גדול המערך
int GetFirst(int[] arr) => arr[0]; // O(1)

// Hash lookup
var dict = new Dictionary<string, int>();
dict["key"] = 42;
var val = dict["key"]; // O(1) בממוצע
```

---

## O(n) — Linear Time

```csharp
// לולאה פשוטה על כל האלמנטים
int Sum(int[] arr)
{
    int sum = 0;
    foreach (int x in arr) // n iterations
        sum += x;
    return sum; // O(n)
}
```

---

## O(n²) — Quadratic Time

```csharp
// לולאה כפולה — מוצאים כפולים
bool HasDuplicates(int[] arr)
{
    for (int i = 0; i < arr.Length; i++)
        for (int j = i + 1; j < arr.Length; j++) // n * n
            if (arr[i] == arr[j])
                return true;
    return false; // O(n²)
}

// ✅ גרסה יעילה יותר — O(n)
bool HasDuplicatesFast(int[] arr)
{
    var seen = new HashSet<int>();
    foreach (int x in arr)
        if (!seen.Add(x))
            return true;
    return false;
}
```

---

## O(log n) — Logarithmic Time

```csharp
// Binary Search — חוצה את המרחב כל פעם
int BinarySearch(int[] arr, int target)
{
    int left = 0, right = arr.Length - 1;
    
    while (left <= right)
    {
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1; // O(log n)
}
```

---

## Space Complexity

```csharp
// O(1) space — לא משתמשים בזיכרון נוסף
int SumInPlace(int[] arr)
{
    int sum = 0;
    foreach (int x in arr) sum += x;
    return sum; // Space: O(1)
}

// O(n) space — יוצרים מבנה נוסף בגודל n
int[] DuplicateArray(int[] arr)
{
    var result = new int[arr.Length]; // O(n) space
    Array.Copy(arr, result, arr.Length);
    return result;
}
```

---

## Drop Constants — כלל חשוב

```csharp
// O(2n) → O(n) (מורידים את ה-2)
void TwoLoops(int[] arr)
{
    foreach (int x in arr) Console.Write(x); // n
    foreach (int x in arr) Console.Write(x); // n
    // O(2n) = O(n)
}

// O(n + m) — כשיש שני קלטים שונים
void TwoInputs(int[] a, int[] b)
{
    foreach (int x in a) Console.Write(x); // n
    foreach (int x in b) Console.Write(x); // m
    // O(n + m) — לא O(n)!
}
```

---

## שאלות ראיון נפוצות

### שאלה 1: "מה הסיבוכיות של פעולות על מבני נתונים?"

| פעולה | Array | LinkedList | HashMap | BST |
|-------|-------|-----------|---------|-----|
| Access | O(1) | O(n) | O(1) | O(log n) |
| Search | O(n) | O(n) | O(1) | O(log n) |
| Insert | O(n) | O(1) | O(1) | O(log n) |
| Delete | O(n) | O(1) | O(1) | O(log n) |

### שאלה 2: "מה עדיף — O(n log n) או O(n²)?"
**תשובה:** O(n log n) בהרבה. עבור n=1000: log n ≈ 10, אז n log n ≈ 10,000 לעומת n² = 1,000,000.

---

## סיכום ויזואלי

```
מהיר
  O(1)        ────────────────────── קבוע
  O(log n)    ─────────/
  O(n)        ────────/
  O(n log n)  ───────/
  O(n²)       ──────/
  O(2^n)      ─────/
איטי                   n →
```

---

*TechAI Explained | מסלול Algorithms | שיעור 1 מתוך 10*
