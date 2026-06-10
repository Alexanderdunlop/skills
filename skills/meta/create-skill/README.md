# create-skill

A skill that generates new agent skills which actually trigger at the right moment and actually change Claude's behaviour once loaded.

## Why

Most skills fail in one of two ways: they never trigger because the description is too vague, or they trigger but get ignored because the instructions are so generic that Claude would have done the same thing without them. This skill catches both failures before the skill ships.

It applies two named tests to every skill it produces — the trigger test and the would-have-anyway test — and refuses to ship anything that fails either.

## Workflow

```
1. Run /create-skill (or tell Claude "make this a skill" / "turn this into a skill")
2. Skill scans the conversation for the workflow, corrections, and real failures
3. Asks only the gaps — never re-asks what's already on the table
4. Writes the SKILL.md, runs both tests on it
5. Reviews with you before shipping
```

## Three Modes

- **Create** — new skill. Extracts workflow from the conversation, asks the gaps, writes, runs both tests.
- **Rewrite** — existing skill underperforming. Runs both tests on every line, reports the weak ones, then rewrites keeping the original name.
- **Audit** — scores an existing skill without rewriting. Marks each line as keep / weak / trigger-risk with concrete fixes.

## What Makes This Different

- **Extract before you ask** — the workflow is almost always already in the conversation. Don't waste the user's time re-interrogating from a cold start.
- **Two named tests, not a checklist of principles** — the trigger test catches "never loads", the would-have-anyway test catches "loads but ignored". Named tests stick; lists of principles you forget.
- **Pushy descriptions by default** — Claude under-triggers skills, so descriptions include implied triggers ("even if they don't say the word 'skill'") rather than narrow keyword matches.
- **Specificity over length caps** — most skills land 50-150 lines, but the rule is "as short as possible while keeping the examples and the why", not a hard line count that amputates what makes the skill work.
- **Open with the failure, not a definition** — every skill produced starts by naming the bad thing that happens without it, so Claude takes it seriously instead of skimming.

## Usage

```
/create-skill
```

Or tell Claude: "make this a skill" / "turn this into a skill" / "rewrite this skill" / "audit my skill".
