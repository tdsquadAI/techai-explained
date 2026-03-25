# AI אחראי — הטיה, הוגנות, הסבריות והערכה

**מאת:** TechAI Explained Team

## מה נלמד בפרק הזה?
- מהי הטיה (bias) במערכות AI ואיך לזהות ולמדוד אותה
- עקרונות הוגנות (fairness) ב-AI והאתגרים המדדיים
- Explainable AI (XAI) — שיטות להסביר החלטות מודל

## שאלות ראיון נפוצות

### שאלה 1: מה זה Bias ב-AI ומאין הוא מגיע?
**תשובה:**
Bias ב-AI מתייחס לנטייה שיטתית של מודל לפקח לא נכון על קבוצות מסוימות של אנשים בצורה לא הוגנת. זהו אחד האתגרים החשובים ביותר ב-Responsible AI.

**מקורות Bias:**

**1. Historical Bias:**
הנתונים משקפים אי-שוויון היסטורי. מודל גיוס שמאומן על נתוני גיוס עבר — שבהם אנשים ממגדר מסוים קיבלו עדיפות — ילמד ויעצים את האי-שוויון.

**2. Representation Bias:**
קבוצות מסוימות חסרות ייצוג בנתוני האימון. מודל זיהוי פנים שאומן בעיקר על תמונות של אנשים בהירי עור — ביצועיו גרועים על אנשים כהי עור.

**3. Measurement Bias:**
הדרך שבה מודדים features או labels משתנה בין קבוצות. "crime rate" כfeature — משקף אי-שוויון בסיור משטרתי, לא רק פשיעה אמיתית.

**4. Aggregation Bias:**
שימוש במודל אחד לכלל האוכלוסייה כאשר צריך מודלים נפרדים לqroups שונים.

**5. Feedback Loops:**
מודל שמשפיע על מה שקורה בעולם → משפיע על נתוני אימון עתידיים → מעצים את ה-bias.

**דוגמאות מפורסמות:**
- COMPAS: מודל לחיזוי חזרה לפשיעה — bias נגד אנשים שחורים
- Amazon Rekognition: דיוק נמוך יותר לזיהוי פנים כהות עור
- Amazon hiring algorithm: הוסר כי הפלה נגד מועמדות נשים

**נקודות מפתח:**
- Bias מגיע מנתונים, לא מ"רצון" המודל
- "Garbage in, garbage out" — נתונים לא הוגנים → מודל לא הוגן
- בדיקת bias צריכה להיות חלק מproc הפיתוח, לא תוספת בסוף

---

### שאלה 2: כיצד מודדים Fairness ב-AI?
**תשובה:**
קיימות הגדרות מרובות ל-fairness, ולמרבה הצער — הוכח מתמטית שלא ניתן לקיים את כולן בו-זמנית.

**מדדי Fairness עיקריים:**

**Demographic Parity (Statistical Parity):**
קבוצות שונות מקבלות תוצאות חיוביות באחוזים שווים.
- `P(ŷ=1 | group=A) = P(ŷ=1 | group=B)`
- דוגמה: אחוז הזוכים בהלוואה שווה בין גברים לנשים.

**Equal Opportunity:**
ה-True Positive Rate שווה בין קבוצות — כל המועמדים ה"ראויים" מקבלים הזדמנות שווה.
- `P(ŷ=1 | y=1, group=A) = P(ŷ=1 | y=1, group=B)`

**Equalized Odds:**
גם TPR וגם FPR שווים בין קבוצות — הכי מחמיר.

**Individual Fairness:**
שני אנשים דומים צריכים לקבל תוצאות דומות — ללא קשר לקבוצה.

**Calibration:**
P(y=1 | ŷ=p) = p לכל p, לכל קבוצה.

**ה-Impossibility Theorem:**
Chouldechova ו-Kleinberg הוכיחו שאי אפשר לקיים במקביל:
1. Calibration
2. Equal FPR
3. Equal FNR
(אלא אם base rates שווות בין קבוצות)

