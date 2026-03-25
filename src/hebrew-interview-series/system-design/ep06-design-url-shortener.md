# עיצוב מערכת: URL Shortener

**מאת:** TechAI Explained Team

## מה נלמד בפרק הזה?
- כיצד לגשת לשאלת עיצוב מערכות מקצה לקצה בראיון
- עיצוב מלא של URL Shortener — שאלה קלאסית ונפוצה
- שיקולי scale, בחירת database, ושיקולי availability

## שאלות ראיון נפוצות

### שאלה 1: כיצד תתחיל לגשת לשאלה "עצב URL shortener"?
**תשובה:**
שלב ראשון: **הגדרת דרישות** (לא להתחיל לתכנן לפני כן!)

**דרישות פונקציונליות:**
- קבלת URL ארוך ויצירת קישור קצר ייחודי
- הפניה (redirect) מהקישור הקצר לארוך
- (אופציונלי) קישורים מותאמים אישית (custom aliases)
- (אופציונלי) תאריך תפוגה לקישורים
- (אופציונלי) analytics — כמה קליקים לכל קישור

**דרישות לא-פונקציונליות:**
- המערכת צריכה לטפל ב-100M קישורים ביום
- Redirect latency נמוך מ-10ms
- High Availability — 99.9% uptime
- Durability — קישורים לא אובדים

**אמידת Scale:**
- 100M URLs ביום = ~1,200 writes לשנייה
- Read/Write ratio נפוץ: 100:1 → ~120,000 reads לשנייה (redirects)
- Storage: URL ממוצע = 200 bytes, 100M ביום × 365 ימים × 5 שנים = ~36TB

**נקודות מפתח:**
- שאל שאלות ברורות לפני שמתחיל לתכנן
- אמוד scale בערכים בגסות — לא צריך דיוק מלא
- הגדר priorities: read-heavy? write-heavy? latency? consistency?

---

### שאלה 2: כיצד יוצרים short code ייחודי?
**תשובה:**
ה-short code (כמו `bit.ly/abc123`) צריך להיות קצר, ייחודי וגנרבל מהר.

**שיטה 1: Hash + Truncation**
לקחת MD5 או SHA-256 של ה-URL הארוך, ולקחת את 6-8 התווים הראשונים.
- MD5("https://example.com/very-long") → "a7f3bc..."
- Short code: "a7f3bc"

בעיה: collision אפשרי (שני URLs שונים → אותו hash). פתרון: במקרה של collision, הוסף מספר נקוב ונסה שוב.

**שיטה 2: Base62 Encoding על Auto-Increment ID**
- DB מייצר auto-increment ID: 12345
- מקודדים ל-Base62 (a-z, A-Z, 0-9): 12345 → "3D7"
- יתרון: אין collisions, קצר
- חסרון: IDs ניתנים לניחוש (predictable) — security concern

**שיטה 3: Random Unique Identifier**
- גנרציה random של 6-8 תווים מ-Base62
- בדיקה שהקוד לא קיים כבר ב-DB
- יתרון: לא ניתן לניחוש
- חסרון: בדיקת uniqueness מול DB לכל כתיבה

**שיטה מומלצת:** Base62 על counter מרכזי + distributed ID generator (כמו Snowflake) לסקלאביליות.

**נקודות מפתח:**
- 6 תווים ב-Base62 = 62^6 = ~56 מיליארד קומבינציות
- Hash approach פשוט אך דורש collision handling
- Distributed ID generation (Twitter Snowflake, Flickr Ticket Server) מאפשר scale

---

### שאלה 3: איזה Database תבחר ולמה?
**תשובה:**
נבחן את האפשרויות לפי דרישות המערכת:

**ניתוח דרישות:**
- Write: ~1,200/sec (כתיבת URLs)
- Read: ~120,000/sec (redirects)
- Data structure: key-value פשוט (short_code → long_url)
- Durability: כן, קישורים לא צריכים לאבד
- Consistency: eventual consistency מספיקה (אם redirect לוקח כמה שניות להיות זמין — בסדר)

**אפשרויות:**

1. **SQL (PostgreSQL/MySQL):**
   - יכול לעבוד, אך 120K reads/sec זה הרבה לשרת יחיד
   - דורש sharding ו-read replicas
   - מתאים אם צריך analytics מורכב

2. **NoSQL Key-Value (DynamoDB, Cassandra):**
   - מצוין ל-read-heavy workloads
   - Scale אופקי קל
   - DynamoDB: single-digit ms latency
   - Cassandra: excellent write throughput

