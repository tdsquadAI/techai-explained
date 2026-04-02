# שיעור 4: Binary Search — ויריאנטים ומלכודות

**סדרת הכנה לראיונות הייטק | מסלול Algorithms & LeetCode | TechAI Explained**

---

## מבוא

Binary Search נראה פשוט — אבל מרבית המפתחים כותבים אותו עם off-by-one errors.  
ויריאנטים כמו "מצא את הראשון/האחרון" או "חפש במטריצה" הם שאלות ראיון קלאסיות.

---

## Binary Search בסיסי

```csharp
int BinarySearch(int[] arr, int target)
{
    int left = 0, right = arr.Length - 1;
    
    while (left <= right) // <= ולא <
    {
        int mid = left + (right - left) / 2; // מניעת overflow
        
        if (arr[mid] == target) return mid;
        if (arr[mid] < target)  left = mid + 1;
        else                    right = mid - 1;
    }
    return -1;
}
```

---

## Find First Occurrence — ויריאנט חשוב

```csharp
int FindFirst(int[] arr, int target)
{
    int left = 0, right = arr.Length - 1;
    int result = -1;
    
    while (left <= right)
    {
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target)
        {
            result = mid;       // שמירת תוצאה
            right = mid - 1;    // המשך שמאלה — לא עוצרים!
        }
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return result;
}
```

---

## Search in Rotated Sorted Array

```csharp
int SearchRotated(int[] nums, int target)
{
    int left = 0, right = nums.Length - 1;
    
    while (left <= right)
    {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        
        // בדיקה איזה חצי ממוין
        if (nums[left] <= nums[mid])
        {
            if (nums[left] <= target && target < nums[mid])
                right = mid - 1;
            else
                left = mid + 1;
        }
        else
        {
            if (nums[mid] < target && target <= nums[right])
                left = mid + 1;
            else
                right = mid - 1;
        }
    }
    return -1;
}
```

---

## Binary Search על Answer Space

```csharp
// מצא את השורש הריבועי (Floor)
int Sqrt(int x)
{
    if (x < 2) return x;
    int left = 1, right = x / 2;
    
    while (left <= right)
    {
        int mid = left + (right - left) / 2;
        long sq = (long)mid * mid;
        
        if (sq == x) return mid;
        if (sq < x)  left = mid + 1;
        else         right = mid - 1;
    }
    return right; // Floor
}
```

---

## שאלות ראיון נפוצות

### שאלה 1: "למה left + (right - left) / 2 ולא (left + right) / 2?"
**תשובה:** מניעת Integer Overflow. אם left ו-right גדולים, החיבור עלול לגלוש.

### שאלה 2: "מתי Binary Search עובד?"
**תשובה:** כשהnput **ממוין** או כשיש **מונוטוניות** — תנאי שמתחיל False ועובר ל-True (או להיפך).

---

## סיכום

| ויריאנט | מה שונה |
|---------|--------|
| Basic | עוצר כשמוצא |
| First Occurrence | ממשיך שמאלה |
| Last Occurrence | ממשיך ימינה |
| Rotated | בודק איזה חצי ממוין |

---

*TechAI Explained | מסלול Algorithms | שיעור 4 מתוך 10*
