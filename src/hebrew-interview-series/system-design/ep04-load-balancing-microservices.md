# Load Balancing ומיקרושירותים

**מאת:** TechAI Explained Team

## מה נלמד בפרק הזה?
- כיצד Load Balancer מפזר תעבורה ואלגוריתמים נפוצים
- ההבדל בין Monolith למיקרושירותים — יתרונות וחסרונות
- תפקיד ה-API Gateway בארכיטקטורת מיקרושירותים

## שאלות ראיון נפוצות

### שאלה 1: מה זה Load Balancer ואיך הוא עובד?
**תשובה:**
Load Balancer הוא רכיב שמקבל בקשות נכנסות ומפזר אותן בין מספר שרתי backend. מטרתו למנוע עומס יתר על שרת בודד, לשפר זמינות ולאפשר horizontal scaling.

**שכבות Load Balancing:**
1. **L4 (Transport Layer)** — עובד על TCP/UDP, מהיר מאוד, מפזר לפי IP ו-port בלבד
2. **L7 (Application Layer)** — מבין HTTP, יכול לנתב לפי URL path, headers, cookies. גמיש יותר אך קצת איטי יותר

**אלגוריתמי פיזור נפוצים:**
- **Round Robin** — מחלק בקשות ברצף שווה בין השרתים. פשוט אך לא לוקח בחשבון עומס נוכחי
- **Weighted Round Robin** — כל שרת מקבל משקל לפי יכולת; שרתים חזקים יותר מקבלים יותר בקשות
- **Least Connections** — מנתב לשרת עם הכי פחות חיבורים פעילים. טוב כאשר הבקשות אורכות זמן שונה
- **IP Hash** — hash על ה-IP של הלקוח, מבטיח שאותו לקוח תמיד מגיע לאותו שרת (session affinity)

**Health Checks:** Load Balancer בודק תדיר האם שרתים תקינים ומסיר שרתים כושלים מהרוטציה.

**נקודות מפתח:**
- Load Balancer עצמו יכול להיות Single Point of Failure — משתמשים בזוג Active-Passive
- Sticky sessions מתאימות לאפליקציות stateful אך מגבילות scaling
- Health checks קריטיים לזיהוי ומסירת שרתים כושלים

---

### שאלה 2: מה ההבדל בין Monolith למיקרושירותים?
**תשובה:**
**Monolith (מונוליט):** כל לוגיקת האפליקציה ב-codebase אחד, שנבנה ו-deployed כיחידה אחת.

יתרונות:
- פשוט לפתח ולהריץ locally
- אין latency בין-שירותי (inter-service)
- Debugging קל יותר
- מתאים לצוותים קטנים ו-MVP

חסרונות:
- Scale כל הכלי גם כאשר רק חלק אחד עמוס
- Deployment של כל שינוי קטן מחייב build ו-deploy מלאים
- קוד נוטה להפוך לספגטי לאורך זמן
- טכנולוגיה אחת לכל הכלי

**Microservices (מיקרושירותים):** מפרקים את האפליקציה לשירותים קטנים ועצמאיים, כל אחד אחראי על domain ספציפי, deployed ו-scaled באופן עצמאי.

יתרונות:
- Scale עצמאי לכל שירות לפי עומסו
- Deployment עצמאי — אפשר לשחרר פיצ'ר ב-payment service מבלי לגעת ב-user service
- גמישות טכנולוגית — שירות שונה יכול להשתמש בשפה אחרת
- Fault isolation — כשל בשירות אחד לא הורס הכל

חסרונות:
- מורכבות תפעולית גבוהה (ניהול, monitoring, distributed tracing)
- Network latency בין שירותים
- Distributed transactions קשות
- דורש תרבות DevOps בשלה

**נקודות מפתח:**
- "Start with a monolith, break to microservices when needed"
- מיקרושירותים מתאימים לצוותים גדולים עם ניסיון DevOps
- הכלל: כל שירות צריך להיות קטן מספיק שיוכל לשכתב אותו תוך שבועיים

---

### שאלה 3: מה זה API Gateway ולמה הוא נחוץ?
**תשובה:**
API Gateway הוא שכבת ביניים בין הלקוחות (clients) לבין מיקרושירותי הbackend. הוא משמש כ-"single entry point" לכל הבקשות.

**תפקידי API Gateway:**
1. **Routing** — מנתב בקשות לשירות המתאים לפי URL path (/users → user service, /orders → order service)
2. **Authentication & Authorization** — בודק tokens ומרשה גישה בנקודה מרכזית, כך שכל שירות לא צריך לממש זאת
3. **Rate Limiting** — מגביל כמות בקשות מלקוח כדי למנוע שימוש לרעה
4. **Load Balancing** — יכול לפזר בקשות בין instances של אותו שירות
5. **SSL Termination** — מטפל ב-HTTPS ומעביר HTTP לשירותים הפנימיים
6. **Request Transformation** — ממיר formats, aggregates תגובות מכמה שירותים ל-response אחד (BFF pattern)
7. **Caching** — יכול לשמור תשובות נפוצות
8. **Observability** — logging, metrics, tracing מרכזי

