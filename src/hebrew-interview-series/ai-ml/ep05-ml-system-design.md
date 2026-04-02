# עיצוב מערכות ML — Feature Stores, Model Serving ו-A/B Testing

**מאת:** TechAI Explained Team

## מה נלמד בפרק הזה?
- ארכיטקטורת ML system: מ-data collection ועד production
- Feature stores ומדוע הם קריטיים לאחידות features
- A/B testing ו-shadow mode לפריסה בטוחה של מודלים

## שאלות ראיון נפוצות

### שאלה 1: מה זה ML System Design ומה הוא כולל?
**תשובה:**
ML System Design הוא תכנון כלל המערכת שמאפשרת ל-ML model לפעול ב-production, כולל איסוף נתונים, אימון, הגשת תחזיות, ניטור ועוד.

**רכיבי ML System:**

1. **Data Collection & Storage:**
   - Raw data מגיע ממקורות שונים (logs, events, APIs)
   - Data Lake לאחסון גולמי (S3, GCS)
   - Data Warehouse לנתונים מעובדים (BigQuery, Snowflake)

2. **Feature Engineering:**
   - Feature pipeline: עיבוד נתונים גולמיים ל-features מוכנים לאימון
   - Feature Store לשיתוף ועקביות features

3. **Model Training:**
   - Training pipeline: נתונים → model artifacts
   - Experiment tracking (MLflow, W&B)
   - Hyperparameter tuning

4. **Model Registry:**
   - גרסאות מודלים, metadata, lineage
   - MLflow Model Registry, Weights & Biases

5. **Model Serving:**
   - Online (real-time): REST/gRPC API
   - Batch: עיבוד מסיבי תקופתי
   - Edge: הרצה על device

6. **Monitoring:**
   - Data drift, model performance degradation
   - Alerting, retraining triggers

**נקודות מפתח:**
- ML system הוא הרבה יותר מהמודל עצמו — 80%+ מהעבודה היא infrastructure
- Google's ML Technical Debt paper: "hidden technical debt in ML systems"
- MLOps = DevOps ל-ML systems

---

### שאלה 2: מה זה Feature Store ולמה הוא חשוב?
**תשובה:**
Feature Store הוא מערכת מרכזית לניהול, אחסון ושיתוף features בין מודלים שונים.

**הבעיה שהוא פותר:**
בלי feature store, כל data scientist מכין features בנפרד. מביא לבעיות:
- **Training-Serving Skew:** features מחושבים אחרת ב-training מאשר ב-serving → drops in performance
- **Feature duplication:** 5 צוותים מחשבים "user activity in last 7 days" בדרכים שונות
- **Latency:** חישוב features on-the-fly ב-real-time inference יכול להיות איטי
- **Data leakage:** שימוש בנתוני עתיד באימון בשוגג

**ארכיטקטורת Feature Store:**

**Offline Store:**
- לאימון: snapshots היסטוריים של features
- בדרך כלל: Parquet files ב-S3, Delta Lake, BigQuery
- Point-in-time correct retrieval — חשוב למנוע data leakage

**Online Store:**
- ל-inference ב-real-time: low-latency feature lookup
- בדרך כלל: Redis, DynamoDB, Cassandra
- Feature values נכתבים מה-offline store ב-materialization process

**Feature Pipeline:**
עיבוד נתונים גולמיים ל-features → אחסון ב-offline ו-online store

**דוגמאות Feature Stores:** Feast (open-source), Tecton, Hopsworks, Vertex AI Feature Store

**נקודות מפתח:**
- Feature Store = consistency בין training לserving
- Online + Offline = שתי מטרות שונות (latency vs history)
- Point-in-time correctness חיונית למניעת data leakage

---

### שאלה 3: מהם דרכי ה-Model Serving השונות?
**תשובה:**
**Online Serving (Real-time Inference):**
- Model כ-REST/gRPC API, מגיב לבקשות בodot real-time
- Latency requirements: 10-100ms
- שיקולים: autoscaling, hardware (GPU vs CPU), caching

**Batch Serving:**
- הרצת מודל על קבוצות גדולות של נתונים בתזמון תקופתי
- Latency לא קריטי (שעות)
- Use cases: daily recommendations, risk scoring, churn prediction
- כלים: Spark, Beam, AWS Batch

**Streaming Serving:**
- Inference על data stream (Kafka, Kinesis) בזמן אמת
- Use cases: fraud detection, real-time recommendations
- כלים: Flink, Kafka Streams

**Edge Serving:**
- הרצת מודל על device (מובייל, IoT) ללא שרת
- מצריך model compression: quantization, pruning, distillation
- שיקול: privacy (נתונים לא עוזבים ה-device), low latency, offline capability
- כלים: TensorFlow Lite, Core ML, ONNX Runtime

**Serving Infrastructure:**
- **TensorFlow Serving:** ייעודי ל-TF models, gRPC + REST
- **Torchserve:** ל-PyTorch
- **Triton Inference Server (NVIDIA):** רב-framework, GPU optimization
- **Ray Serve:** Python-native, distributed
- **KServe:** Kubernetes-native ML serving

