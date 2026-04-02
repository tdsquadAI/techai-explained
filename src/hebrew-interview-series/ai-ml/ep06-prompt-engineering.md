# Prompt Engineering — דפוסים ו-Chain of Thought

**מאת:** TechAI Explained Team

## מה נלמד בפרק הזה?
- עקרונות Prompt Engineering: כיצד לתקשר עם LLMs בצורה יעילה
- טכניקות מתקדמות: Few-shot, Chain-of-Thought, ReAct
- בניית prompts עמידים לproduction

## שאלות ראיון נפוצות

### שאלה 1: מה זה Prompt Engineering ולמה זה מיומנות חשובה?
**תשובה:**
Prompt Engineering הוא אמנות וגם מדע של עיצוב הקלט (prompt) לLLM כדי לקבל פלט רצוי, עקבי ומדויק. למרות שנשמע פשוט, prompt design משפיע דרמטית על איכות התוצאות.

**למה זה חשוב:**
- שינוי קטן בניסוח יכול לשנות לחלוטין את הפלט
- prompts טובים מפחיתים hallucinations ומשפרים דיוק
- בpractice — prompt engineering הוא לרוב מהיר ויעיל יותר מfine-tuning
- מיומנות נדרשת לכל תפקיד שעובד עם LLMs

**עקרונות בסיסיים:**

1. **Clarity (בהירות):** היה ספציפי — "כתוב סיכום של 3 משפטים" > "תסכם"
2. **Context (הקשר):** ספק מידע רקע רלוונטי
3. **Format (תבנית):** הגדר את מבנה הפלט הרצוי — JSON, bullet points, פסקאות
4. **Role (תפקיד):** "אתה מומחה לאבטחת מידע עם 10 שנות ניסיון"
5. **Examples (דוגמאות):** הראה ל-LLM את הפלט הרצוי דרך דוגמאות

**מה להימנע:**
- prompts עמומים ("כתוב משהו טוב")
- הנחת הנחות שלא נאמרו בprompt
- prompts ארוכים מדי עם הוראות סותרות

**נקודות מפתח:**
- Prompt engineering הוא iterative — בדוק, מדוד, שפר
- System prompt ל-behavior כללי; User prompt לבקשה ספציפית
- Temperature = creativity level: 0 = deterministic, 1 = creative

---

### שאלה 2: מה זה Few-Shot Prompting?
**תשובה:**
Few-Shot Prompting היא טכניקה שבה מספקים ל-LLM כמה דוגמאות (2-10) של input/output רצוי בתוך ה-prompt עצמו, לפני הבקשה האמיתית.

**סוגים:**

**Zero-Shot:** ללא דוגמאות — מסתמכים על יכולות ה-LLM הבסיסיות
```
סווג את הסנטימנט של הביקורת: "המוצר היה גרוע מאוד"
```

**One-Shot:** דוגמה אחת
```
ביקורת: "המוצר מעולה!" → סנטימנט: חיובי
ביקורת: "המוצר היה גרוע מאוד" → סנטימנט:
```

**Few-Shot:** כמה דוגמאות
```
ביקורת: "המוצר מעולה!" → סנטימנט: חיובי
ביקורת: "לא שווה את הכסף" → סנטימנט: שלילי
ביקורת: "בסדר, לא יוצא דופן" → סנטימנט: ניטרלי
ביקורת: "המוצר היה גרוע מאוד" → סנטימנט:
```

**מתי Few-Shot עוזר:**
- כאשר הformat חשוב ומדויק (JSON ספציפי, HTML template)
- כאשר יש "רוח" מסוימת שקשה להסביר במילים
- כאשר Zero-Shot מייצר תוצאות לא עקביות

**טיפים:**
- דוגמאות שונות ומגוונות = טוב יותר מדוגמאות דומות
- סדר הדוגמאות משפיע — השימה האחרונה לפני הבקשה הכי משפיעה
- 4-8 דוגמאות בדרך כלל מספיק

**נקודות מפתח:**
- Few-shot = in-context learning — המודל לא לומד לצמיתות, רק ב-context
- זול מfine-tuning אך פחות יעיל לtasks מורכבים מאוד
- Dynamic few-shot: בחר דוגמאות רלוונטיות דינמית (לפי similarity)

---

### שאלה 3: מה זה Chain-of-Thought Prompting?
**תשובה:**
Chain-of-Thought (CoT) היא טכניקה שגורמת ל-LLM לפתוח את חשיבתו ב"צעדים ביניים" לפני מתן התשובה הסופית. הוכח שמשפר מאוד ביצועים ב-reasoning tasks.

**הרעיון:**
LLMs נוטים לטעות כאשר קופצים ישר לתשובה. על ידי "חשיבה בקול" צעד אחרי צעד, המודל עושה פחות טעויות.

**Zero-Shot CoT:**
הוספת "Let's think step by step" או "בוא נחשוב צעד אחרי צעד" לסוף ה-prompt.
מחקר הוכיח שרק הוספת ביטוי זה משפרת accuracy ב-arithmetic ו-reasoning tasks.

**Few-Shot CoT:**
ספק דוגמאות שכוללות reasoning מלא:
```
שאלה: אם יש לי 5 תפוחים ואני נותן 2 לחבר, כמה נשארו?
חשיבה: אני מתחיל עם 5 תפוחים. אני נותן 2. 5-2=3.
תשובה: 3 תפוחים.

שאלה: אם חנות קנתה 100 מוצרים ב-$5 כל אחד ומכרה 70 ב-$8, מה הרווח?
חשיבה:
```

