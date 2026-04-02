# אסטרטגיות Cache — Redis, CDN ואינוואלידציה

**מאת:** TechAI Explained Team

## מה נלמד בפרק הזה?
- כיצד caching משפר ביצועים ומפחית עומסים על מסד הנתונים
- ההבדל בין Redis, Memcached ו-CDN
- אסטרטגיות cache invalidation: write-through, write-back, write-around

## שאלות ראיון נפוצות

### שאלה 1: למה cache חשוב במערכות בקנה מידה גדול?
**תשובה:**
Cache הוא שכבת אחסון זמני מהיר שנמצאת בין האפליקציה למקור הנתונים המקורי (בדרך כלל מסד נתונים). המטרה היא להפחית latency ולהקל על מסד הנתונים.

**הסיבות לשימוש ב-cache:**
1. **מסד נתונים הוא צוואר הבקבוק** — disk I/O הרבה יותר איטי מ-in-memory access (100ms לעומת 0.1ms)
2. **הרבה נתונים נקראים פעמים רבות** — ה-80/20 rule: 80% מהבקשות מתמקדות ב-20% מהנתונים
3. **חישובים יקרים** — aggregations, report generation שניתן לחשב פעם ולשמור
4. **הגנה על downstream services** — מניעת מפולת בעת spike בתעבורה

**Cache Hit vs Cache Miss:**
- **Hit** — הנתון נמצא ב-cache, מוחזר מהר
- **Miss** — הנתון לא ב-cache, צריך לפנות למקור, זמן תגובה גבוה יותר
- **Hit Rate** — אחוז ה-hits מתוך כלל הבקשות; hit rate גבוה = cache אפקטיבי

**נקודות מפתח:**
- Cache יעיל לנתונים שנקראים הרבה ומשתנים לעתים רחוקות
- Hit rate של 80%+ נחשב טוב
- יש לחשוב על cache warm-up — מה קורה אחרי restart?

---

### שאלה 2: מה ההבדל בין Redis ל-Memcached?
**תשובה:**
שניהם הם in-memory data stores מהירים, אך יש הבדלים משמעותיים:

**Memcached:**
- פשוט יותר — רק key-value strings
- Multi-threaded — יכול לנצל מספר cores
- מתאים ל-simple caching use case
- לא תומך ב-persistence (נתונים אובדים בהפעלה מחדש)

**Redis:**
- תומך במבני נתונים עשירים: strings, hashes, lists, sets, sorted sets, streams
- תומך ב-persistence (RDB snapshots, AOF log)
- תומך ב-pub/sub messaging
- Replication ו-clustering מובנים
- Atomic operations
- מתאים ל-use cases מורכבים: leaderboards, rate limiting, session storage, distributed locks

**מתי לבחור מה:**
- Memcached: רק צריך simple string cache, יש הרבה traffic ו-multi-threading חשוב
- Redis: צריך מבני נתונים מורכבים, persistence, clustering, או use cases מעבר ל-simple cache

**נקודות מפתח:**
- Redis הוא הבחירה הנפוצה יותר כיום
- Redis יכול לשמש גם כ-primary database ל-use cases מסוימים
- שניהם in-memory = נתונים אובדים בהפעלה מחדש (אלא אם מגדירים persistence)

---

### שאלה 3: מה זה Cache Invalidation ולמה זה קשה?
**תשובה:**
Cache Invalidation הוא התהליך של הסרה או עדכון של נתונים ב-cache כאשר המקור המקורי משתנה. זהו אחד מהאתגרים הקשים ביותר בעיצוב מערכות.

**האתגר:** אם cache מחזיק נתונים ישנים (stale data), המשתמשים יראו מידע לא עדכני. אם מחדשים cache כל הזמן, מאבדים את היתרון שלו.

**גישות נפוצות:**
1. **TTL (Time to Live)** — כל פריט ב-cache מוגדר לפוג אחרי זמן מסוים. פשוט אך עלול לגרום ל-stale data עד ה-expiry
2. **Event-driven invalidation** — כשנתון משתנה ב-DB, נשלח event שמוחק/מעדכן ב-cache. עדכני יותר אך מורכב
3. **Write-through** — כתיבה מתרחשת גם ב-cache וגם ב-DB. Cache תמיד עדכני אך כתיבות איטיות יותר
4. **Cache-aside (Lazy Loading)** — האפליקציה בודקת cache, אם miss קוראת מ-DB ומכניסה ל-cache. פשוט אך cache יכול להיות ריק בהתחלה

