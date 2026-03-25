# יסודות Machine Learning לראיון

**מאת:** TechAI Explained Team

## מה נלמד בפרק הזה?
- ההבדל בין Supervised, Unsupervised ו-Reinforcement Learning
- ה-Bias/Variance Tradeoff — אחד המושגים הנפוצים ביותר בראיונות ML
- מדדי הערכה נפוצים ומתי להשתמש בכל אחד

## שאלות ראיון נפוצות

### שאלה 1: מה ההבדל בין Supervised ל-Unsupervised Learning?
**תשובה:**
**Supervised Learning (למידה מפוקחת):**
האלגוריתם לומד מנתוני אימון עם תוויות (labels) — כל דוגמה כוללת input ו-output ידוע. המטרה: ללמוד פונקציה שממפה inputs ל-outputs, ולהשתמש בה על נתונים חדשים שהתשובה עליהם לא ידועה.

דוגמאות: סיווג אימיילים ל-spam/לא spam, חיזוי מחיר בית, זיהוי תמונות, תרגום שפות.

**Unsupervised Learning (למידה בלתי מפוקחת):**
האלגוריתם לומד מנתונים ללא תוויות — מחפש patterns ומבנה נסתר בנתונים.

דוגמאות: Clustering לקוחות לפי התנהגות (K-Means), Dimensionality Reduction (PCA), Anomaly Detection, Topic Modeling.

**Semi-Supervised Learning:** שילוב — מעט נתונים עם תוויות והרבה ללא תוויות. שימושי כאשר תיוג נתונים יקר.

**Self-Supervised Learning:** המודל מייצר labels מהנתונים עצמם (למשל: LLMs שמנבאים את המילה הבאה).

**Reinforcement Learning:** סוכן לומד ע"י ניסוי-ושגיאה — מקבל reward על פעולות טובות ו-penalty על גרועות. שימוש: משחקים, רובוטיקה, RLHF ב-LLMs.

**נקודות מפתח:**
- Supervised = labels ידועים; Unsupervised = חיפוש patterns ללא labels
- הבחירה תלויה בזמינות נתונים מתויגים ובמטרה
- Modern LLMs משתמשים ב-self-supervised + RLHF

---

### שאלה 2: מה זה Bias-Variance Tradeoff?
**תשובה:**
זהו אחד המושגים היסודיים ביותר ב-ML. שגיאת מודל ניתנת לפירוק לשלושה רכיבים: Bias, Variance ו-Irreducible Noise.

**Bias (הטיה):**
הטעות שנובעת מהנחות מוטעות באלגוריתם. מודל עם bias גבוה מפשט יתר על המידה את הבעיה.
- תסמין: **Underfitting** — ביצועים גרועים גם על אימון וגם על validation
- דוגמה: ניסיון לפתור בעיה לא לינארית עם מודל לינארי

**Variance (שונות):**
רגישות גבוהה לתנודות בנתוני אימון. מודל עם variance גבוה "שינן" את נתוני האימון ולא למד דפוס כללי.
- תסמין: **Overfitting** — ביצועים מעולים על אימון אך גרועים על validation
- דוגמה: decision tree עמוק מאוד שזוכר כל דוגמה

