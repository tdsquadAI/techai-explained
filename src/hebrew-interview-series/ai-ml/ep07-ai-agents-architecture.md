# ארכיטקטורת AI Agents — Tool Use ו-ReAct

**מאת:** TechAI Explained Team

## מה נלמד בפרק הזה?
- מה הם AI Agents ואיך הם שונים מchatbots רגילים
- ארכיטקטורות agents: single agent, multi-agent, orchestration patterns
- בניית agents בטוחים ואמינים בproduction

## שאלות ראיון נפוצות

### שאלה 1: מה זה AI Agent ומה הופך אותו ל"agent"?
**תשובה:**
AI Agent הוא מערכת שמשתמשת ב-LLM כ"מוח" לקבלת החלטות, יחד עם יכולת לבצע **פעולות** (actions) על העולם — לא רק לייצר טקסט.

**מה מגדיר "agent"?**
1. **Perception (תפיסה):** קולט מידע מהסביבה — שאלת משתמש, תוצאות כלים, state נוכחי
2. **Reasoning (חשיבה):** LLM מחליט מה לעשות הבא
3. **Action (פעולה):** מבצע פעולה — קורא API, מריץ קוד, שולח אימייל, מחפש ב-web
4. **Observation (תצפית):** קולט תוצאה מהפעולה
5. **Iteration:** ממשיך ב-loop עד להשגת המטרה

**ההבדל מ-LLM רגיל:**
- LLM רגיל: input → output (one-shot)
- Agent: goal → plan → execute → observe → plan again → ... → goal achieved

**סוגי Agents:**
- **Tool-using agents:** משתמש בכלים (search, calculator, code executor)
- **Planning agents:** מחלק מטרות למשימות ומבצע בסדר
- **Multi-agent systems:** מספר agents שמשתפים פעולה

**נקודות מפתח:**
- Agent = LLM + Memory + Tools + Planning
- Autonomy level משתנה: fully autonomous עד human-in-the-loop
- ה-loop הוא מה שמבדיל agent מchatbot

---

### שאלה 2: מה זה Tool Use ו-Function Calling?
**תשובה:**
Tool Use (נקרא גם Function Calling) מאפשר ל-LLM להחליט **מתי ואיזה כלי** לקרוא, לספק את הפרמטרים הנכונים, ולשלב את התוצאה בתשובה.

**כיצד Function Calling עובד (OpenAI API):**

1. **הגדרת tools:** מספקים ל-LLM רשימת functions עם שם, תיאור וparameters
```json
{
  "name": "get_weather",
  "description": "מחזיר תחזית מזג אוויר לעיר נתונה",
  "parameters": {
    "city": {"type": "string", "description": "שם העיר"}
  }
}
```

2. **LLM מחליט:** בהתאם לשאלה, ה-LLM מחזיר tool call request (לא תשובה ישירה):
```json
{"name": "get_weather", "arguments": {"city": "Tel Aviv"}}
```

3. **הApp מריץ:** הקוד שלך מריץ את הfunction, מקבל תוצאה

4. **LLM משלב:** שולחים את התוצאה חזרה, ה-LLM מייצר תשובה סופית

**Parallel Tool Calling:**
LLMs מודרניים יכולים לקרוא מספר tools בו-זמנית. GPT-4 ו-Claude תומכים בזה.

**Tool categories:**
- **Information tools:** web search, database lookup, file read
- **Action tools:** send email, create calendar event, post tweet
- **Compute tools:** code execution, calculator, image generation
- **Communication tools:** Slack message, API calls

**Grounding Effect:**
Tool use מנמיך hallucinations — ה-LLM עובד עם נתונים אמיתיים ולא מ"זיכרון" שעשוי להיות שגוי.

**נקודות מפתח:**
- Function calling = API structure ל-tool use
- תמיד validate tool outputs לפני שמשלבים בtשובה
- Tool descriptions חיוניות — LLM בוחר tool על בסיסן

---

### שאלה 3: מה ההבדל בין ארכיטקטורות Single Agent ל-Multi-Agent?
**תשובה:**
**Single Agent:**
LLM אחד עם כלים מרובים ו-loop. פשוט יחסית.

יתרונות: קל לdebug, פחות latency (אין communication בין agents), context מלא
חסרונות: context window מוגבל; אחד agent לא יכול להתמחות בהכל; קשה לhuman oversight

מתאים ל: tasks פשוטים עד בינוניים, use cases מוגדרים היטב

**Multi-Agent System:**
מספר agents שמשתפים פעולה — כל agent מתמחה בdomain ספציפי.

**דפוסי multi-agent:**

1. **Orchestrator + Sub-agents:**
   - Orchestrator (מנהל) מפרק task למשימות קטנות
   - Sub-agents מתמחים מבצעים כל משימה
   - Orchestrator מאחד תוצאות
   - דוגמה: Orchestrator → Research Agent + Writing Agent + Review Agent

2. **Peer-to-Peer Collaboration:**
   - Agents "מדברים" ישירות זה עם זה
   - כל agent יכול לבקש עזרה מהאחרים
   - מורכב יותר לניהול

3. **Assembly Line:**
   - Agent A → Agent B → Agent C (pipeline)
   - פלט של אחד הוא input של השני
   - ברור ומסודר, קשה להשתנות

