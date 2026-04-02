# שיעור 2: Arrays ו-Strings — Two-Pointer ו-Sliding Window

**סדרת הכנה לראיונות הייטק | מסלול Algorithms & LeetCode | TechAI Explained**

---

## מבוא

Arrays ו-Strings הם הנושאים הכי נפוצים ב-LeetCode ובראיונות.  
שני הטכניקות החיוניות: **Two-Pointer** ו-**Sliding Window** יפתרו עשרות שאלות.

---

## Two-Pointer — שני מצביעים

```csharp
// בעיה: האם יש זוג ב-sorted array שסכומו שווה ל-target?
bool TwoSum(int[] arr, int target)
{
    int left = 0, right = arr.Length - 1;
    
    while (left < right)
    {
        int sum = arr[left] + arr[right];
        if (sum == target) return true;
        if (sum < target) left++;
        else right--;
    }
    return false; // O(n) במקום O(n²)!
}
```

---

## Reverse Array — Two-Pointer

```csharp
void ReverseArray(int[] arr)
{
    int left = 0, right = arr.Length - 1;
    
    while (left < right)
    {
        (arr[left], arr[right]) = (arr[right], arr[left]); // swap
        left++;
        right--;
    }
}
```

---

## בעיות String נפוצות

```csharp
// Palindrome check
bool IsPalindrome(string s)
{
    int left = 0, right = s.Length - 1;
    while (left < right)
    {
        if (s[left] != s[right]) return false;
        left++;
        right--;
    }
    return true; // O(n)
}

// Count characters
Dictionary<char, int> CharCount(string s)
{
    var count = new Dictionary<char, int>();
    foreach (char c in s)
        count[c] = count.GetValueOrDefault(c) + 1;
    return count;
}

// Anagram check
bool IsAnagram(string s, string t)
{
    if (s.Length != t.Length) return false;
    var count = new int[26];
    foreach (char c in s) count[c - 'a']++;
    foreach (char c in t) count[c - 'a']--;
    return count.All(x => x == 0);
}
```

---

## Sliding Window — חלון הזזה

```csharp
// מציאת תת-מערך מקסימלי עם סכום K
int MaxSubarraySum(int[] arr, int k)
{
    int windowSum = 0;
    for (int i = 0; i < k; i++)
        windowSum += arr[i];
    
    int maxSum = windowSum;
    
    for (int i = k; i < arr.Length; i++)
    {
        windowSum += arr[i] - arr[i - k]; // הזזת חלון
        maxSum = Math.Max(maxSum, windowSum);
    }
    return maxSum; // O(n)
}
```

---

## שאלות ראיון נפוצות

### שאלה: Remove Duplicates מ-Sorted Array (In-Place)
```csharp
int RemoveDuplicates(int[] nums)
{
    if (nums.Length == 0) return 0;
    int slow = 0;
    
    for (int fast = 1; fast < nums.Length; fast++)
    {
        if (nums[fast] != nums[slow])
        {
            slow++;
            nums[slow] = nums[fast];
        }
    }
    return slow + 1; // O(n), Space O(1)
}
```

---

## סיכום

| טכניקה | מתי להשתמש | סיבוכיות |
|---------|-----------|----------|
| Two-Pointer | sorted array, pairs | O(n) |
| Sliding Window | subarray/substring | O(n) |
| HashMap | frequency count | O(n) |

---

*TechAI Explained | מסלול Algorithms | שיעור 2 מתוך 10*