**ה-Tradeoff:**
הפחתת bias (בדרך כלל ע"י מודלים מורכבים יותר) מגדילה variance ולהיפך. יש למצוא את האיזון הנכון.

**כיצד מתמודדים:**
- Underfitting: הגדל מורכבות המודל, הוסף features, הפחת regularization
- Overfitting: הוסף regularization (L1/L2), Dropout, Early Stopping, Cross-Validation, הוסף נתונים

**נקודות מפתח:**
- Bias גבוה = מודל פשוט מדי (underfitting)
- Variance גבוה = מודל מורכב מדי (overfitting)
- Cross-validation עוזרת לזהות ולאזן את ה-tradeoff

---

### שאלה 3: מה ההבדל בין Classification ל-Regression?
**תשובה:**
שניהם supervised learning, אך הoutput שונה:

**Classification (סיווג):**
המודל מנבא קטגוריה דיסקרטית. Output הוא מחלקה מתוך סט מוגדר.
- Binary: spam/לא spam, חולה/בריא
- Multi-class: סיווג 1 מ-10 ספרות, זיהוי שפה
- Multi-label: תמונה יכולה להכיל גם "חתול" גם "כלב"
- אלגוריתמים: Logistic Regression, SVM, Random Forest, Neural Networks
- מדדים: Accuracy, Precision, Recall, F1-Score, AUC-ROC

**Regression (רגרסיה):**
המודל מנבא ערך רציף (continuous).
- חיזוי מחיר בית, טמפרטורה, ביקוש מוצר
- אלגוריתמים: Linear Regression, Ridge, Lasso, Neural Networks
- מדדים: MSE, RMSE, MAE, R²

**בעיה: Imbalanced Classes:**
כאשר אחת המחלקות נדירה (למשל: 1% fraud). Accuracy לא מתאים — מודל שתמיד יחזיר "לא fraud" יקבל accuracy=99%!
פתרון: השתמש ב-Precision/Recall/F1, AUC-ROC, SMOTE לoversampling, class weights.

**נקודות מפתח:**
- Classification = output קטגורי; Regression = output רציף
- לעולם אל תשתמש ב-Accuracy בלבד עם imbalanced classes
- F1-Score = הממוצע ההרמוני של Precision ו-Recall

---

### שאלה 4: מה זה Cross-Validation ולמה הוא חשוב?
**תשובה:**
Cross-Validation הוא שיטה להערכת ביצועי מודל שמפחיתה את השונות של מדד ה-evaluation.

**K-Fold Cross-Validation:**
1. מחלקים את הנתונים ל-K חלקים שווים (folds)
2. בכל איטרציה: K-1 חלקים = אימון, 1 חלק = validation
3. מריצים K פעמים, כל פעם fold שונה הוא ה-validation
4. מחזירים ממוצע הביצועים על כל K הריצות

יתרון: מנצל את כל הנתונים לאימון ולוולידציה, נותן הערכה יציבה יותר.

**Leave-One-Out Cross-Validation (LOOCV):** K = N (מספר הדוגמאות). יקר חישובית אך שימושי לdatasets קטנים.

**Stratified K-Fold:** מבטיח שכל fold שומר על פרופורציה זהה של מחלקות. חשוב ב-imbalanced datasets.

**הפרדת Test Set:**
חשוב: test set צריך להיות נעול עד הערכה סופית! אם משתמשים ב-test set לכוונון hyperparameters, מתאכנסים לנתוני ה-test ומקבלים הערכה אופטימיסטית מדי.
- שלב 1: חלק נתונים ל-train+validation + test
- שלב 2: K-Fold על train+validation לבחירת hyperparameters
- שלב 3: אמן על כל train+validation עם הפרמטרים הטובים
- שלב 4: הערכה סופית על test set פעם אחת בלבד!

**נקודות מפתח:**
- Cross-validation עוזרת לזהות overfitting
- Test set צריך להיות "locked" עד הסוף
- Stratified K-Fold הכרחי ל-imbalanced data

---

### שאלה 5: מה ההבדל בין Precision, Recall ו-F1?
**תשובה:**
שלושת המדדים רלוונטיים לבעיות classification, במיוחד כאשר classes לא מאוזנות.

**ה-Confusion Matrix:**
```
              | Predicted Positive | Predicted Negative
Actual Positive |  TP (True Pos)    |  FN (False Neg)
Actual Negative |  FP (False Pos)   |  TN (True Neg)
```

**Precision (דיוק):** מכל מה שחזיתי כ-positive, כמה היה נכון?
`Precision = TP / (TP + FP)`
גבוה כאשר: חשוב להמנע מ-false alarms (spam filter — לא רוצים לסמן אימייל לגיטימי כspam)

**Recall (רגישות):** מכל ה-positives האמיתיים, כמה זיהיתי?
`Recall = TP / (TP + FN)`
גבוה כאשר: חשוב לא לפספס מקרים (גילוי מחלות — לא רוצים לפספס חולה)

**F1-Score:** הממוצע ההרמוני של Precision ו-Recall.
`F1 = 2 × (Precision × Recall) / (Precision + Recall)`
גבוה רק אם שניהם גבוהים. שימושי כאשר יש tradeoff בין השניים.

**AUC-ROC:** מודד ביצוע על כל ה-thresholds — ממוצע של Recall על ציר ה-X ו-False Positive Rate על ציר ה-Y. AUC=0.5 = אקראי, AUC=1 = מושלם.

**מתי מה:**
- Precision חשוב: spam detection, content moderation (עדיף לא לסנן מאשר לסנן בטעות)
- Recall חשוב: cancer detection, fraud (עדיף false alarm מאשר לפספס)
- F1: כאשר שניהם חשובים
- AUC-ROC: השוואת מודלים ללא תלות ב-threshold

**נקודות מפתח:**
- Accuracy גרועה ל-imbalanced data
- Precision vs Recall = tradeoff שמוגדר ע"י הדרישות העסקיות
- F1 = ממוצע הרמוני (לא ממוצע רגיל) — עונש על חוסר איזון

## סיכום
יסודות ML — supervised vs unsupervised, bias-variance tradeoff, ומדדי הערכה — הם הבסיס לכל ראיון ML. חשוב לא רק לדעת את ההגדרות, אלא להבין מתי כל מדד מתאים ואיך לפרש תוצאות. בפרקים הבאים נעמיק ב-neural networks, LLMs, ו-ML system design.

## מקורות להמשך לימוד
- Hands-On Machine Learning — Aurélien Géron
- Pattern Recognition and Machine Learning — Bishop
- scikit-learn Documentation
- StatQuest with Josh Starmer (YouTube)
