# claude-md

A skill that generates, updates, or audits your project's CLAUDE.md by scanning the codebase and asking you guided questions.

## Why

Most CLAUDE.md files are either empty, full of vague "follow best practices" filler, or a 500-line dump that Claude stops reading after the first screen. Apple's internal CLAUDE.md files show what good looks like: imperative, specific, architecture-focused, and under 200 lines.

This skill applies those patterns to any project. It scans first, asks second, and writes a CLAUDE.md that actually changes how Claude works in your codebase.

## Workflow

```
1. Run /claude-md (or tell Claude "generate my CLAUDE.md")
2. Skill silently scans your codebase
3. Shares what it found, asks guided questions about the rest
4. Generates CLAUDE.md following Apple's patterns
5. Reviews with you before writing
```

## Three Modes

- **Generate** — new project, no CLAUDE.md yet. Full scan + questions + write.
- **Update** — existing CLAUDE.md. Diffs current file against what the scan reveals, proposes changes.
- **Audit** — scores each section, flags secrets, vague instructions, and bloat.

## What Makes This Different

- **Scan first, ask second** — doesn't waste your time on things it can figure out from `package.json` and directory structure
- **Guided questions** — offers what it found and asks you to confirm or correct, not open-ended "describe your architecture"
- **Apple's actual format** — one heading, flat bullet list, no section headers. Matches their leaked files exactly, not a structured template with "Architecture" / "Commands" / "Conventions" sections
- **200 line hard cap** — Claude's adherence drops on longer files, so the skill enforces the budget
- **Secrets detection** — scans for API keys, connection strings, and credentials before writing

## Usage

After your project has code in it:

```
/claude-md
```

Or tell Claude: "generate my CLAUDE.md" / "audit my CLAUDE.md" / "update my CLAUDE.md"
