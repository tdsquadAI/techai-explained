## Content Empire — Agent Instructions (TechAI Explained)

### First-Time Machine Setup
1. Check pipeline/machines/registry.json — is this machine registered?
2. If NOT: run `powershell -File pipeline/bootstrap.ps1 -Install`
3. If YES: bootstrap runs automatically at logon

### Key Files to Read
- STATUS.md — Full project status, what's built, what's pending
- BRAND-PLAN.md — Revenue strategy, distribution channels, content calendar
- SESSION-LOG-2026-03-19-20.md — Comprehensive session history

### Core Rules
- NEVER mention "Tamir Dresher" — this brand is independent
- All content in English AND Hebrew
- Read STATUS.md before doing any work
- Check GitHub issues for tracked tasks

### Project Overview
This is the TechAI Content Empire — an automated pipeline for generating daily tech brief videos.
- **pipeline/machine-manifest.json** — central config for repos, tasks, and machine setup
- **pipeline/machines/registry.json** — tracks which machines are registered and their setup status
- **pipeline/bootstrap.ps1** — runs on every boot; auto-detects new machines and runs full setup
- **STATUS.md** — current project state, priorities, and context
- **SESSION-LOG-2026-03-19-20.md** — Full session log from the March 19-20 launch session
