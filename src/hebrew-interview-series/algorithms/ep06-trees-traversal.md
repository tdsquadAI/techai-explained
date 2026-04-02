# שיעור 6: עצים ו-Traversal — BFS, DFS וBinary Trees

**סדרת הכנה לראיונות הייטק | מסלול Algorithms & LeetCode | TechAI Explained**

---

## מבוא

עצים הם הנושא הכי נפוץ בראיונות אחרי arrays.  
BFS ו-DFS הם שתי הגישות הבסיסיות שצריך לדעת בעיניים עצומות.

---

## TreeNode

```csharp
public class TreeNode
{
    public int Val;
    public TreeNode? Left, Right;
    
    public TreeNode(int val = 0, TreeNode? left = null, TreeNode? right = null)
    {
        Val = val; Left = left; Right = right;
    }
}
```

---

## DFS — Depth First Search

### InOrder (Left → Root → Right) — יוצא ממוין מ-BST

```csharp
IList<int> InOrder(TreeNode? root)
{
    var result = new List<int>();
    
    void Traverse(TreeNode? node)
    {
        if (node == null) return;
        Traverse(node.Left);
        result.Add(node.Val);
        Traverse(node.Right);
    }
    
    Traverse(root);
    return result;
}
```

### PreOrder (Root → Left → Right)

```csharp
void PreOrder(TreeNode? node, IList<int> result)
{
    if (node == null) return;
    result.Add(node.Val);       // Root קודם
    PreOrder(node.Left, result);
    PreOrder(node.Right, result);
}
```

---

## BFS — Breadth First Search (Level Order)

```csharp
IList<IList<int>> LevelOrder(TreeNode? root)
{
    var result = new List<IList<int>>();
    if (root == null) return result;
    
    var queue = new Queue<TreeNode>();
    queue.Enqueue(root);
    
    while (queue.Count > 0)
    {
        int levelSize = queue.Count;
        var level = new List<int>();
        
        for (int i = 0; i < levelSize; i++)
        {
            var node = queue.Dequeue();
            level.Add(node.Val);
            
            if (node.Left != null) queue.Enqueue(node.Left);
            if (node.Right != null) queue.Enqueue(node.Right);
        }
        result.Add(level);
    }
    return result;
}
```

---

## Maximum Depth

```csharp
int MaxDepth(TreeNode? root)
{
    if (root == null) return 0;
    return 1 + Math.Max(MaxDepth(root.Left), MaxDepth(root.Right));
}
```

---

## Validate BST

```csharp
bool IsValidBST(TreeNode? root,
    long min = long.MinValue, long max = long.MaxValue)
{
    if (root == null) return true;
    if (root.Val <= min || root.Val >= max) return false;
    
    return IsValidBST(root.Left, min, root.Val) &&
           IsValidBST(root.Right, root.Val, max);
}
```

---

## Lowest Common Ancestor

```csharp
TreeNode? LCA(TreeNode? root, TreeNode p, TreeNode q)
{
    if (root == null || root == p || root == q) return root;
    
    var left = LCA(root.Left, p, q);
    var right = LCA(root.Right, p, q);
    
    if (left != null && right != null) return root; // p וq בצדדים שונים
    return left ?? right;
}
```

---

## שאלות ראיון נפוצות

### שאלה 1: "מתי BFS ומתי DFS?"
**תשובה:**
- **BFS:** מצא shortest path, level-order, "קרוב ביותר"
- **DFS:** בדיקת מסלולים, backtracking, depth-based

### שאלה 2: "מה הסיבוכיות של tree traversal?"
**תשובה:** O(n) time — מבקרים כל node פעם. O(h) space — h הוא עומק העץ (Stack recursion). עץ מאוזן: O(log n), worst case: O(n).

---

## סיכום

| Traversal | סדר | שימוש |
|-----------|-----|-------|
| InOrder | L-Root-R | ממוין מBST |
| PreOrder | Root-L-R | Copy עץ |
| PostOrder | L-R-Root | מחיקת עץ |
| BFS | Level by level | Shortest path |

---

*TechAI Explained | מסלול Algorithms | שיעור 6 מתוך 10*