3. **Redis (כ-Cache לפני DB):**
   - Cache tier ל-hot links: short_code → long_url
   - Expected cache hit rate: 80%+
   - משלים DynamoDB/MySQL — לא מחליף

**ארכיטקטורה מומלצת:**
Redis cache (ל-hot links) → DynamoDB/Cassandra (primary storage)

אם short code נמצא ב-Redis — redirect מיידי (< 1ms). אם לא — שליפה מ-DB, cache ב-Redis, redirect.

**נקודות מפתח:**
- Use case זה read-heavy, לכן cache קריטי
- NoSQL מועדף על SQL ל-simple key-value lookup בscale גדול
- אל תשכח לציין Redis cache כחלק מהארכיטקטורה

---

### שאלה 4: כיצד מיישמים Redirect?
**תשובה:**
כאשר משתמש לוחץ על `bit.ly/abc123`, הדפדפן שולח HTTP GET request ל-`bit.ly/abc123`.

**HTTP Redirect Codes:**
1. **301 Moved Permanently** — מצביע שה-URL השתנה לצמיתות. הדפדפן מאחסן את ה-redirect ב-cache ולא שולח שוב לשרת שלך!
   - יתרון: פחות עומס על שרת
   - חסרון: לא ניתן לאסוף analytics קליקים (הדפדפן redirect בלי להגיע אלינו)

2. **302 Found (Temporary Redirect)** — הדפדפן לא מאחסן ב-cache, שולח בקשה לשרת בכל פעם.
   - יתרון: ניתן לאסוף analytics, לשנות destination בעתיד
   - חסרון: יותר load על שרת

**המלצה:** אם analytics חשוב — 302. אם רוצים לחסוך load — 301.

**Flow מלא:**
1. User → GET bit.ly/abc123
2. שרת בודק Redis cache
3. אם miss → שולף מ-DynamoDB
4. מעדכן cache (אם miss)
5. מחזיר 302 redirect עם Location: https://original-url.com
6. (Async) מעדכן analytics counter

**נקודות מפתח:**
- 301 vs 302 trade-off: performance vs analytics
- ה-redirect logic צריך להיות מהיר מאוד — זה ה-hot path
- לוגיקת analytics כדאי לעשות async כדי לא לפגוע ב-redirect latency

---

### שאלה 5: כיצד תבנה את ה-Analytics?
**תשובה:**
Analytics ל-URL shortener כולל מעקב על: כמה קליקים, מאיזה browser/device, מאיזה גיאוגרפיה, לאורך זמן.

**האתגר:** ב-120K redirects/sec, לא ניתן לכתוב record ל-SQL DB בכל קליק.

**ארכיטקטורת Analytics:**

1. **Async Event Streaming:**
   - בכל redirect, שולחים event ל-Kafka: `{short_code, timestamp, user_agent, ip}`
   - Redirect ממשיך מיידית — לא מחכה לכתיבת ה-event
   - Kafka consumers מעבדים events async

2. **Consumer Processing:**
   - Consumer קורא מ-Kafka
   - מקבץ events (batching) לחיסכון בכתיבות
   - כותב ל-analytics DB כל X שניות

3. **Analytics Database:**
   - ClickHouse, Apache Druid, BigQuery — column-store DBs מעולות ל-analytics
   - אפשרות פשוטה יותר: Redis counters לstatistics בסיסיות (INCR)

4. **Real-time Dashboard:**
   - Redis sorted sets ל-trending links
   - Aggregated stats ב-column-store ל-historical analysis

**API Analytics:**
- `GET /api/stats/abc123` → מחזיר: total clicks, clicks per day, top countries, top browsers

**נקודות מפתח:**
- Analytics תמיד async — אל תפגע ב-redirect latency
- Kafka + column-store DB הוא pipeline נפוץ ל-click analytics
- Redis counters מתאימים ל-real-time simple stats

## סיכום
URL Shortener הוא תרגיל קלאסי לראיון שמאחד הרבה נושאים: URL encoding, caching, database selection, redirect mechanics, ו-analytics. המפתח הוא גישה מובנית: קודם דרישות, אחר כך scale estimation, אז הארכיטקטורה, ואז צלילה לרכיבים ספציפיים. ארכיטקטורה טובה: Web servers → Redis cache → NoSQL DB לקריאות מהירות, Kafka → Analytics DB לאנליטיקה async.

## מקורות להמשך לימוד
- System Design Interview Vol. 1 — Alex Xu (Chapter: URL Shortener)
- ByteByteGo — URL Shortener Design
- bit.ly Engineering Blog
- TinyURL Technical Blog