**בפועל:**
בחר את הגדרת fairness המתאימה לcontax העסקי. מה הנזק הגדול יותר — false positive או false negative? לאיזו קבוצה?

**נקודות מפתח:**
- אין "fairness אחת נכונה" — יש trade-offs בין הגדרות
- Fairness מדיד ≠ fairness מוסרית מלאה
- תמיד בדוק performance metrics separately לכל demographic group

---

### שאלה 3: מה זה Explainability ומדוע זה חשוב?
**תשובה:**
Explainable AI (XAI) מתייחס לשיטות שמאפשרות להבין **מדוע** מודל קיבל החלטה מסוימת.

**למה Explainability חשוב:**
1. **Regulatory Compliance:** GDPR (EU) מחייב "right to explanation" להחלטות אוטומטיות
2. **Trust:** משתמשים ורגולטורים לא יאמצו מודל שהוא "black box" לdecisions קריטיות
3. **Debugging:** להבין מה המודל "למד לא נכון"
4. **Fairness auditing:** לבדוק האם features לא-מותרים (גיל, מגדר) משפיעים על predictions

**Global vs Local Explanations:**
- **Global:** מה המודל באופן כללי לומד? אילו features הכי חשובים בממוצע?
- **Local:** מדוע prediction ספציפי זה ניתן? מה השפיע על התוצאה הספציפית?

**שיטות מרכזיות:**

**SHAP (SHapley Additive exPlanations):**
מבוסס על Game Theory. מחשב Shapley values — כמה כל feature תרם לprediction ספציפי.
- Model-agnostic (עובד על כל מודל)
- מדויק אך חישובית יקר
- הנפוץ ביותר כיום

**LIME (Local Interpretable Model-agnostic Explanations):**
מאמן מודל פשוט (לינארי) סביב prediction ספציפי. מסביר locally.
- מהיר יותר מSHAP
- פחות עקבי — הסברים יכולים להשתנות בין runs

**Attention Visualization:**
ב-Transformers — ניתוח attention weights להבנה אילו tokens השפיעו.
פחות מהימן כ-explanation כי attention ≠ causation.

**Integrated Gradients:**
מחשב attributions לפי gradients. מדויק יחסית לneural networks.

**Inherently Interpretable Models:**
Decision Trees, Linear Regression, Rule-based systems — כבר explainable by design.
כלל אצבע: אם task מאפשר, בחר interpretable model על black box.

**נקודות מפתח:**
- SHAP הוא gold standard לfeature attribution
- Explanations local ≠ explanations global
- עם LLMs — explainability עדיין open research problem

---

### שאלה 4: כיצד מעריכים ומנטרים מערכות AI?
**תשובה:**
Evaluation נכונה של AI systems הוא אחד האתגרים הקשים ביותר בפיתוח.

