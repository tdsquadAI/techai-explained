# Transformers ו-LLMs — Attention, BERT ו-GPT

**מאת:** TechAI Explained Team

## מה נלמד בפרק הזה?
- מנגנון ה-Attention וכיצד הוא מאפשר ל-Transformers להבין הקשר
- ההבדל בין ארכיטקטורת BERT לGPT ומתי כל אחד מתאים
- כיצד מאמנים ומכווננים LLMs (Pre-training, Fine-tuning)

## שאלות ראיון נפוצות

### שאלה 1: מה הבעיה שה-Transformer פתר?
**תשובה:**
לפני Transformers, ה-state of the art ל-NLP היה RNN/LSTM. לאלה שתי בעיות מרכזיות:

**בעיה 1 — Sequential Processing:**
RNN מעבד טוקנים ברצף — כדי לעבד טוקן מספר 100, חייב לעבד קודם 1-99. זה מונע **parallelism** ומאט מאוד את האימון.

**בעיה 2 — Long-Range Dependencies:**
לאורך רצפים ארוכים, RNN "שוכח" מידע מוקדם. גם LSTM עם gates מגיע לגבולות.

**הפתרון — Self-Attention:**
Transformer (הוצג ב-"Attention is All You Need", 2017) מאפשר לכל טוקן לשים "תשומת לב" לכל טוקן אחר בו-זמנית, ללא ממגבלת רצף. כלומר:
- **Parallelizable לחלוטין** — כל הטוקנים מעובדים בו-זמנית
- **Direct access** לכל חלק ברצף, ללא "שכחה"

זה מה שאיפשר לאמן מודלים ענקיים על כמויות נתונים עצומות.

**נקודות מפתח:**
- Transformer פתר את בעיית ה-sequential processing וה-long-range dependencies
- הבסיס לכל ה-LLMs המודרניים: GPT, BERT, T5, LLaMA
- "Attention is All You Need" — נחשב אחד ממאמרי ה-AI החשובים בהיסטוריה

---

### שאלה 2: כיצד מנגנון Attention עובד?
**תשובה:**
Self-Attention מאפשר לכל טוקן ל"שאול שאלה" אצל כל טוקן אחר ברצף ולשקול את תשובתם.

**Query, Key, Value:**
לכל טוקן מחשבים שלושה וקטורים:
- **Q (Query):** "מה אני מחפש?"
- **K (Key):** "מה יש לי להציע?"
- **V (Value):** "מה המידע בפועל שלי?"

**החישוב:**
1. כל Query ×  כל Key → Attention Score (כמה רלוונטי כל טוקן)
2. Softmax על ה-scores → Attention Weights (סכום=1)
3. Weighted sum של Values → Output vector לכל טוקן

`Attention(Q,K,V) = softmax(QK^T / √d_k) × V`

