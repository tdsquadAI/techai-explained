# RAG — Retrieval Augmented Generation

**מאת:** TechAI Explained Team

## מה נלמד בפרק הזה?
- מה זה RAG ולמה הוא שינה את האופן שבו מפתחים עם LLMs
- כיצד Vector Databases ו-Embeddings עובדים
- שיקולי עיצוב RAG pipeline בעולם האמיתי

## שאלות ראיון נפוצות

### שאלה 1: מה זה RAG ולמה זה חשוב?
**תשובה:**
RAG (Retrieval Augmented Generation) היא ארכיטקטורה שמחברת בין LLM לבין מאגר ידע חיצוני. במקום להסתמך רק על מה שה-LLM למד בזמן האימון, RAG מאפשר לו לחפש מידע רלוונטי ב-runtime ולכלול אותו ב-context לפני יצירת התשובה.

**למה RAG?**
1. **Knowledge Cutoff** — LLMs לא יודעים על אירועים חדשים. RAG מאפשר גישה למידע עדכני
2. **Hallucination** — LLM ש"לא יודע" ממציא תשובות. עם RAG, הוא מסתמך על מסמכים אמיתיים
3. **Domain Knowledge** — שימוש במסמכים פנימיים של ארגון (docs, policies) ללא צורך ב-fine-tuning
4. **Traceability** — ניתן להצביע על המקורות שמהם הגיעה התשובה
5. **Cost Efficiency** — זול מ-fine-tuning, ניתן לעדכן מאגר ידע ללא אימון מחדש

**ה-flow הבסיסי של RAG:**
1. User שואל שאלה
2. המערכת **מחפשת** (retrieves) מסמכים רלוונטיים מה-knowledge base
3. מסמכים + שאלה מוזרמים ל-LLM כ-context
4. LLM יוצר תשובה מבוססת על המסמכים

**נקודות מפתח:**
- RAG = "search + generate" — לא יצירה מהזיכרון בלבד
- ניתן לעדכן מאגר ידע בזמן real-time ללא re-training
- חיוני לאפליקציות enterprise שצריכות מידע פנים-ארגוני

---

### שאלה 2: מה זה Embeddings ו-Vector Search?
**תשובה:**
**Embeddings:**
ייצוג נומרי (וקטור) של טקסט ב-space רב-ממדי. מודלי embedding ממירים משפטים לוקטורים כך שמשפטים דומים סמנטית = וקטורים קרובים במרחב.

דוגמה: 
- "חתול אוהב חלב" → [0.23, -0.45, 0.87, ...]
- "לחתולים טעים חלב" → [0.24, -0.43, 0.85, ...] (קרוב!)
- "המכונית נסעה מהר" → [-0.15, 0.72, -0.34, ...] (רחוק)

**Cosine Similarity:** מודד קרבה בין וקטורים. ערך 1 = זהה, 0 = לא קשורים, -1 = מנוגדים.

מודלי Embedding פופולריים: `text-embedding-ada-002` (OpenAI), `sentence-transformers` (HuggingFace), Cohere Embed.

**Vector Search:**
לאחר שיוצרים embeddings לכל המסמכים ב-knowledge base:
1. ממירים את השאלה ל-embedding
2. מחפשים את ה-K המסמכים הקרובים ביותר (K-Nearest Neighbors)
3. מחזירים את המסמכים הרלוונטיים ביותר

**נקודות מפתח:**
- Embeddings לוכדים משמעות סמנטית, לא רק keyword matching
- מממד גבוה (1536 לAda-002) מאפשר ייצוג עשיר
- Cosine similarity הנפוץ, אפשר גם Euclidean distance

---

### שאלה 3: מהם Vector Databases ומה ההבדל ביניהם?
**תשובה:**
Vector Database הוא מסד נתונים ייעודי לאחסון וחיפוש וקטורים במהירות. תומך ב-ANN (Approximate Nearest Neighbors) חיפוש — קרוב מספיק, מהיר מספיק.

**שחקנים עיקריים:**

**1. Pinecone:**
- Managed, serverless vector DB
- קל להתחלה, managed service
- יקר יחסית
- מתאים: prototypes ו-production מהיר

**2. Weaviate:**
- Open-source, multi-modal
- תומך ב-hybrid search (vector + BM25 keyword)
- גמיש, ניתן לself-host
- מתאים: production עם control מלא

**3. Qdrant:**
- Open-source, Rust-based, מהיר מאוד
- תומך ב-filtering לפי metadata
- מתאים: high performance use cases

**4. ChromaDB:**
- Lightweight, open-source
- מתאים ל-local development, prototypes

**5. pgvector:**
- Extension ל-PostgreSQL
- לאלה שכבר עובדים עם Postgres ולא רוצים DB חדש
- פשוט אך לא מתאים לscale ענק

**6. FAISS (Meta):**
- Library (לא DB) לחיפוש וקטורים יעיל
- מאוד מהיר, נפוץ ב-research
- לא כולל persistence, metadata, APIs

