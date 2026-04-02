# שיעור 8: Graphs — BFS, DFS ו-Dijkstra

**סדרת הכנה לראיונות הייטק | מסלול Algorithms & LeetCode | TechAI Explained**

---

## מבוא

Graphs הם מבנה הנתונים הכי כללי — עצים, מפות, רשתות חברתיות — כולם graphs.  
BFS למרחק, DFS למסלולים, Dijkstra לנתיב קצר — שלושת האלגוריתמים שחייבים לדעת.

---

## ייצוג Graph

```csharp
// Adjacency List — נפוץ בשאלות
var graph = new Dictionary<int, List<int>>
{
    { 0, new List<int> { 1, 2 } },
    { 1, new List<int> { 0, 3 } },
    { 2, new List<int> { 0, 4 } },
    { 3, new List<int> { 1 } },
    { 4, new List<int> { 2 } }
};
```

---

## BFS על Graph — Shortest Path

```csharp
int ShortestPath(int[][] graph, int src, int dst)
{
    var visited = new HashSet<int>();
    var queue = new Queue<(int node, int dist)>();
    queue.Enqueue((src, 0));
    visited.Add(src);
    
    while (queue.Count > 0)
    {
        var (node, dist) = queue.Dequeue();
        if (node == dst) return dist;
        
        foreach (int neighbor in graph[node])
        {
            if (!visited.Contains(neighbor))
            {
                visited.Add(neighbor);
                queue.Enqueue((neighbor, dist + 1));
            }
        }
    }
    return -1; // לא נמצא
}
```

---

## DFS — Cycle Detection ו-Connected Components

```csharp
// מציאת כל Connected Components
int CountComponents(int n, int[][] edges)
{
    var adj = new List<int>[n];
    for (int i = 0; i < n; i++) adj[i] = new List<int>();
    
    foreach (var edge in edges)
    {
        adj[edge[0]].Add(edge[1]);
        adj[edge[1]].Add(edge[0]);
    }
    
    var visited = new bool[n];
    int count = 0;
    
    for (int i = 0; i < n; i++)
    {
        if (!visited[i])
        {
            DFS(adj, visited, i);
            count++;
        }
    }
    return count;
}

void DFS(List<int>[] adj, bool[] visited, int node)
{
    visited[node] = true;
    foreach (int neighbor in adj[node])
        if (!visited[neighbor])
            DFS(adj, visited, neighbor);
}
```

---

## Topological Sort — Directed Acyclic Graph

```csharp
IList<int> TopologicalSort(int n, int[][] prerequisites)
{
    var inDegree = new int[n];
    var adj = new List<int>[n];
    for (int i = 0; i < n; i++) adj[i] = new List<int>();
    
    foreach (var pre in prerequisites)
    {
        adj[pre[1]].Add(pre[0]);
        inDegree[pre[0]]++;
    }
    
    var queue = new Queue<int>();
    for (int i = 0; i < n; i++)
        if (inDegree[i] == 0) queue.Enqueue(i);
    
    var order = new List<int>();
    while (queue.Count > 0)
    {
        int node = queue.Dequeue();
        order.Add(node);
        
        foreach (int next in adj[node])
            if (--inDegree[next] == 0)
                queue.Enqueue(next);
    }
    return order.Count == n ? order : new List<int>();
}
```

---

## Dijkstra — Shortest Weighted Path

```csharp
int[] Dijkstra(int[][] graph, int src)
{
    int n = graph.Length;
    var dist = new int[n];
    Array.Fill(dist, int.MaxValue);
    dist[src] = 0;
    
    // (distance, node)
    var pq = new PriorityQueue<(int dist, int node), int>();
    pq.Enqueue((0, src), 0);
    
    while (pq.Count > 0)
    {
        var (d, u) = pq.Dequeue();
        if (d > dist[u]) continue; // outdated
        
        for (int v = 0; v < n; v++)
        {
            if (graph[u][v] > 0)
            {
                int newDist = dist[u] + graph[u][v];
                if (newDist < dist[v])
                {
                    dist[v] = newDist;
                    pq.Enqueue((newDist, v), newDist);
                }
            }
        }
    }
    return dist; // O((V+E) log V)
}
```

---

## שאלות ראיון נפוצות

### שאלה 1: "BFS vs DFS — מתי כל אחד?"
**תשובה:**
- **BFS:** Shortest path, level traversal, מצא "קרוב ביותר"
- **DFS:** Cycle detection, Connected components, Topological sort

### שאלה 2: "מתי Dijkstra לא עובד?"
**תשובה:** כשיש **משקלים שליליים**. במקרה זה — Bellman-Ford.

---

## סיכום

| אלגוריתם | שימוש | סיבוכיות |
|----------|-------|----------|
| BFS | Shortest path (unweighted) | O(V+E) |
| DFS | Connectivity, cycles | O(V+E) |
| Dijkstra | Shortest path (weighted) | O((V+E)log V) |
| Topo Sort | Task scheduling, dependencies | O(V+E) |

---

*TechAI Explained | מסלול Algorithms | שיעור 8 מתוך 10*
