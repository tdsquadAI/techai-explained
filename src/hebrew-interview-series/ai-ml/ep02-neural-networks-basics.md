# רשתות נוירונים — שכבות, פונקציות הפעלה ו-Backpropagation

**מאת:** TechAI Explained Team

## מה נלמד בפרק הזה?
- מבנה רשת נוירונים: שכבות, נוירונים ומשקלות
- פונקציות הפעלה ותפקידן — ReLU, Sigmoid, Softmax
- כיצד Backpropagation לומד מטעויות ומעדכן משקלות

## שאלות ראיון נפוצות

### שאלה 1: כיצד בנויה רשת נוירונים?
**תשובה:**
רשת נוירונים מלאכותית (Artificial Neural Network — ANN) מורכבת מ**שכבות** (layers) של **נוירונים** (nodes) שמחוברים ביניהם.

**מרכיבים עיקריים:**

1. **Input Layer (שכבת קלט):** מקבלת את הנתונים הגולמיים. כמות הנוירונים שווה למספר ה-features. לא מבצעת חישוב, רק מעבירה.

2. **Hidden Layers (שכבות נסתרות):** שכבה אחת או יותר שמבצעות חישובים. כל נוירון מחשב סכום משוקלל של הקלטות ממנו ומפעיל עליו פונקציית הפעלה (activation function).

3. **Output Layer (שכבת פלט):** מייצרת את הפלט הסופי. מספר הנוירונים תואם את מספר המחלקות (binary → 1 נוירון, multi-class → N נוירונים).

**החישוב בנוירון בודד:**
`output = activation(w1*x1 + w2*x2 + ... + wn*xn + bias)`

כאשר `w` = משקלות (weights), `x` = קלטות, `bias` = הוספת גמישות.

**Deep Learning:** רשת עם שכבות נסתרות רבות. "עומק" = מספר שכבות. ההירארכיה מאפשרת ללמוד features מורכבים יותר בכל שכבה.

**נקודות מפתח:**
- כל שכבה נסתרת לומדת ייצוג (representation) מופשט יותר
- יותר שכבות ≠ תמיד טוב — יש בעיית Vanishing Gradient בעמקי הרשת
- Width (רוחב) ו-Depth (עומק) הם hyperparameters שמשפיעים על capacity

---

### שאלה 2: מה זה פונקציות הפעלה ולמה הן נחוצות?
**תשובה:**
פונקציית הפעלה (Activation Function) מוסיפה **אי-לינאריות** לרשת. בלעדיה, רשת של שכבות רבות הייתה שקולה לשכבה לינארית אחת — לא יכולה ללמוד patterns מורכבים.

**פונקציות נפוצות:**

**1. Sigmoid:**
`σ(x) = 1 / (1 + e^(-x))` → טווח: (0, 1)
- שימוש: פלט binary classification (הסתברות)
- בעיה: **Vanishing Gradient** — בערכים קיצוניים, gradient ≈ 0 → רשת עמוקה לא לומדת

**2. ReLU (Rectified Linear Unit):**
`f(x) = max(0, x)` → מחזיר x אם חיובי, אחרת 0
- הנפוץ ביותר היום ל-hidden layers
- מהיר לחישוב, gradient=1 לערכים חיוביים
- בעיה: **Dying ReLU** — נוירונים שמקבלים ערכים שליליים תמיד "מתים" (gradient=0)
- פתרונות: Leaky ReLU, ELU

**3. Softmax:**
מחשב הסתברויות עבור multi-class classification — כל output בטווח (0,1) והסכום = 1
- שימוש: שכבת פלט לסיווג רב-מחלקתי

**4. Tanh:**
טווח (-1, 1). דומה ל-sigmoid אך ממורכז סביב 0. עדיף על sigmoid ל-hidden layers אך גם סובל מ-vanishing gradient.

**5. GELU (Gaussian Error Linear Unit):**
שימוש ב-Transformers ו-BERT. גרסה חלקה ומשופרת של ReLU.

**נקודות מפתח:**
- ReLU = הבחירה הראשונה ל-hidden layers ברוב הרשתות
- Sigmoid ו-Softmax ל-output layers בלבד
- Vanishing Gradient = הסיבה ש-ReLU החליף Sigmoid ב-hidden layers

---

### שאלה 3: כיצד Backpropagation עובד?
**תשובה:**
Backpropagation הוא האלגוריתם שמאפשר לרשת ללמוד — הוא מחשב כיצד לשנות כל משקל כדי להפחית את שגיאת הפלט.

**שני שלבים:**

**1. Forward Pass (מעבר קדימה):**
- הקלט עובר משכבה לשכבה עד לפלט
- מחשבים את שגיאת הפלט מול התשובה הנכונה (Loss Function)
- Loss פופולארי: Cross-Entropy לסיווג, MSE לרגרסיה

**2. Backward Pass (מעבר לאחור) — Backpropagation:**
- מחשבים את הנגזרת של ה-loss לגבי כל משקל (gradient)
- משתמשים ב-Chain Rule כדי לחשב gradients לכל שכבה מהסוף להתחלה
- מעדכנים משקלות בכיוון שמפחית ה-loss: `w = w - learning_rate × gradient`

