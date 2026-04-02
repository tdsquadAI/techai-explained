# שיעור 3: Linked Lists — מבנה הנתונים הקלאסי

**סדרת הכנה לראיונות הייטק | מסלול Algorithms & LeetCode | TechAI Explained**

---

## מבוא

Linked Lists הן אחת השאלות הקלאסיות ביותר בראיונות.  
Reversal, cycle detection וmerge — אלה שאלות שכדאי לפתור תוך שניות.

---

## Node ו-LinkedList

```csharp
public class ListNode
{
    public int Val;
    public ListNode? Next;
    
    public ListNode(int val = 0, ListNode? next = null)
    {
        Val = val;
        Next = next;
    }
}
```

---

## Reverse Linked List — השאלה הקלאסית

```csharp
// Iterative — O(n) time, O(1) space
ListNode? ReverseList(ListNode? head)
{
    ListNode? prev = null;
    ListNode? curr = head;
    
    while (curr != null)
    {
        ListNode? next = curr.Next; // שמירה
        curr.Next = prev;           // היפוך
        prev = curr;                // קדמה
        curr = next;                // קדמה
    }
    return prev;
}

// Recursive — O(n) time, O(n) space
ListNode? ReverseListRec(ListNode? head)
{
    if (head?.Next == null) return head;
    
    var newHead = ReverseListRec(head.Next);
    head.Next.Next = head;
    head.Next = null;
    return newHead;
}
```

---

## Fast & Slow Pointers — Cycle Detection

```csharp
// Floyd's Algorithm — מציאת מעגל
bool HasCycle(ListNode? head)
{
    var slow = head;
    var fast = head;
    
    while (fast?.Next != null)
    {
        slow = slow!.Next;
        fast = fast.Next.Next;
        
        if (slow == fast) return true; // מצאנו מעגל
    }
    return false; // O(n), Space O(1)
}

// מציאת אמצע הרשימה
ListNode? FindMiddle(ListNode? head)
{
    var slow = head;
    var fast = head;
    
    while (fast?.Next != null)
    {
        slow = slow!.Next;
        fast = fast.Next.Next;
    }
    return slow; // האמצע
}
```

---

## Merge Two Sorted Lists

```csharp
ListNode? MergeTwoLists(ListNode? l1, ListNode? l2)
{
    var dummy = new ListNode(0);
    var curr = dummy;
    
    while (l1 != null && l2 != null)
    {
        if (l1.Val <= l2.Val)
        {
            curr.Next = l1;
            l1 = l1.Next;
        }
        else
        {
            curr.Next = l2;
            l2 = l2.Next;
        }
        curr = curr.Next;
    }
    
    curr.Next = l1 ?? l2; // שאריות
    return dummy.Next; // O(n+m)
}
```

---

## Delete N-th Node from End

```csharp
ListNode? RemoveNthFromEnd(ListNode? head, int n)
{
    var dummy = new ListNode(0, head);
    var fast = dummy;
    var slow = dummy;
    
    for (int i = 0; i <= n; i++)
        fast = fast.Next!;
    
    while (fast != null)
    {
        fast = fast.Next;
        slow = slow.Next!;
    }
    
    slow.Next = slow.Next?.Next;
    return dummy.Next;
}
```

---

## שאלות ראיון נפוצות

### שאלה 1: "מה יתרון Linked List על Array?"
**תשובה:** Insertion/Deletion ב-O(1) כשיש pointer (אין shift). אבל Random Access הוא O(n).

### שאלה 2: "איך בודקים מעגל?"
**תשובה:** Floyd's Cycle Detection — Fast & Slow pointers. אם נפגשים — יש מעגל.

---

## סיכום

| פעולה | Singly Linked | Array |
|-------|--------------|-------|
| Access | O(n) | O(1) |
| Insert Head | O(1) | O(n) |
| Insert Tail | O(n) | O(1) amortized |
| Delete | O(n) search | O(n) shift |

---

*TechAI Explained | מסלול Algorithms | שיעור 3 מתוך 10*
