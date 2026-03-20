# Video 3: "From Zero to 21 Games in 24 Hours with AI Agent Teams"
**Channel:** TechAI Explained
**Duration:** 10–12 minutes
**Style:** Case study with gameplay footage, terminal recordings, and data visualizations

---

## INTRO (0:00–1:00)

[VISUAL] Rapid montage of HTML5 games running in browsers — a platformer, a space shooter, a puzzle game, a 3D racing game. Numbers counting up: 1, 5, 10, 15, 21. Clock showing 24 hours passing.

[NARRATION] Twenty-one games. Twenty-four hours. Zero human-written lines of code. This is the story of how I used Squad — the AI agent team framework — to build an entire game studio's worth of HTML5 games in a single day. 2D platformers, puzzle games, tower defense, even 3D games with Three.js. All published live on itch.io. And the wild part? It didn't stop at games. The same agent team generated articles, video scripts, and course content for every single one. This is the JellyBolt Games experiment, and I'm about to break down exactly how it worked.

---

## THE SETUP (1:00–2:30)

[VISUAL] Show a clean project directory. Terminal: `squad init`. The `.squad/` folder appearing.

[NARRATION] The setup was simple. I created a monorepo with a `games/` directory and initialized Squad. But here's where it gets interesting — I didn't use the default team configuration. I customized the team specifically for game development.

[VISUAL] Show customized `team.md` with game-specific roles:
```
## Team Roster
- Lead (Keaton) — Game Design & Architecture
- Frontend (McManus) — HTML5/Canvas/Three.js Implementation
- Backend (Verbal) — Game Logic & State Management
- Tester (Fenster) — QA & Gameplay Testing
- Scribe (Kobayashi) — Documentation & Publishing
```

[NARRATION] Keaton became the game designer — defining mechanics, level structure, and player experience. McManus handled the actual HTML5 implementation — Canvas for 2D, Three.js for 3D. Verbal managed game logic and state. Fenster became QA, testing for bugs, checking frame rates, validating controls. And Kobayashi handled documentation and itch.io publishing metadata.

[VISUAL] Show `routing.md` with game-specific routing rules.

[NARRATION] I set up the routing so that when I said "build a platformer," the coordinator knew exactly how to distribute the work. Game design to Keaton. Rendering to McManus. Physics and collision to Verbal. Playtest checklist to Fenster.

---

## THE PARALLEL DEVELOPMENT STRATEGY (2:30–4:00)

[VISUAL] Animated timeline showing multiple games being developed simultaneously, with colored bars for each agent.

[NARRATION] Here's the key insight that made 21 games possible: parallel development. I didn't build games one at a time. I batched them.

[VISUAL] Show the terminal with multiple agent spawns:
```
Batch 1: Games 1-3
🎮 Keaton — designing "Neon Runner" (platformer)
🎮 McManus — implementing "Neon Runner" canvas engine
🎮 Keaton — designing "Star Drift" (space shooter)
🎮 McManus — implementing "Star Drift" particle system
🎮 Keaton — designing "Block Logic" (puzzle game)
```

[NARRATION] I'd kick off a batch of three games at once. Keaton would design all three in parallel — defining game mechanics, controls, scoring systems. Then McManus would implement each one while Keaton moved on to designing the next batch. Verbal would wire up game state management, Fenster would test completed games, and Kobayashi would write the itch.io descriptions and README files.

[VISUAL] Show a Gantt-chart-style visualization of the 24-hour period with games progressing through stages.

[NARRATION] It was like a production pipeline. While games 4 through 6 were being implemented, games 1 through 3 were being tested. While games 7 through 9 were being designed, games 4 through 6 were getting polish. Every agent was always busy.

---

## THE GAMES (4:00–6:30)

[VISUAL] Quick showcase of games with gameplay footage. 3-4 seconds each, with game title and type overlaid.

[NARRATION] Let me show you what came out of this. We had 2D games built with HTML5 Canvas — platformers with pixel art, space shooters with particle effects, puzzle games with drag-and-drop mechanics. Simple but functional and genuinely fun to play.

[VISUAL] Show a platformer game running. Character jumping, collecting items, avoiding obstacles.

[NARRATION] "Neon Runner" was a side-scrolling platformer with procedurally generated levels. McManus implemented smooth pixel movement, gravity physics, and collision detection all in vanilla Canvas. No game engine.

[VISUAL] Show a 3D game running. Camera rotating around a scene.

[NARRATION] Then we leveled up to 3D. Using Three.js, the team built racing games, a first-person maze explorer, and a 3D tower defense game. These were more complex — Verbal had to handle 3D collision detection, camera systems, and 3D asset generation using procedural geometry.

[VISUAL] Show a puzzle game. Colorful blocks being matched and cleared.

[NARRATION] The puzzle games were probably the most polished — "Chromatic" was a color-matching game with satisfying animations, combo scoring, and progressive difficulty. Clean code, smooth gameplay, responsive controls.

[VISUAL] Quick montage of all 21 game titles with thumbnails.

[NARRATION] In total: 8 platformer and action games, 5 puzzle games, 4 3D games, and 4 arcade-style games. Every single one playable in a browser. Every single one published to itch.io with proper descriptions, screenshots, and tags.

---

## THE DECISION LOG (6:30–7:30)

[VISUAL] Show `decisions.md` scrolling — dozens of entries from across the 24-hour period.

