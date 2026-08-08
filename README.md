# Codex skills

This repository contains installable Codex skill packages.

## Available skills

- [`audhd-consulting-psychologist`](skills/audhd-consulting-psychologist/SKILL.md) — evidence-informed, neurodiversity-affirming conversational support for adults with co-occurring or suspected autism and ADHD.
- [`game-designer`](skills/game-designer/SKILL.md) — game design support.
- [`game-devops-operator`](skills/game-devops-operator/SKILL.md) — CI/CD, releases, infrastructure, observability, and live operations for games.
- [`unreal5-game-developer`](skills/unreal5-game-developer/SKILL.md) — Unreal Engine 5 development with low-end PC guidance.

The skill supports reflective conversation, emotional clarification, overload and burnout triage, executive-function problem solving, accommodation design, and preparation for professional care. It does not impersonate a licensed clinician, diagnose, prescribe, or replace emergency services.

## Install locally

From PowerShell, copy the complete package into the Codex skills directory:

```powershell
Copy-Item -Recurse -Force `
  .\skills\audhd-consulting-psychologist `
  "$env:USERPROFILE\.codex\skills\audhd-consulting-psychologist"
```

Restart or refresh Codex skill discovery after installation. Keep `SKILL.md` and its `references` directory together.

## Validate

```powershell
python .\scripts\validate_skill.py
```

The validator checks package structure, frontmatter, referenced files, the presence of required safety clauses, and fixture inventory. It does not certify clinical behavior. Behavioral cases and their reviewed response record are kept under [`tests/`](tests/).