**Model Optimization לatency:**
- Quantization: FP32 → INT8 → מהיר יותר, קצת פחות דיוק
- Distillation: מודל גדול מלמד מודל קטן
- ONNX: export לformat universal

**נקודות מפתח:**
- Online vs Batch → tradeoff latency vs cost
- GPU serving יקר — בדוק אם CPU מספיק (טרנספורמרים קטנים)
- Model versioning ב-serving חשובה להצגת גרסאות שונות במקביל

---

### שאלה 4: כיצד מבצעים A/B Testing למודלי ML?
**תשובה:**
A/B Testing ב-ML הוא שיטה לבדיקה אמפירית האם מודל חדש טוב יותר ממה שקיים ב-production.

**מדוע A/B ולא offline evaluation?**
Offline metrics (AUC, RMSE) לא תמיד מתורגמות ל-business metrics. מודל שמשפר CTR ב-offline יכול להשפיע שלילית על retention. A/B testing מודד impact אמיתי.

**ה-setup:**
- **Control (A):** המודל הנוכחי (baseline)
- **Treatment (B):** המודל החדש
- מחלקים users אקראית: 90% קבלו A, 10% קבלו B
- מודדים business metrics: conversion, engagement, revenue

**שיקולים חשובים:**
1. **Sample Size:** חישוב הספק סטטיסטי לפני תחילת הניסוי — כמה users צריך לראות הbehavior?
2. **Duration:** הניסוי צריך לרוץ מספיק זמן לללכוד weekly patterns
3. **Novelty Effect:** users אוהבים דברים חדשים — מצב זמני שעשוי להיראות כהצלחה
4. **Network Effects:** אם A ו-B משפיעים זה על זה (social network) — isolation קשה
5. **Multiple Metrics:** הגדר primary metric ו-guardrail metrics (לא להשפיע לרעה)

**Shadow Mode (Shadow Testing):**
- המודל החדש רץ במקביל למודל הישן
- ה-serving מבוסס על המודל הישן בלבד
- הפלטים של המודל החדש מתועדים להשוואה בלבד
- **יתרון:** אין risk לusers, אפשר לבדוק latency, errors

**Canary Deployment:**
- 1-5% מה-traffic הולך למודל החדש
- מזהים בעיות לפני rollout מלא
- מוגדר thresholds לrollback אוטומטי

**Multi-armed Bandit:**
במקום split סטטי, allocate traffic דינמי לפי performance — variant טוב יותר מקבל יותר traffic.
יתרון: מינימום regret. חסרון: מורכב יותר לניתוח.

**נקודות מפתח:**
- A/B testing חיוני לvalidate שיפור offline metrics = שיפור real-world
- תמיד חשב sample size לפני תחילת הניסוי
- Shadow mode ל-risky models; canary ל-gradual rollout

---

### שאלה 5: כיצד מזהים ומתמודדים עם Model Drift?
**תשובה:**
Model Drift הוא תופעה שבה ביצועי המודל ב-production מתדרדרים לאורך זמן. יש שני סוגים עיקריים:

**Data Drift:**
התפלגות נתוני הקלט משתנה ביחס לנתוני האימון.
- דוגמה: מודל credit scoring שאומן ב-2019 — patterns של התנהגות כלכלית השתנו אחרי COVID
- זיהוי: Statistical tests (Kolmogorov-Smirnov, Jensen-Shannon divergence) על feature distributions

**Concept Drift:**
הקשר בין features ל-target משתנה.
- דוגמה: מודל spam detection — spammers מסתגלים לפילטרים
- קשה יותר לזיהוי כי דורש labels עדכניים

**Monitoring בpractice:**

1. **Input Monitoring:** מדד statistics של features (mean, std, distribution) ובדוק drift מהנתונים ההיסטוריים

2. **Prediction Monitoring:** מדד distribution של פלטי המודל — שינוי פתאומי ב-prediction distribution = red flag

3. **Performance Monitoring:** אם יש labels מוגדרים (feedback loop), עקוב אחרי metrics בזמן אמת

4. **Alerting:** הגדר thresholds, alert כאשר עוברים אותם

**כלים:** Evidently AI, WhyLabs, Arize, Datadog ML

**Retraining Strategies:**
- **Scheduled:** אחזור תקופתי (weekly, monthly)
- **Triggered:** כשpearformance מתחת ל-threshold
- **Continuous:** pipeline שמוסיף נתונים חדשים לאימון כל הזמן

**נקודות מפתח:**
- Monitoring הוא לא אופציה ב-production ML
- Data drift קל יותר לזיהוי מ-concept drift
- Feedback loop חיוני: ניתן לאמן מחדש רק אם יש labels עדכניים

## סיכום
ML System Design הוא הפגישה בין data science להנדסת תוכנה בסדר גודל גדול. Feature stores, model serving, A/B testing ו-drift monitoring הם ה-building blocks של כל ML system production-grade. בראיון, הראה שאתה מבין שמודל הוא רק 20% מהעבודה — ה-80% הנשאר הוא infrastructure, pipelines ו-monitoring.

## מקורות להמשך לימוד
- Designing Machine Learning Systems — Chip Huyen
- Machine Learning Engineering — Andriy Burkov
- MLOps Guide — Google Cloud
- Made With ML (madewithml.com)