4. **Voting / Debate:**
   - מספר agents נותנים תשובות
   - מנגנון majority vote או debate לbest answer
   - מגדיל accuracy אך יקר

**Frameworks מרכזיים:**
- **LangGraph:** graph-based agent orchestration
- **AutoGen (Microsoft):** multi-agent conversations
- **CrewAI:** role-based multi-agent
- **OpenAI Swarm:** lightweight multi-agent

**נקודות מפתח:**
- Start simple — single agent לפני multi-agent
- Multi-agent מוסיף complexity (debugging, latency, cost)
- Shared memory / state management הוא האתגר המרכזי

---

### שאלה 4: כיצד מנהלים Memory ב-Agents?
**תשובה:**
Agents צריכים לזכור מידע בין פעולות ובין שיחות. יש ארבעה סוגי memory:

**1. In-Context Memory (Working Memory):**
ה-context window הנוכחי. נגיש מיידית אך מוגבל בגודל וזמני (נאבד בסיום שיחה).
ניהול: Summarization כאשר context ארוך מדי; sliding window; selective retention.

**2. External Memory (Long-term Memory):**
מאגר ידע חיצוני שה-agent יכול לquery. בדרך כלל vector store.
- שמירת events חשובים, preferences, facts
- Retrieval לפי relevance לcontask הנוכחי
- כלים: Mem0, Zep, כל vector DB

**3. Episodic Memory:**
זיכרון של "מה עשיתי בעבר" — history של actions ותוצאותיהם.
שימושי ל: למידה מניסיון, אי-חזרה על טעויות

**4. Semantic Memory:**
ידע כללי — facts, concepts. ה-LLM עצמו + knowledge base חיצוני.

**Memory Management Strategies:**

- **Summarization:** אחרי כל N הודעות, סכם את השיחה עד כה
- **Entity extraction:** זיהוי וsaving ישויות חשובות (שמות, preferences)
- **Recency bias:** ה-working memory שומר recent context; older מועבר ל-external
- **Forgetting:** מחק מידע ישן / לא רלוונטי

**Memory ב-Production:**
- Redis / PostgreSQL ל-session memory
- Vector DB (Pinecone, Weaviate) ל-long-term semantic memory
- ה-agent מחליט מה לשמור ומה לשכוח (meta-memory)

**נקודות מפתח:**
- בלי memory, כל שיחה מתחילה מאפס — לא שימושי
- Long-term memory = persistent state בין sessions
- Memory retrieval = mini-RAG: חפש מה רלוונטי לcontask הנוכחי

---

### שאלה 5: אילו בעיות יש ב-Agents ב-Production?
**תשובה:**
Agents ב-production מציגים אתגרים ייחודיים שלא קיימים בLLM רגיל:

**1. Reliability ו-Determinism:**
Agents יכולים לקבל החלטות שונות ב-runs שונים. בproduction, זה עלול לגרום לתוצאות לא עקביות.
פתרון: extensive logging, deterministic tools where possible, human checkpoints.

**2. Infinite Loops:**
Agent שלא מוצא פתרון עלול להמשיך ב-loop. 
פתרון: max_iterations limit, timeout, fallback to human.

**3. Tool Failures:**
כלים חיצוניים (APIs) נכשלים. איך ה-agent מגיב?
פתרון: retry logic, error handling בprompt, fallback tools.

**4. Cost Management:**
Agent loops = הרבה LLM calls = עלות גבוהה.
פתרון: caching, cheaper models לsub-tasks, token budget tracking.

**5. Safety ו-Guardrails:**
Agent שיכול לשלוח אימיילים, למחוק files, לבצע רכישות — מסוכן אם לא מאובטח.
פתרון:
- **Human-in-the-loop:** אישור אנושי לprioritized actions
- **Action whitelisting:** רשימה מוגדרת של actions מורשות
- **Sandbox execution:** קוד רץ בsandbox מבודד
- **Rate limiting:** הגבלת פעולות בזמן נתון

**6. Observability:**
קשה לדבג agent כשאין ראות מלאה על ה-reasoning path.
פתרון: full logging של thought process, LangSmith, Phoenix, Langfuse.

**7. Prompt Injection:**
אם ה-agent קורא תוכן מאינטרנט, משתמש זדוני יכול לשתול הוראות שמפנות ה-agent.
פתרון: sanitize tool outputs, context isolation.

**נקודות מפתח:**
- Production agents צריכים human oversight לhigh-stakes actions
- Observability (logging, tracing) חיוני לdebug
- "Minimal footprint principle" — agent צריך רק הרשאות שבאמת נחוץ

## סיכום
AI Agents מייצגים את הגבול הבא של AI applications — מLLMs שעונים לLLMs שמבצעים. הבנת ארכיטקטורת agents, tool use, memory management ו-production challenges היא קריטית לכל מי שרוצה לבנות AI systems מתקדמים. בראיון, הראה שאתה מבין גם את היכולות וגם את המגבלות — especially לגבי safety ו-reliability.

## מקורות להמשך לימוד
- LangChain Agents Documentation
- AutoGen (Microsoft Research)
- Building Effective Agents — Anthropic Blog
- ReAct: Synergizing Reasoning and Acting
