# שיעור 9: Sorting Algorithms — Merge Sort, Quick Sort ומה שביניהם

**סדרת הכנה לראיונות הייטק | מסלול Algorithms & LeetCode | TechAI Explained**

---

## מבוא

"מה הסיבוכיות של Merge Sort?" — שאלת ראיון קלאסית.  
אבל המראיין גם יכול לשאל: "מה stable sort?" או "מתי Quick Sort גרוע מ-O(n log n)?".

---

## Merge Sort — Divide & Conquer

```csharp
void MergeSort(int[] arr, int left, int right)
{
    if (left >= right) return;
    
    int mid = left + (right - left) / 2;
    MergeSort(arr, left, mid);
    MergeSort(arr, mid + 1, right);
    Merge(arr, left, mid, right);
}

void Merge(int[] arr, int left, int mid, int right)
{
    var temp = new int[right - left + 1];
    int i = left, j = mid + 1, k = 0;
    
    while (i <= mid && j <= right)
    {
        if (arr[i] <= arr[j]) temp[k++] = arr[i++];
        else                  temp[k++] = arr[j++];
    }
    while (i <= mid)  temp[k++] = arr[i++];
    while (j <= right) temp[k++] = arr[j++];
    
    Array.Copy(temp, 0, arr, left, temp.Length);
}
// O(n log n) תמיד, O(n) space, STABLE
```

---

## Quick Sort — הכי מהיר בפועל

```csharp
void QuickSort(int[] arr, int left, int right)
{
    if (left >= right) return;
    
    int pivotIdx = Partition(arr, left, right);
    QuickSort(arr, left, pivotIdx - 1);
    QuickSort(arr, pivotIdx + 1, right);
}

int Partition(int[] arr, int left, int right)
{
    int pivot = arr[right]; // pivot אחרון
    int i = left - 1;
    
    for (int j = left; j < right; j++)
    {
        if (arr[j] <= pivot)
        {
            i++;
            (arr[i], arr[j]) = (arr[j], arr[i]);
        }
    }
    (arr[i + 1], arr[right]) = (arr[right], arr[i + 1]);
    return i + 1;
}
// O(n log n) ממוצע, O(n²) worst case, O(1) extra space, NOT stable
```

---

## Counting Sort — O(n) לטווח ידוע

```csharp
int[] CountingSort(int[] arr, int max)
{
    var count = new int[max + 1];
    foreach (int x in arr) count[x]++;
    
    var result = new int[arr.Length];
    int idx = 0;
    for (int i = 0; i <= max; i++)
        while (count[i]-- > 0)
            result[idx++] = i;
    
    return result; // O(n + k), k = range
}
```

---

## השוואת Sorting Algorithms

| אלגוריתם | Best | Average | Worst | Space | Stable |
|----------|------|---------|-------|-------|--------|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ |
| Heap | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ |
| Counting | O(n+k) | O(n+k) | O(n+k) | O(k) | ✅ |

---

## שאלות ראיון נפוצות

### שאלה 1: "מה הוא Stable Sort?"
**תשובה:** אלגוריתם שמשמר את הסדר היחסי של אלמנטים שווים. Merge Sort הוא stable, Quick Sort הוא לא.

### שאלה 2: "מתי Quick Sort גרוע?"
**תשובה:** כשה-pivot תמיד גרוע (ה-minimum או ה-maximum). קורה על מערך ממוין אם תמיד בוחרים ה-pivot האחרון. פתרון: Random pivot.

### שאלה 3: "למה Array.Sort ב-C# משתמש ב-IntroSort?"
**תשובה:** IntroSort מתחיל עם Quick Sort אבל עובר ל-Heap Sort אם רמת הרקורסיה גבוהה מדי. מבטיח O(n log n) worst case.

---

## סיכום

השתמשו ב-**Merge Sort** כשצריך:
- Stable sort מובטח
- Linked lists
- External sorting (קבצים גדולים)

השתמשו ב-**Quick Sort** כשצריך:
- In-place sorting מהיר בממוצע
- Arrays (cache-friendly)
- Random data

---

*TechAI Explained | מסלול Algorithms | שיעור 9 מתוך 10*
