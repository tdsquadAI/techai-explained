# שיעור 5: Stacks ו-Queues — מבני נתונים ושימושים

**סדרת הכנה לראיונות הייטק | מסלול Algorithms & LeetCode | TechAI Explained**

---

## מבוא

Stack וQueue הם מבני נתונים בסיסיים עם שימושים עצומים — parsing, BFS/DFS, undo/redo.  
בשיעור זה נכסה את המבנים, היישומים ושאלות ראיון קלאסיות.

---

## Stack — LIFO

```csharp
// מימוש עם Stack<T> מ-.NET
var stack = new Stack<int>();
stack.Push(1);  // [1]
stack.Push(2);  // [1, 2]
stack.Push(3);  // [1, 2, 3]

int top = stack.Peek();  // 3 — ללא הסרה
int val = stack.Pop();   // 3 — עם הסרה
// [1, 2]

// מימוש ידני עם LinkedList
public class MyStack<T>
{
    private readonly LinkedList<T> _list = new();
    
    public void Push(T item) => _list.AddLast(item);
    public T Pop() 
    {
        var val = _list.Last!.Value;
        _list.RemoveLast();
        return val;
    }
    public T Peek() => _list.Last!.Value;
    public bool IsEmpty => _list.Count == 0;
}
```

---

## Queue — FIFO

```csharp
var queue = new Queue<int>();
queue.Enqueue(1); // [1]
queue.Enqueue(2); // [1, 2]
queue.Enqueue(3); // [1, 2, 3]

int front = queue.Peek();    // 1 — ללא הסרה
int val = queue.Dequeue();   // 1 — עם הסרה
// [2, 3]
```

---

## Valid Parentheses — Stack קלאסי

```csharp
bool IsValid(string s)
{
    var stack = new Stack<char>();
    var matching = new Dictionary<char, char>
    {
        { ')', '(' }, { ']', '[' }, { '}', '{' }
    };
    
    foreach (char c in s)
    {
        if ("([{".Contains(c))
        {
            stack.Push(c);
        }
        else if (matching.ContainsKey(c))
        {
            if (stack.Count == 0 || stack.Pop() != matching[c])
                return false;
        }
    }
    return stack.Count == 0; // O(n)
}
```

---

## Monotonic Stack — שאלות מתקדמות

```csharp
// Next Greater Element
int[] NextGreaterElement(int[] arr)
{
    int n = arr.Length;
    var result = new int[n];
    Array.Fill(result, -1);
    var stack = new Stack<int>(); // שומר indices
    
    for (int i = 0; i < n; i++)
    {
        while (stack.Count > 0 && arr[stack.Peek()] < arr[i])
        {
            result[stack.Pop()] = arr[i];
        }
        stack.Push(i);
    }
    return result; // O(n)
}
// arr = [2,1,2,4,3] → [4,2,4,-1,-1]
```

---

## Min Stack

```csharp
public class MinStack
{
    private readonly Stack<int> _stack = new();
    private readonly Stack<int> _minStack = new();
    
    public void Push(int val)
    {
        _stack.Push(val);
        int min = _minStack.Count == 0 ? val : Math.Min(val, _minStack.Peek());
        _minStack.Push(min);
    }
    
    public void Pop()
    {
        _stack.Pop();
        _minStack.Pop();
    }
    
    public int Top() => _stack.Peek();
    public int GetMin() => _minStack.Peek(); // O(1)!
}
```

---

## שאלות ראיון נפוצות

### שאלה 1: "מה ההבדל בין Stack ל-Queue?"
**תשובה:** Stack הוא LIFO (Last In First Out) — כמו ערימת צלחות. Queue הוא FIFO (First In First Out) — כמו תור.

### שאלה 2: "מה הוא Monotonic Stack?"
**תשובה:** Stack שמנהל סדר מונוטוני (עולה/יורד). שימושי לבעיות "Next Greater Element", "Largest Rectangle in Histogram".

---

## סיכום

| מבנה | הכנסה | הוצאה | שימוש |
|------|-------|-------|-------|
| Stack | Push O(1) | Pop O(1) | DFS, Parentheses |
| Queue | Enqueue O(1) | Dequeue O(1) | BFS, Scheduling |
| Deque | O(1) משני צדדים | O(1) | Sliding Window Max |

---

*TechAI Explained | מסלול Algorithms | שיעור 5 מתוך 10*