**Hybrid Search:**
שילוב vector search (semantic) + BM25 keyword search. מחזיר תוצאות טובות יותר מכל שיטה לבדה.

**נקודות מפתח:**
- אין "הטוב ביותר" — תלוי ב-scale, budget, ו-infra preferences
- Hybrid search בדרך כלל עדיף על vector search בלבד
- pgvector מתאים כנקודת פתיחה אם כבר יש Postgres

---

### שאלה 4: כיצד מעצבים RAG Pipeline בעולם האמיתי?
**תשובה:**
RAG pipeline מלא כולל כמה שלבים שכל אחד דורש תשומת לב:

**שלב 1 — Ingestion Pipeline (טעינת נתונים):**
1. **Loading:** קריאת מסמכים (PDF, Word, HTML, code)
2. **Chunking:** פיצול מסמכים לcunks קטנים. חשוב: chunk גדול מדי → context מיותר; קטן מדי → אובדן context
   - Chunking strategies: fixed-size, sentence-based, semantic chunking
3. **Embedding:** כל chunk → embedding vector
4. **Storing:** שמירה ב-vector DB עם metadata (source, date, section)

**שלב 2 — Query Pipeline (מענה לשאלות):**
1. **Query Understanding:** לעתים יש לנסח מחדש את השאלה (query rewriting, HyDE)
2. **Retrieval:** K-NN search ב-vector DB
3. **Re-ranking:** דירוג חוזר של תוצאות (Cross-Encoder לדיוק גבוה יותר)
4. **Context Building:** בניית prompt עם השאלה + המסמכים הרלוונטיים
5. **Generation:** LLM מייצר תשובה

**אתגרים נפוצים:**
- **Chunking strategy** — הפיצול משפיע מאוד על איכות הretrieval
- **Retrieval quality** — מה אם המסמך הנכון לא נמצא? (recall)
- **Context window** — מה עושים עם 20 מסמכים רלוונטיים?
- **Citation** — כיצד להצביע על מקורות ספציפיים?

**Advanced RAG Techniques:**
- **HyDE (Hypothetical Document Embeddings):** מייצרים מסמך היפותטי מהשאלה לפני החיפוש
- **Multi-query Retrieval:** מייצרים גרסאות מרובות של השאלה לשיפור recall
- **RAPTOR/Hierarchical RAG:** עץ סיכומים לtexts ארוכים

**נקודות מפתח:**
- Chunking strategy היא אחת ההחלטות החשובות ביותר ב-RAG
- Evaluation קריטי: RAGAS framework מודד faithfulness, relevance, context recall
- Naive RAG ≠ Production RAG — פרוד דורש re-ranking, hybrid search, evaluation

---

### שאלה 5: מה ה-tradeoffs בין RAG ל-Fine-tuning?
**תשובה:**
שתי גישות לhsתאמת LLM לdomain ספציפי — לכל אחת יתרונות וחסרונות:

**RAG:**
- **יתרונות:** ניתן לעדכן מידע ב-real-time; מקורות traceable; אין צורך ב-GPU לאימון; ניתן להתחיל מהר
- **חסרונות:** latency גבוה יותר (retrieval + generation); תלוי באיכות הretrieval; מורכבות תשתית
- **מתאים ל:** מידע שמשתנה תדיר, knowledge-intensive tasks, צורך ב-citations

**Fine-tuning:**
- **יתרונות:** המודל לומד style ו-format; לא צריך retrieval בruntime; latency נמוך יותר
- **חסרונות:** יקר (GPU time); קשה לעדכן מידע; hallucinations עדיין אפשריות; דורש נתוני אימון איכותיים
- **מתאים ל:** learning style/format ספציפי, tasks שדורשים format output מסוים

**בפועל — שילוב (RAG + Fine-tuning):**
- Fine-tune ל-style, tone, ו-format
- RAG ל-factual knowledge עדכני
- תוצאה: מודל שמדבר ב-tone הנכון ויודע עובדות עדכניות

**Prompt Engineering ראשון:**
לפני RAG ו-Fine-tuning — נסה prompt engineering. לעתים prompt טוב מספיק ואין צורך ב-infrastructure נוסף.

**נקודות מפתח:**
- RAG ≠ Fine-tuning — משלימים, לא מתחרים
- RAG עדיף לfactual updates; Fine-tuning לstyle adaptation
- תמיד התחל עם prompt engineering לפני ש-invest ב-RAG או Fine-tuning

## סיכום
RAG שינה את אופן בניית אפליקציות AI — במקום להסתמך על ידע "קפוא" של LLM, ניתן לחבר אותו למידע חי ועדכני. הבנת embeddings, vector search, ו-RAG pipeline design הפכו לכישורי ליבה לכל ML engineer שעובד עם LLMs. בראיון, הראה שאתה מבין לא רק מה RAG עושה, אלא גם את ה-tradeoffs ואת האתגרים ב-production.

## מקורות להמשך לימוד
- LangChain Documentation
- LlamaIndex Documentation
- RAGAS — RAG Evaluation Framework
- Andrej Karpathy — State of GPT (YouTube)
