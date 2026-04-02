# שיעור 10: Sliding Window Pattern — פתרון בעיות Subarray/Substring

**סדרת הכנה לראיונות הייטק | מסלול Algorithms & LeetCode | TechAI Explained**

---

## מבוא

Sliding Window הוא אחד מהpatterns החשובים ביותר ב-LeetCode.  
הוא הופך עשרות שאלות מ-O(n²) ל-O(n).  
ברגע שמזהים "subarray/substring עם תנאי" — ייתכן שזה Sliding Window.

---

## מתי להשתמש ב-Sliding Window?

- שאלות על **תת-מערך** (subarray) או **תת-מחרוזת** (substring)
- מחפשים מקסימום/מינימום/קיום
- תנאי על "חלון" של אלמנטים רצופים

---

## Fixed-Size Window — חלון קבוע

```csharp
// Maximum Sum Subarray of Size K
int MaxSumSubarray(int[] arr, int k)
{
    int windowSum = 0;
    
    // בניית חלון ראשון
    for (int i = 0; i < k; i++)
        windowSum += arr[i];
    
    int maxSum = windowSum;
    
    // הזזת החלון
    for (int i = k; i < arr.Length; i++)
    {
        windowSum += arr[i] - arr[i - k]; // הוסף חדש, הסר ישן
        maxSum = Math.Max(maxSum, windowSum);
    }
    return maxSum; // O(n)
}

// arr = [2, 1, 5, 1, 3, 2], k = 3
// Windows: [2,1,5]=8, [1,5,1]=7, [5,1,3]=9, [1,3,2]=6
// Max = 9
```

---

## Variable-Size Window — חלון דינמי

```csharp
// Longest Subarray with Sum <= Target
int LongestSubarray(int[] arr, int target)
{
    int left = 0, sum = 0, maxLen = 0;
    
    for (int right = 0; right < arr.Length; right++)
    {
        sum += arr[right]; // הרחב חלון ימינה
        
        // כווץ חלון משמאל עד שהתנאי מתקיים
        while (sum > target)
        {
            sum -= arr[left];
            left++;
        }
        
        maxLen = Math.Max(maxLen, right - left + 1);
    }
    return maxLen; // O(n)
}
```

---

## Longest Substring Without Repeating Characters

```csharp
int LengthOfLongestSubstring(string s)
{
    var charIndex = new Dictionary<char, int>(); // מיקום אחרון
    int left = 0, maxLen = 0;
    
    for (int right = 0; right < s.Length; right++)
    {
        char c = s[right];
        
        // אם תו כבר בחלון — כווץ
        if (charIndex.TryGetValue(c, out int prevIdx) && prevIdx >= left)
            left = prevIdx + 1;
        
        charIndex[c] = right;
        maxLen = Math.Max(maxLen, right - left + 1);
    }
    return maxLen; // O(n)
}
// "abcabcbb" → 3 ("abc")
```

---

## Minimum Window Substring

```csharp
string MinWindow(string s, string t)
{
    var need = new Dictionary<char, int>();
    foreach (char c in t) need[c] = need.GetValueOrDefault(c) + 1;
    
    int have = 0, required = need.Count;
    int left = 0, minLen = int.MaxValue, minLeft = 0;
    var window = new Dictionary<char, int>();
    
    for (int right = 0; right < s.Length; right++)
    {
        char c = s[right];
        window[c] = window.GetValueOrDefault(c) + 1;
        
        if (need.ContainsKey(c) && window[c] == need[c])
            have++;
        
        while (have == required)
        {
            // עדכון תוצאה
            if (right - left + 1 < minLen)
            {
                minLen = right - left + 1;
                minLeft = left;
            }
            
            // כווץ משמאל
            char leftChar = s[left];
            window[leftChar]--;
            if (need.ContainsKey(leftChar) && window[leftChar] < need[leftChar])
                have--;
            left++;
        }
    }
    return minLen == int.MaxValue ? "" : s.Substring(minLeft, minLen);
}
```

---

## Sliding Window Maximum (Deque)

```csharp
int[] MaxSlidingWindow(int[] nums, int k)
{
    var deque = new LinkedList<int>(); // indices
    var result = new int[nums.Length - k + 1];
    
    for (int i = 0; i < nums.Length; i++)
    {
        // הסר אלמנטים מחוץ לחלון
        while (deque.Count > 0 && deque.First!.Value < i - k + 1)
            deque.RemoveFirst();
        
        // הסר אלמנטים קטנים יותר
        while (deque.Count > 0 && nums[deque.Last!.Value] < nums[i])
            deque.RemoveLast();
        
        deque.AddLast(i);
        
        if (i >= k - 1)
            result[i - k + 1] = nums[deque.First!.Value];
    }
    return result; // O(n)
}
```

---

## שאלות ראיון נפוצות

### שאלה 1: "איך מזהים שאלת Sliding Window?"
**תשובה:** "תת-מערך/substring רצוף", "מקסימום/מינימום של חלון", "תנאי על אלמנטים רצופים". אם Brute Force הוא O(n²) — ייתכן שSW יהיה O(n).

### שאלה 2: "מה ההבדל בין Fixed ו-Variable Window?"
**תשובה:** Fixed — גודל החלון קבוע, רק מזיזים. Variable — מרחיבים ומכווצים לפי תנאי.

### שאלה 3: "מה הסיבוכיות?"
**תשובה:** O(n) — כל אלמנט נכנס ויוצא מהחלון לכל היותר פעם אחת.

---

## Template לבעיות Sliding Window

```csharp
int SlidingWindowTemplate(int[] arr, /* תנאי */)
{
    int left = 0, result = 0;
    // state של החלון
    
    for (int right = 0; right < arr.Length; right++)
    {
        // הרחב חלון — הוסף arr[right]
        
        // כווץ חלון אם לא עומד בתנאי
        while (/* תנאי לא מתקיים */)
        {
            // הסר arr[left]
            left++;
        }
        
        // עדכן תוצאה
        result = Math.Max(result, right - left + 1);
    }
    return result;
}
```

---

## סיכום

| שאלה | גישה | מבנה נוסף |
|------|------|----------|
| Fixed sum | Fixed window | - |
| Longest with condition | Variable window | HashSet/Dict |
| No repeating chars | Variable + last index | Dictionary |
| Window maximum | Fixed + Deque | Deque |

---

*TechAI Explained | מסלול Algorithms | שיעור 10 מתוך 10*