**Evaluation for Classification/Regression:**
מדדים כמותיים: accuracy, F1, AUC-ROC, RMSE.
אבל: metric שאתה מדווח עליו הופך ל-target, וה-target מפסיק להיות מדד טוב (Goodhart's Law).

**Evaluation for LLMs:**
יותר מורכב — הפלט טקסט פתוח.

1. **Benchmarks:**
   - MMLU, HellaSwag, ARC — knowledge ו-reasoning
   - HumanEval — code generation
   - MT-Bench — multi-turn conversation
   בעיה: LLMs מגיעים ל"data contamination" — הbenchmarks נמצאים בtraining data.

2. **LLM-as-Judge:**
   שימוש ב-LLM אחר (GPT-4, Claude) לדרג פלטים.
   יתרון: scalable, לא דורש human annotators
   חסרון: ה-judge עצמו יכול להיות biased (self-preference bias)

3. **Human Evaluation:**
   Human annotators דורגים תשובות. הכי מהימן אך יקר ואיטי.
   Preference tests (A vs B): "איזו תשובה עדיפה?"

4. **RAGAS (ל-RAG systems):**
   מדדים ספציפיים: Faithfulness, Answer Relevance, Context Recall, Context Precision.

**Red Teaming:**
ניסיון לגרום למודל להתנהג לא נכון — jailbreaks, adversarial prompts, edge cases. קריטי לפני deployment.

**Monitoring בProduction:**
- Tracking distribution שינויים ב-outputs
- Sample לreview אנושי תקופתי
- Feedback loop מ-users

**נקודות מפתח:**
- No single metric tells the whole story — evaluation portfolio
- Red teaming חיוני לfind failure modes לפני deployment
- Continuous monitoring — מודל שעבד טוב ב-launch יכול לדרדר

---

### שאלה 5: מה הם עקרונות Responsible AI?
**תשובה:**
Responsible AI הוא מסגרת עקרונות לפיתוח ו-deployment של מערכות AI שהן הוגנות, בטוחות, שקופות ואחראיות.

**עקרונות מרכזיים (EU AI Act, Microsoft, Google, IBM):**

**1. Fairness:**
מערכות AI לא ישמרו או יעצימו אי-שוויון. בדיקה פעילה ל-bias בנתונים ובמודל.

**2. Reliability & Safety:**
מערכות AI צריכות לפעול כצפוי, בטוח ועמיד לכשלים. "Do no harm" — מונע גרימת נזק.

**3. Transparency & Explainability:**
שקיפות לגבי מה מערכת AI יכולה ולא יכולה לעשות. הסברים להחלטות.

**4. Privacy & Security:**
שמירת פרטיות המשתמשים. מניעת שימוש לרעה בנתונים אישיים.

**5. Accountability:**
ברורות מי אחראי על ההחלטות של מערכת AI. "Humans in the loop" לhigh-stakes decisions.

**6. Inclusivity:**
מערכות AI צריכות לשרת את כלל האוכלוסייה, לא רק קבוצות מסוימות.

**AI Act (EU):**
הרגולציה הראשונה לAI בעולם. מסווג AI systems לפי risk:
- Unacceptable risk: אסור (social scoring, biometric surveillance)
- High risk: דורש בדיקות fairness, transparency, human oversight (hiring, credit, medical)
- Limited/Minimal risk: הוראות שקיפות בלבד (chatbots)

**Responsible AI Practices:**

1. **Diverse teams:** צוותים מגוונים מזהים bias שצוותים הומוגניים מפספסים
2. **Impact assessments:** לפני deployment, הערך השפעות אפשריות על קבוצות שונות
3. **Fairness testing:** בדוק performance metrics per demographic group
4. **Documentation (Model Cards):** פרסם "model card" עם ביצועים, מגבלות ו-intended use
5. **Feedback mechanisms:** אפשר למשתמשים לדווח על תוצאות לא הוגנות
6. **Regular audits:** בדיקות תקופתיות לdrift ב-fairness

**נקודות מפתח:**
- Responsible AI = ethical + legal + technical practices
- EU AI Act כבר בתוקף — לא רק theory
- Model Cards ו-Dataset Cards הן best practice שכל מוצר AI צריך

## סיכום
Responsible AI עוצמת לאחד מהתחומים הקריטיים ביותר כשמערכות AI הופכות לחלק מהחלטות חיוניות בחיינו. הבנת bias, fairness definitions, explainability ו-evaluation frameworks הם לא רק "nice to have" — הם דרישה professional ורגולטורית. בראיון, הראה שאתה מבין ש-ML engineering כוללת אחריות על ההשפעה החברתית של המערכות שאתה בונה.

## מקורות להמשך לימוד
- Fairness and Machine Learning — Barocas, Hardt, Narayanan (fairmlbook.org)
- Model Cards for Model Reporting — Mitchell et al.
- EU AI Act Official Text
- Responsible AI Practices — Google AI