**Self-Consistency:**
הרץ את אותה שאלה מספר פעמים עם temperature > 0, קח את התשובה הנפוצה ביותר (majority vote). משפר accuracy ב-CoT.

**Tree of Thoughts (ToT):**
הרחבה של CoT — חוקר עצים של מחשבות ומאפשר backtracking. שימושי לbעיות מורכבות יותר.

**מתי CoT מועיל:**
- Math word problems
- Multi-step reasoning
- Code debugging
- Complex analysis

**מתי CoT לא עוזר:**
- Simple factual questions (CoT עלול לבלבל)
- Creative tasks

**נקודות מפתח:**
- "Let's think step by step" היא אחת ה-prompts היעילות ביותר שהתגלו
- CoT עובד טוב יותר על מודלים גדולים (>100B parameters)
- Self-Consistency משפרת accuracy אך מכפילה עלות

---

### שאלה 4: מה זה ReAct Pattern?
**תשובה:**
ReAct (Reasoning + Acting) הוא דפוס prompting שמשלב reasoning (חשיבה) עם action (פעולה) — ה-LLM לא רק "חושב" אלא גם קורא כלים ומשתמש בתוצאותיהם.

**ה-flow:**
```
Thought: צריך לדעת את מחיר המניה הנוכחי של Apple
Action: search("Apple stock price today")
Observation: AAPL = $185.50
Thought: עכשיו יכול לענות על השאלה
Answer: מחיר מניית Apple היום הוא $185.50
```

**למה ReAct?**
LLMs מוגבלים בידע שלהם (knowledge cutoff). ReAct מאפשר להם לגשת לכלים חיצוניים:
- Web search
- Code execution
- Database queries
- API calls
- Calculator

**ReAct vs Chain-of-Thought:**
- CoT: חשיבה בלבד, ללא כלים
- ReAct: חשיבה + שימוש בכלים + תצפית על תוצאות
- ReAct מתאים לtasks שדורשים מידע עדכני או חישובים

**Grounding ב-ReAct:**
ה-"Observation" מה-tools מנמיך hallucinations — ה-LLM מסתמך על נתונים אמיתיים.

**מימוש:**
LangChain, LlamaIndex, AutoGen — כולם תומכים ב-ReAct agents.

**נקודות מפתח:**
- ReAct = הבסיס לרוב AI agent frameworks
- Tool calling (function calling ב-OpenAI API) הוא מימוש מודרני של ReAct
- חשוב להגביל tools ולוולידציה outputs — security concern

---

### שאלה 5: כיצד בונים prompts עמידים לproduction?
**תשובה:**
Prompt Engineering לproduction שונה ממשחק עם prompts ב-playground. יש לבנות prompts שעובדים עקבית, בטוחים, ומדידים.

**1. Prompt Templates:**
אל תשמור prompts כ-hardcoded strings. השתמש בtemplates עם variables:
```python
SYSTEM_PROMPT = """
אתה עוזר לתמיכת לקוחות של {company_name}.
ענה תמיד ב{language}.
אם אינך יודע — אמור "לא יודע".
"""
```

**2. Output Parsing:**
דרוש output מובנה (JSON) כדי לפרסר בצורה אמינה:
- "ענה תמיד ב-JSON עם שדות: {answer: string, confidence: number, sources: list}"
- השתמש ב-Pydantic/Structured Outputs של OpenAI

**3. Guardrails:**
- Input validation: בדוק שהuser לא מנסה prompt injection
- Output validation: וולידציה שהfound עומד בtemplates ובheuristics
- Retry logic: אם הparse נכשל, נסה שוב עם הוראה לתיקון

**4. Prompt Versioning:**
- שמור prompts ב-version control
- Tag כל prompt version עם ביצועים
- A/B test prompts כמו features

**5. Evaluation Framework:**
- בנה eval set: שאלות + תשובות נכונות ידועות
- מדוד: correctness, format adherence, latency, cost
- הרץ evals לפני כל שינוי בprompt

**6. Prompt Injection Defense:**
כאשר user input חלק מה-prompt, מנע ניסיונות injection:
- Sanitize user input
- Use separate message roles (system/user/assistant)
- Validate שה-output לא "ברח" מהformat המצופה

**נקודות מפתח:**
- Production prompts = code — גרסאות, tests, monitoring
- Structured output = json_mode ב-OpenAI, Pydantic
- Prompt injection הוא security vulnerability אמיתי

## סיכום
Prompt Engineering הפכה ממיומנות ניסיונית לכישור הנדסי בשל. טכניקות כמו Few-Shot ו-Chain-of-Thought משפרות דרמטית את איכות התוצאות, ו-ReAct מאפשר ל-LLMs לפעול ב-environment דינמי עם כלים. בproduction, prompts צריכים להיות מנוהלים כcode — עם versioning, evals, ו-guardrails. בראיון, הראה שאתה מבין שprompts אינם "טריק" — הם ממשק תכנותי לשפות גדולות.

## מקורות להמשך לימוד
- Prompt Engineering Guide (promptingguide.ai)
- OpenAI Cookbook
- Chain-of-Thought Prompting — Wei et al. (2022)
- ReAct: Synergizing Reasoning and Acting — Yao et al. (2022)
