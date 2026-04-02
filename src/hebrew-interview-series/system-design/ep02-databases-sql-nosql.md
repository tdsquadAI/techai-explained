# מסדי נתונים — SQL vs NoSQL

**מאת:** TechAI Explained Team

## מה נלמד בפרק הזה?
- ההבדלים היסודיים בין SQL ל-NoSQL ומתי לבחור כל אחד
- אסטרטגיות sharding ו-replication לסקלאביליות
- טכניקות אינדוקס וכיצד הן משפרות ביצועים

## שאלות ראיון נפוצות

### שאלה 1: מה ההבדל העיקרי בין SQL ל-NoSQL?
**תשובה:**
**SQL (Relational Databases)** כגון MySQL, PostgreSQL ו-SQL Server, מאחסנים נתונים בטבלאות עם schema מוגדר מראש. הם מספקים ACID transactions (Atomicity, Consistency, Isolation, Durability) ותומכים ב-JOIN מורכבים. מתאימים לנתונים מובנים עם קשרים ברורים.

**NoSQL** כוללת מספר סוגים:
- **Document stores** (MongoDB, CouchDB) — מאחסנים JSON documents, גמישים ב-schema
- **Key-Value stores** (Redis, DynamoDB) — מהירים ביותר לגישה לפי מפתח
- **Column-family** (Cassandra, HBase) — מתאים לכמויות נתונים ענקיות עם כתיבות כבדות
- **Graph databases** (Neo4j) — מתאים לנתונים בעלי קשרים מורכבים (רשתות חברתיות)

NoSQL בדרך כלל מאפשר scale אופקי קל יותר, אך לרוב מוותר על עקביות מלאה לטובת זמינות וביצועים.

**נקודות מפתח:**
- SQL: schema נוקשה, ACID, מתאים לנתונים מובנים
- NoSQL: schema גמיש, BASE, מתאים ל-scale גדול
- הבחירה תלויה בדרישות העסקיות ובטיב הנתונים

---

### שאלה 2: מתי תבחר NoSQL על פני SQL?
**תשובה:**
תבחר NoSQL כאשר:

1. **Scale ענק** — צריך לאחסן ולקרוא מיליארדי רשומות (Cassandra עובד טוב עם petabytes של נתונים)
2. **Schema לא ידוע מראש** — המבנה משתנה תדיר, כמו catalog של מוצרים עם תכונות שונות
3. **כתיבות כבדות** — מערכת כמו log aggregation שמקבלת מיליוני events לשנייה
4. **Latency נמוך מאוד** — Redis כ-cache מחזיר תשובות ב-sub-millisecond
5. **נתוני גרף** — רשתות חברתיות, recommendation engines

תבחר SQL כאשר:
1. הנתונים מובנים עם קשרים מורכבים וצריך JOINs
2. נדרשת עקביות חזקה ו-ACID transactions (בנקאות, הזמנות)
3. הצוות מכיר SQL ויש legacy code שמשתמש בו

בפועל, רוב המערכות הגדולות משתמשות בשני הסוגים — SQL לנתוני ה-core ו-NoSQL ל-cache, sessions, logs.

**נקודות מפתח:**
- NoSQL ≠ תמיד יותר טוב — יש trade-offs ברורים
- שימוש משולב (polyglot persistence) הוא גישה נפוצה
- תמיד שאל: מה דרישות ה-consistency? מה ה-scale?

---

### שאלה 3: מה זה Database Sharding ואיך זה עובד?
**תשובה:**
Sharding הוא שיטה לפיצול אופקי של מסד נתונים — במקום לשמור את כל הנתונים בשרת אחד, מפצלים אותם למספר שרדים (shards), כל אחד מחזיק חלק מהנתונים.

**שיטות Sharding נפוצות:**
1. **Hash-based sharding** — מחשבים hash על ה-key ומחלקים לפי תוצאה. פיזור טוב אך קשה לשינוי מספר ה-shards
2. **Range-based sharding** — מחלקים לפי טווח ערכים (למשל: user_id 1-1M בshard א', 1M-2M בshard ב'). פשוט אך עלול לגרום לעומסים לא שווים (hotspots)
3. **Directory-based sharding** — lookup table שמצביעה לאיזה shard שייכת כל רשומה. גמיש אך מוסיף latency