**Multi-Head Attention:**
מריצים מספר Attention "heads" במקביל, כל אחד לומד patterns שונים (תחבירי, סמנטי, קו-רפרנס וכו'). מאחדים בסוף.

**Positional Encoding:**
כיוון ש-Transformer מעבד את כל הטוקנים בו-זמנית, אין לו מושג של סדר. Positional Encoding מוסיף מידע על מיקום כל טוקן לvectors שלו.

**נקודות מפתח:**
- Attention = "ציון רלוונטיות" בין כל זוג טוקנים
- Multi-head = לומד patterns מרובים בו-זמנית
- Complexity: O(n²) לאורך רצף — בעיה לרצפים ארוכים מאוד

---

### שאלה 3: מה ההבדל בין BERT ל-GPT?
**תשובה:**
שניהם מבוססים Transformer אך עם ארכיטקטורות שונות שמתאימות ל-use cases שונים:

**BERT (Bidirectional Encoder Representations from Transformers):**
- **ארכיטקטורה:** Encoder-only
- **קריאה:** דו-כיוונית — כל טוקן "רואה" גם מה לפניו וגם מה אחריו
- **Pre-training task:** Masked Language Modeling (MLM) — הסתרת 15% מהטוקנים וחיזויים, + Next Sentence Prediction
- **חוזק:** הבנת הקשר (understanding, NLU) — classification, NER, Question Answering
- **חולשה:** לא טוב ליצירת טקסט (לא auto-regressive)

**GPT (Generative Pre-trained Transformer):**
- **ארכיטקטורה:** Decoder-only
- **קריאה:** חד-כיוונית (causal) — כל טוקן רואה רק מה לפניו (לא מה אחריו)
- **Pre-training task:** Next Token Prediction — חיזוי הטוקן הבא
- **חוזק:** יצירת טקסט (generation, NLG) — text completion, chatbots, code generation
- **חולשה:** לא אופטימלי ל-classification (יכול לעשות עם prompt)

**T5 (Text-to-Text Transfer Transformer):**
Encoder-Decoder — מתאים ל-seq2seq tasks: תרגום, סיכום, Q&A.

**בפועל:**
- BERT: סיווג sentiment, NER, QA extractive
- GPT: כתיבת טקסט, code completion, conversational AI
- LLaMA, Mistral, Claude, Gemini: GPT-style (Decoder-only) בגדלים ויכולות שונות

**נקודות מפתח:**
- BERT = Encoder, GPT = Decoder — משפיע על כיוון ה-attention
- BERT טוב להבנה, GPT ליצירה
- מודלים מודרניים (GPT-4, Claude) = Decoder-only בקנה מידה עצום

---

### שאלה 4: מה זה Fine-tuning ו-PEFT?
**תשובה:**
**Pre-training:**
LLM מאומן על כמות עצומה של טקסט אינטרנטי (trillions של tokens). הוא לומד ייצוג כללי של שפה ועולם. יקר מאוד (מיליוני דולרים).

**Fine-tuning:**
לקחת מודל pre-trained ולאמן אותו על נתוני domain ספציפי לשיפור ביצועים. מעדכן את כל/רוב הפרמטרים של המודל.
- יקר לmodels גדולים (עדכון מיליארדי פרמטרים)
- דורש כמות סבירה של נתוני domain

**PEFT (Parameter-Efficient Fine-Tuning):**
שיטות לכוונון שמעדכנות רק **חלק קטן** מהפרמטרים:

1. **LoRA (Low-Rank Adaptation):**
   - מוסיף מטריצות קטנות בנות דרגה נמוכה (low-rank) ל-attention layers
   - מאמן רק את המטריצות החדשות (~0.1% מהפרמטרים)
   - ביצועים קרובים ל-full fine-tuning!
   - הנפוץ ביותר כיום

2. **Prefix Tuning:**
   - מוסיף tokens "virtual" לתחילת כל שכבה
   - המודל המקורי קפוא לחלוטין

3. **Adapter Layers:**
   - מוסיף שכבות קטנות בין שכבות ה-Transformer
   - קפוא את שכבות המקורי

**RLHF (Reinforcement Learning from Human Feedback):**
שלב נוסף לאחר fine-tuning — מאמנים reward model על העדפות אנושיות, ואז מכווננים עם RL לעמוד בציפיות אנושיות. זה מה שהפך ChatGPT ממודל "לנבא מילה הבאה" ל"עוזר שימושי".

**נקודות מפתח:**
- LoRA = הדרך הנפוצה לcustomize LLMs בעלות נמוכה
- RLHF קריטי ל-alignment — ללמד מודל להיות helpful ו-harmless
- Fine-tuning ≠ training from scratch — זה leverage של מה שכבר נלמד

---

### שאלה 5: מהם ה-challenges העיקריים של LLMs?
**תשובה:**
**1. Hallucination (הזיה):**
LLMs מייצרים טקסט עקבי ובטוח גם כאשר הם "ממציאים" עובדות שגויות. אין להם מנגנון מובנה לאמת עובדות.
פתרונות: RAG (Retrieval Augmented Generation), grounding to sources, uncertainty quantification.

**2. Context Window:**
מודלים מוגבלים בכמות הטוקנים שיכולים "לראות" בו-זמנית. GPT-4 = ~128K tokens, Claude 3 = 200K. קובץ ארוך מאוד לא יכנס ל-context.
פתרון: hierarchical summarization, chunking strategies, RAG.

**3. Knowledge Cutoff:**
מידע המודל מוגבל לתאריך סיום האימון. לא יודע על אירועים חדשים.
פתרון: RAG עם מקורות עדכניים, tool use לחיפוש בזמן אמת.

**4. Computational Cost:**
inference של LLMs גדולים דורש GPU חזק ויקר. latency יכול להיות גבוה.
פתרון: quantization (FP16, INT8, INT4), distillation, speculative decoding.

**5. Bias ו-Safety:**
מודלים לומדים biases מנתוני האינטרנט. עשויים לייצר תוכן מזיק אם לא מאומנים כראוי.
פתרון: RLHF, Constitutional AI, safety classifiers.

**6. Prompt Sensitivity:**
שינוי קטן בפרומפט יכול לשנות דרמטית את הפלט.
פתרון: prompt engineering, structured outputs, few-shot examples.

**נקודות מפתח:**
- Hallucination היא הבעיה המרכזית ל-production deployments
- RAG פותרת כמה בעיות: knowledge cutoff, hallucination, relevance
- RLHF לא פתרון מושלם — יש "alignment tax" על ביצועים

## סיכום
Transformers ו-LLMs מייצגים את הגל הנוכחי של מהפכת ה-AI. הבנת Attention Mechanism, ההבדל בין ארכיטקטורות Encoder/Decoder, ו-fine-tuning approaches היא חיונית לכל ראיון AI/ML. בפרק הבא נחפש כיצד RAG מפתרת את בעיית ה-knowledge cutoff וה-hallucination.

## מקורות להמשך לימוד
- Attention is All You Need — Vaswani et al. (2017)
- The Illustrated Transformer — Jay Alammar
- Hugging Face NLP Course
- Sebastian Raschka — LLMs from Scratch