**דוגמאות:** AWS API Gateway, Kong, Nginx, Traefik, Envoy

**BFF Pattern (Backend For Frontend):** יצירת API Gateway ספציפי לסוג לקוח — אחד ל-mobile, אחד ל-web — שמחזיר תשובות מותאמות לכל לקוח.

**נקודות מפתח:**
- API Gateway פותר cross-cutting concerns בנקודה מרכזית
- עלול להפוך ל-bottleneck — חשוב לוודא שהוא scalable
- Circuit breaker pattern מוסיף לו חוסן

---

### שאלה 4: מה זה Service Mesh?
**תשובה:**
Service Mesh הוא שכבת תשתית ייעודית לניהול תקשורת בין מיקרושירותים. בניגוד ל-API Gateway שמנהל תקשורת north-south (חיצוני→פנימי), service mesh מנהל תקשורת east-west (שירות→שירות).

**כיצד עובד:**
בכל pod/container מוסיפים sidecar proxy (בדרך כלל Envoy). ה-proxy מיירט את כל התקשורת הנכנסת והיוצאת ומטפל בה.

**יכולות Service Mesh:**
- **Traffic management** — A/B testing, canary deployments, circuit breaking
- **Security** — mTLS בין שירותים, authentication, authorization
- **Observability** — distributed tracing, metrics, logging אוטומטי
- **Retries & Timeouts** — ניהול automatic retries עם backoff

**דוגמאות:** Istio, Linkerd, Consul Connect

**מתי צריך Service Mesh:**
- עשרות מיקרושירותים שמתקשרים ביניהם
- צרכים ברורים ל-mutual TLS, fine-grained traffic control, ו-observability
- הצוות מסוגל לנהל את המורכבות הנוספת

**נקודות מפתח:**
- Service Mesh = "תשתית לניהול east-west traffic"
- מוסיף overhead אך מפחית boilerplate code בשירותים עצמם
- Kubernetes + Istio הוא combination נפוץ

---

### שאלה 5: כיצד מתמודדים עם Distributed Transactions במיקרושירותים?
**תשובה:**
בארכיטקטורת מיקרושירותים, כאשר פעולה אחת משפיעה על מספר שירותים (למשל: הזמנה שמורידה מלאי, גובה תשלום, ושולחת אימייל), לא ניתן להשתמש ב-ACID transaction רגיל.

**פתרונות:**

1. **Two-Phase Commit (2PC):**
Protocol שמבטיח שכולם מסכימים לבצע או לא לפני ביצוע. מורכב ויוצר blocking — לא מומלץ ב-microservices.

2. **Saga Pattern:**
פירוק ה-transaction למספר local transactions. אם שלב נכשל, מריצים compensating transactions כדי לבטל מה שכבר בוצע.
- **Choreography-based Saga:** כל שירות מגיב ל-events ושולח events. פשוט אך קשה לעקוב
- **Orchestration-based Saga:** orchestrator מרכזי מנהל את ה-flow. ברור יותר אך orchestrator הוא single point

3. **Eventual Consistency:**
מקבלים שהנתונים יהיו עקביים "בסוף" ולא מיד. המערכת מתוכננת לטפל ב-inconsistencies זמניות.

4. **Outbox Pattern:**
כתיבת ה-event לאותה database transaction כמו השינוי בנתונים, ואז transactional outbox processor שולח ל-message broker. מבטיח exactly-once publishing.

**נקודות מפתח:**
- 2PC לא מתאים ל-microservices בגלל blocking ומורכבות
- Saga Pattern הוא הגישה המומלצת
- Eventual consistency היא לא כישלון — זו תכונה מכוונת

## סיכום
Load balancing ומיקרושירותים הם אבני יסוד בארכיטקטורת מערכות מודרניות. Load balancer מאפשר scale אופקי ו-high availability. המעבר ממונוליט למיקרושירותים מביא יתרונות ברורים בצמיחה אך דורש הבנה מעמיקה של אתגרים כמו distributed transactions ו-observability. API Gateway הוא הנקודה המרכזית שמנהלת גישה לשירותים ופותר cross-cutting concerns.

## מקורות להמשך לימוד
- Microservices Patterns — Chris Richardson
- Building Microservices — Sam Newman
- NGINX Load Balancing Documentation
- Pattern: Saga (microservices.io)