**Cache stampede (Thundering Herd):** כאשר cache item פג ובאותו רגע הרבה requests מגיעים, כולם מנסים לרנדר את הנתון מ-DB בו-זמנית. פתרון: probabilistic early expiration, distributed locking.

**נקודות מפתח:**
- "There are only two hard things in CS: cache invalidation and naming things"
- TTL פשוט אך לא מתאים לנתונים קריטיים
- Write-through מבטיח עקביות אך מוסיף latency לכתיבות

---

### שאלה 4: מה ההבדל בין Write-Through ל-Write-Back Cache?
**תשובה:**
**Write-Through Cache:**
כאשר נכתב נתון, הוא נכתב גם ל-cache וגם ל-database באותה פעולה. הקריאה הבאה תמצא את הנתון העדכני ב-cache.

יתרונות: cache תמיד עדכני, אין אובדן נתונים
חסרונות: כל כתיבה כרוכה בשתי פעולות (cache + DB) = latency גבוה יותר לכתיבות

**Write-Back (Write-Behind) Cache:**
כאשר נכתב נתון, הוא נכתב תחילה ל-cache בלבד ומסומן כ"dirty". הכתיבה ל-DB מתרחשת מאוחר יותר, בצורה async.

יתרונות: כתיבות מהירות מאוד (רק ל-memory), ניתן לאגד כתיבות ל-DB (write batching)
חסרונות: אם cache node נכשל לפני שהנתון נכתב ל-DB, הנתון אובד!

**Write-Around:**
כתיבה הולכת ישירות ל-DB, עוקפת את ה-cache. מתאים לנתונים שנכתבים פעם אחת ואינם נקראים מיד.

**מתי להשתמש:**
- Write-Through: כשעקביות קריטית (פיננסים, הזמנות)
- Write-Back: כשביצועי כתיבה קריטיים ויש סבילות לאובדן נתונים קטן (logging, analytics)

**נקודות מפתח:**
- Write-Through = עקביות, Write-Back = ביצועים
- Write-Back מסוכן בלי persistence ל-cache
- הבחירה תלויה בדרישות consistency ו-performance

---

### שאלה 5: מה זה CDN ואיך זה עובד?
**תשובה:**
CDN (Content Delivery Network) הוא רשת של שרתים גיאוגרפית מפוזרת שמשרתת תוכן סטטי ודינמי למשתמשים מהשרת הקרוב אליהם ביותר.

**כיצד CDN עובד:**
1. משתמש מבקש resource (תמונה, CSS, JS)
2. DNS מפנה לשרת CDN הקרוב ביותר (PoP — Point of Presence)
3. אם הקובץ קיים ב-CDN cache (cache hit) — מוחזר מיד
4. אם לא (cache miss) — CDN מביא מה-origin server, שומר ב-cache, ומחזיר למשתמש

**מה מטמינים ב-CDN:**
- Static assets: images, CSS, JavaScript, videos
- HTML דפים (עם TTL מתאים)
- API responses שלא משתנים תדיר

**יתרונות CDN:**
- Reduced latency — תוכן מגיע ממיקום גיאוגרפי קרוב
- DDoS protection — מסנן traffic זדוני
- מפחית עומס על origin server
- Cost savings — bandwidth זולה יותר דרך CDN

**שחקנים עיקריים:** CloudFront (AWS), Cloudflare, Akamai, Fastly

**נקודות מפתח:**
- CDN = cache גיאוגרפי לתוכן סטטי
- יש לשים לב ל-cache invalidation בעת deploy חדש (cache busting)
- CDN יכול גם לשפר security (WAF, DDoS protection)

## סיכום
Caching הוא אחד מהכלים החשובים ביותר לשיפור ביצועים ומדרגיות. הבנת ה-trade-offs בין consistency לביצועים, ובחירת אסטרטגיית cache invalidation נכונה, הם מפתח לעיצוב מערכות בריאות. Redis הוא הכלי הנפוץ ביותר לאפליקציה-level cache, וCDN לתוכן סטטי. בראיון, הראה שאתה מבין מה cache מתאים לאחסן ומה לא, ואיך להתמודד עם stale data.

## מקורות להמשך לימוד
- Redis Documentation (redis.io)
- AWS ElastiCache Developer Guide
- Cloudflare Learning — CDN
- Designing Data-Intensive Applications — Chapter 5