**Gradient Descent:**
- **Batch GD:** מחשב gradient על כל הנתונים — מדויק אך איטי
- **Stochastic GD (SGD):** gradient על דוגמה אחת — מהיר אך רועש
- **Mini-batch GD:** gradient על batch קטן — איזון בין מהירות לדיוק. הנפוץ בפועל

**Optimizers מתקדמים:**
- **Adam:** משלב Momentum ו-RMSProp. Learning rate adaptive לכל פרמטר. הנפוץ ביותר כיום
- **AdamW:** Adam עם weight decay — טוב ל-Transformers

**נקודות מפתח:**
- Backprop = Chain Rule + Gradient Descent
- Learning Rate חשוב — גדול מדי = לא מתכנס, קטן מדי = איטי
- Adam הוא baseline optimizer טוב לרוב הבעיות

---

### שאלה 4: מה זה Regularization ולמה זה חשוב?
**תשובה:**
Regularization הוא קבוצת טכניקות למניעת overfitting — גרימה למודל להיות "פשוט יותר" ולהכליל טוב יותר על נתונים חדשים.

**L1 Regularization (Lasso):**
מוסיף לloss `λ × Σ|w|`. גורם לחלק מהמשקלות להתאפס — מייצר **sparse models**. שימושי ל-feature selection.

**L2 Regularization (Ridge / Weight Decay):**
מוסיף לloss `λ × Σw²`. מוריד משקלות גדולים אך לא מאפס — גורם למשקלות להיות קטנים ומפוזרים. הנפוץ יותר.

**Dropout:**
בכל צעד אימון, מבטל אקראית חלק מהנוירונים (למשל 20%). הרשת לומדת להסתמך על patterns מרובים ולא על נוירונים ספציפיים. רק בשלב training — ב-inference כל הנוירונים פעילים.

**Early Stopping:**
עוצרים אימון כאשר ה-validation loss מפסיק להתפחית. פשוט ויעיל.

**Batch Normalization:**
מנרמל את הpre-activations בכל שכבה. מאיץ אימון ומאפשר learning rates גבוהים יותר. משמש כ-regularizer.

**Data Augmentation:**
הגדלה מלאכותית של dataset — לתמונות: סיבוב, חיתוך, שינוי צבע. מעלה גיוון בנתוני אימון.

**נקודות מפתח:**
- L2 + Dropout + Early Stopping = combination נפוץ
- Regularization strength (λ) הוא hyperparameter שכדאי לכוונן
- Dropout שימושי ל-fully connected layers; BatchNorm ל-convolutional

---

### שאלה 5: מה ההבדל בין CNN ל-RNN?
**תשובה:**
שני סוגי ארכיטקטורות ייעודיות ל-data שונה:

**CNN (Convolutional Neural Network):**
- מיועד לנתוני grid: תמונות, אות (audio), טקסט כspatial data
- מבצע convolution — מסנן קטן (kernel) שסורק על הקלט ומזהה patterns מקומיים
- **Pooling layers** מפחיתות מימדים ומוסיפות invariance
- ארכיטקטורות: ResNet, VGG, EfficientNet
- שימוש: זיהוי תמונות, object detection, semantic segmentation

**RNN (Recurrent Neural Network):**
- מיועד לנתונים סדרתיים (sequential): טקסט, time series, audio
- שומר **hidden state** שמועבר בין צעדים — "זיכרון" של הרשת
- בעיה: Vanishing Gradient לרצפים ארוכים — RNN שוכח מידע ישן

**LSTM (Long Short-Term Memory):**
שיפור של RNN — מוסיף gates (Forget, Input, Output) שמאפשרים לשלוט מה לשמור ומה לשכוח. פתרון טוב לlong-range dependencies.

**GRU (Gated Recurrent Unit):**
גרסה פשוטה יותר של LSTM עם פחות פרמטרים, לרוב ביצועים דומים.

**עכשיו:** Transformers החליפו את RNNs ברוב tasks של NLP — הם מקבילים יותר ואינם סובלים מ-vanishing gradient.

**נקודות מפתח:**
- CNN = מרחבי (spatial); RNN = סדרתי (sequential)
- LSTM פתרה את בעיית ה-vanishing gradient ב-RNN
- Transformers החליפו RNN/LSTM ב-NLP כיום

## סיכום
רשתות נוירונים הן הבסיס של modern deep learning. הבנת ארכיטקטורת שכבות, פונקציות הפעלה, backpropagation ו-regularization היא קריטית לכל ראיון ML. בפרק הבא נעמיק ב-Transformers ו-LLMs — הארכיטקטורה שמניעת את מהפכת ה-AI המודרנית.

## מקורות להמשך לימוד
- Deep Learning — Goodfellow, Bengio, Courville
- Fast.ai Practical Deep Learning Course
- 3Blue1Brown — Neural Networks Series (YouTube)
- PyTorch Documentation
