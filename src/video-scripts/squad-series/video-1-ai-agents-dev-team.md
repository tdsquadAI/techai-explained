# Video 1: "I Let AI Agents Run My Entire Dev Team — Here's What Happened"
**Channel:** TechAI Explained
**Duration:** 8–10 minutes
**Style:** Fast-paced developer walkthrough with screen recordings

---

## INTRO (0:00–0:45)

[VISUAL] Quick montage: terminal windows spawning, code appearing in editors, pull requests merging — all happening simultaneously. Cut to host on camera.

[NARRATION] What if you could say "build me a login page" and five AI agents — each with their own personality, memory, and expertise — just… did it? Not one chatbot pretending to be five people. Five separate agents, running in parallel, sharing decisions, and learning from each other. Today I'm going to show you Squad — an open-source framework that gives you an AI development team through GitHub Copilot. And yes… every agent is named after a character from a movie. Let's get into it.

---

## WHAT IS SQUAD? (0:45–2:30)

[VISUAL] Show the Squad GitHub repo (github.com/bradygaster/squad). Highlight the tagline: "AI agent teams for any project. One command."

[NARRATION] Squad was created by Brady Gaster, and it's beautifully simple in concept. You install it into your project, and it scaffolds an entire AI team — a lead engineer, frontend specialist, backend specialist, tester, and a scribe — right into your repo as markdown files.

[VISUAL] Show the `.squad/` directory structure in a file explorer. Zoom into `team.md`, `routing.md`, `decisions.md`.

[NARRATION] Each agent has its own charter — that's like its job description, personality, and voice. They have their own history files where they remember what they've learned about YOUR project. And here's what makes it different from just prompting ChatGPT with "pretend you're a frontend developer" — each agent runs in its own execution context. They read only their own knowledge. They write back what they learned. And all of it lives in git.

[VISUAL] Show the `agents/` folder with individual agent directories, each containing `charter.md` and `history.md`.

[NARRATION] When someone clones your repo, they get the team. With all the accumulated knowledge. That's wild.

---

## THE CASTING SYSTEM (2:30–3:30)

[VISUAL] Show `casting/policy.json` — highlight the "universe" field. Show example cast from The Usual Suspects.

[NARRATION] Here's one of my favorite parts — the casting system. Squad doesn't give you boring names like "Agent-1" or "Frontend-Bot." It casts your agents from movie universes. The default? The Usual Suspects. So your lead is Keaton. Your frontend engineer is McManus. Your backend is Verbal. Your tester is Fenster.

[VISUAL] Show a split screen of agent names mapped to roles.

[NARRATION] Why does this matter? Because names are memorable. You start saying "Keaton handles the architecture decisions" instead of "the lead agent." You build a relationship with these agents over time. And when you add a sixth agent? They get cast from the same universe. The identity carries forward. It sounds silly, but it works.

---

## THE DEMO: "Build Me a Login Page" (3:30–6:30)

[VISUAL] Terminal: `copilot --yolo`, then typing the command to Squad.

[NARRATION] Alright, let's see this in action. I'm going to start Copilot with the `--yolo` flag — which auto-approves tool calls so we don't get interrupted — and I'm going to ask the team to build a login page.

[VISUAL] Type: `Team, build the login page with email/password auth`

[NARRATION] Watch what happens. The coordinator reads the request and immediately fans out to multiple agents — simultaneously.

[VISUAL] Show the terminal output with parallel agent spawning:
```
🏗️ Keaton — analyzing requirements...
⚛️ McManus — building login form...
🔧 Verbal — setting up auth endpoints...
🧪 Fenster — writing test cases from spec...
📋 Kobayashi — logging everything...
```

[NARRATION] Keaton, the lead, breaks down the requirements. McManus starts on the React login form. Verbal spins up the authentication endpoints on the backend. Fenster is already writing test cases based on the spec — before the code even exists. And Kobayashi? The scribe. Silently logging every decision to `decisions.md` so the team has a shared brain.

[VISUAL] Show `decisions.md` being updated in real-time with entries like "Decision: Use bcrypt for password hashing. Author: Verbal. Reason: team expertise, battle-tested library."

[NARRATION] This is the part that blew my mind. When Verbal decides to use bcrypt for password hashing, that decision gets written to the shared decisions file. Now when McManus is building the login form, it knows what auth strategy the backend chose — without anyone having to coordinate manually.

[VISUAL] Show the completed files: `LoginForm.tsx`, `auth.ts` routes, `login.test.ts`.

[NARRATION] In about two minutes, we have a login form component, authentication API endpoints, and test coverage. All created by different agents, all consistent with each other, because they share a decision log.

---

## KNOWLEDGE COMPOUNDS (6:30–7:30)

[VISUAL] Show `history.md` files for different agents with accumulated learnings.

[NARRATION] Here's the thing that makes Squad genuinely different from just asking an AI to write code. Knowledge compounds across sessions. Every time McManus works on your project, it writes its learnings to `history.md`. "This project uses Tailwind v4." "Dark mode is stored in theme.config.ts." "The design system uses shadcn components."

[VISUAL] Show a before/after of agent history — empty file vs. rich context file.

[NARRATION] After a few sessions, your agents know your conventions, your preferences, your architecture. They stop asking questions they've already answered. They get BETTER the more you use them. And because it's all in git, this knowledge transfers to anyone who clones the repo.

---

## THE HOOK PIPELINE (7:30–8:30)

[VISUAL] Show code snippets of the HookPipeline with file-write guards and PII scrubbing.

[NARRATION] Now, giving AI agents freedom to write code sounds scary, right? Squad handles this with what they call the Hook Pipeline. These are code-level guardrails — not prompt-level suggestions.

[VISUAL] Show the `allowedWritePaths` configuration.

[NARRATION] You define which directories agents can write to. If an agent — compromised or confused — tries to write outside those paths? Blocked. Not because we asked nicely in a prompt. Because code won't let it. There's also PII scrubbing, reviewer lockouts — if a tester rejects code, the original author can't sneak a fix in — and rate limiting on how often agents can ask you for help.

---

## OUTRO & CTA (8:30–9:00)

[VISUAL] Show the Squad GitHub repo, star count, installation command.

[NARRATION] Squad is open source and in alpha right now. You can install it with `npm install -g @bradygaster/squad-cli` and run `squad init` in any project. It works with GitHub Copilot — both the CLI and VS Code.

[VISUAL] Show on screen: `npm install -g @bradygaster/squad-cli && squad init`

[NARRATION] I'm going to be doing a deep dive on Ralph — the autonomous work monitor — in the next video. Ralph watches your GitHub issues and keeps shipping code while you sleep. If that sounds insane, that's because it kind of is. Subscribe so you don't miss it, and drop a comment telling me — what would YOU build with an AI dev team? See you in the next one.

[VISUAL] End card with subscribe button, link to Squad repo, and next video thumbnail.

---

## VIDEO METADATA

**Title:** I Let AI Agents Run My Entire Dev Team — Here's What Happened
**Description:** What happens when you give five AI agents their own identities, memories, and expertise — then tell them to build a login page? Meet Squad, the open-source framework that gives you an AI dev team through GitHub Copilot. Each agent has a name from a movie, runs in its own context, shares decisions with teammates, and gets smarter the more you use it.

🔗 Squad on GitHub: https://github.com/bradygaster/squad
📦 Install: npm install -g @bradygaster/squad-cli

**Tags:** ai agents, ai development team, squad framework, github copilot, ai coding, autonomous agents, multi-agent systems, ai programming, developer tools, open source ai