[NARRATION] One of the most fascinating artifacts from this experiment was the decision log. Remember, every time an agent makes a significant choice, it's recorded in `decisions.md`. After 24 hours, we had a massive log of architectural decisions.

[VISUAL] Highlight specific entries:
```
Decision: Use requestAnimationFrame for game loops
Author: McManus
Reason: Consistent 60fps, battery-friendly, auto-pauses in background tabs

Decision: Standardize game state as { score, lives, level, entities[] }
Author: Verbal
Reason: Consistent interface lets Fenster write reusable test harness

Decision: All games must support keyboard + touch
Author: Keaton
Reason: itch.io audience includes mobile players
```

[NARRATION] Look at this — McManus decided early on to standardize the game loop pattern using requestAnimationFrame. That decision cascaded to every subsequent game. Verbal standardized the game state shape, which meant Fenster could write a reusable test harness. Keaton mandated keyboard plus touch support because itch.io has mobile players. These weren't random — they were informed decisions that got better as the team learned.

---

## THE CONTENT EMPIRE EXPANSION (7:30–9:00)

[VISUAL] Show a spreadsheet or dashboard showing: 21 games + articles + video scripts + course modules.

[NARRATION] But here's where this experiment went from impressive to insane. I didn't just build games. I built a content empire around them. For each game, Kobayashi — the scribe — generated an article breaking down how the game was built. Technical deep-dive, code highlights, design decisions.

[VISUAL] Show an article titled "Building a Procedural Platformer in HTML5 Canvas" with code snippets and diagrams.

[NARRATION] Then I had the team generate video scripts for game development tutorials. "How to build a 3D maze game with Three.js in 30 minutes." Each script follows our video format with VISUAL and NARRATION markers.

[VISUAL] Show a folder structure:
```
content/
├── games/          # 21 games
├── articles/       # 21 game dev articles
├── video-scripts/  # Tutorial scripts
└── courses/        # Course modules
```

[NARRATION] And finally, I generated course modules. Five modules on HTML5 game development, using our actual games as examples. Lessons, exercises, quizzes — all based on real code the team wrote. One experiment generated enough content to fuel a YouTube channel, a blog, and a course platform for months.

---

## LESSONS LEARNED (9:00–10:30)

[VISUAL] Numbered list appearing one at a time with icons.

[NARRATION] After 24 hours with an AI game studio, here are the biggest lessons.

[VISUAL] Show: "1. Batch work, don't serialize it"

[NARRATION] Lesson one: batch your work. Don't ask the team to build one game at a time. Give them three games in parallel. The pipeline stays full, agents stay busy, and you get 3x throughput.

[VISUAL] Show: "2. Standardize early"

[NARRATION] Lesson two: standardize early. The best decision we made was establishing a common game state shape in game two. Every game after that was faster because agents knew the pattern.

[VISUAL] Show: "3. Let knowledge compound"

[NARRATION] Lesson three: let knowledge compound. Game 21 was significantly better than game 1 — not because I gave better instructions, but because the agents had 20 games worth of learnings in their history files. They knew what worked.

[VISUAL] Show: "4. Quality varies — and that's OK"

[NARRATION] Lesson four: quality varies. Some games were great. Some were mediocre. A couple needed manual fixes. That's fine — the point isn't perfection, it's velocity. Ship fast, iterate on what works.

[VISUAL] Show: "5. Content multiplication is the real power"

[NARRATION] Lesson five — and this is the big one: content multiplication is the real superpower. One game becomes an article, a tutorial, a course module. The AI team doesn't just build — it documents, teaches, and publishes. That's where the compounding really kicks in.

---

## OUTRO & CTA (10:30–11:15)

[VISUAL] Show the full collection of 21 games on an itch.io page. Zoom out to show the broader content ecosystem.

[NARRATION] Twenty-one games in twenty-four hours. Plus articles, scripts, and course content for each one. All powered by Squad and a team of AI agents named after movie characters. If you want to try this yourself, Squad is free and open source — link in the description.

[VISUAL] Show course thumbnail: "Mastering AI Agent Teams with Squad"

[NARRATION] I've also put together a full course on mastering Squad — from installation to running your own autonomous content pipeline. Five modules, hands-on exercises, real configurations. Check the link in the description for that too.

[VISUAL] End card with: subscribe, Squad repo link, course link, itch.io games link.

[NARRATION] Smash that subscribe button if you want more experiments like this. I'm planning to push this even further — maybe an entire SaaS product built by AI agents. What do you think? Let me know in the comments. See you in the next one!

---

## VIDEO METADATA

**Title:** From Zero to 21 Games in 24 Hours with AI Agent Teams
**Description:** What happens when you give an AI agent team 24 hours and tell them to build as many games as possible? The answer: 21 HTML5 games (2D + 3D), all playable, all published to itch.io — plus articles, video scripts, and course content for each one. This is the JellyBolt Games experiment using Squad, the open-source AI agent team framework.

🔗 Squad on GitHub: https://github.com/bradygaster/squad
🎮 JellyBolt Games on itch.io: [link]
📚 Squad Mastery Course: [link]
📦 Install: npm install -g @bradygaster/squad-cli

**Tags:** ai game development, html5 games, ai agent teams, squad framework, game dev challenge, 24 hour challenge, three.js games, canvas games, autonomous ai, content creation ai, itch.io publishing, ai coding challenge