**אתגרי Sharding:**
- Cross-shard queries קשות ויקרות
- Rebalancing כאשר מוסיפים shards
- נדרש application-level sharding logic

**נקודות מפתח:**
- Sharding פותר בעיות scale אך מוסיף מורכבות
- יש להימנע מ-hotspots בבחירת shard key
- Consistent hashing מפחית rebalancing עם הוספת nodes

---

### שאלה 4: מה ההבדל בין Database Indexes לבין Full Table Scan?
**תשובה:**
**Full Table Scan** — מסד הנתונים קורא כל שורה בטבלה כדי למצוא התאמות. סיבוכיות O(n). מקובל לטבלאות קטנות, אך הורס ביצועים בטבלאות של מיליוני שורות.

**Index** — מבנה נתונים נוסף (בדרך כלל B-Tree) שמאחסן את ערכי העמודה יחד עם הצבעה לשורה המקורית. מאפשר חיפוש ב-O(log n) במקום O(n).

**סוגי Indexes:**
- **B-Tree Index** — הנפוץ ביותר, מתאים לחיפוש על טווחים ושיוויון
- **Hash Index** — מהיר לחיפוש שיוויון בלבד, לא תומך ב-range queries
- **Composite Index** — על מספר עמודות, חשוב לשים לב לסדר העמודות
- **Covering Index** — Index שמכסה את כל העמודות שהשאילתה צריכה, נמנע מגישה לטבלה עצמה

**מתי לא להוסיף Index:**
- על עמודות עם cardinality נמוך (כמו gender)
- על טבלאות שרובן כתיבות — כל כתיבה מעדכנת את ה-index
- יותר מדי indexes מאטים INSERT/UPDATE/DELETE

**נקודות מפתח:**
- Index מאיץ קריאות אך מאט כתיבות
- יש לזהות את השאילתות הכבדות (slow query log) לפני הוספת indexes
- Explain/Query Plan הוא הכלי לבדיקת שימוש ב-index

---

### שאלה 5: מה זה Database Replication ולמה זה חשוב?
**תשובה:**
Replication הוא תהליך של שמירת עותקים של מסד הנתונים במספר שרתים סימולטנית.

**מודלים עיקריים:**
1. **Master-Slave (Primary-Replica)** — כל הכתיבות הולכות ל-primary, הקריאות מתפזרות בין ה-replicas. פשוט אך Primary הוא single point of failure
2. **Master-Master** — שני שרתים מקבלים כתיבות. מורכב יותר, מצריך conflict resolution
3. **Synchronous Replication** — Primary מאשר כתיבה רק אחרי ש-replica אישר. מבטיח עקביות אך מוסיף latency
4. **Asynchronous Replication** — Primary מאשר מיד, replica מתעדכן בהמשך. מהיר יותר אך ייתכן אובדן נתונים בכשל

**יתרונות Replication:**
- High Availability — אם Primary נכשל, אפשר לעשות failover ל-replica
- Read Scaling — ניתן לפזר קריאות בין replicas
- Geographic distribution — replica קרוב יותר לגיאוגרפיה של המשתמשים

**נקודות מפתח:**
- Replication != Backup (שניהם צריכים להיות)
- Replication lag הוא בעיה ב-async replication
- Multi-region replication מורכבת אך קריטית למערכות גלובליות

## סיכום
הבחירה בין SQL ל-NoSQL תלויה בדרישות המערכת — אין פתרון "תמיד נכון". שאלות על databases בראיון בוחנות הבנת trade-offs: consistency מול availability, read performance מול write performance, schema flexibility מול data integrity. Sharding ו-replication הן כלים חיוניים לסקלאביליות, ו-indexing הוא אחד מהכלים החשובים ביותר לאופטימיזציה של ביצועים.

## מקורות להמשך לימוד
- Designing Data-Intensive Applications — Martin Kleppmann
- Use The Index, Luke (use-the-index-luke.com)
- MongoDB Documentation — Data Modeling
- PostgreSQL Documentation — Indexes
