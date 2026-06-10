---
name: audit-skill
description: Score an existing SKILL.md line-by-line and flag the dead weight using the would-have-anyway and trigger tests. Use this whenever the user wants to audit, review, score, or sanity-check a skill, says "is this skill any good" or "why isn't this triggering", or hands you a skill file expecting a verdict. Use it even when they don't say "audit" — if they're staring at a skill file asking what's wrong with it, this is the job.
---

# Audit Skill

The failure: someone writes a skill, it triggers, and nothing changes. Every line feels like instruction, so they can't see which ones Claude would have followed anyway. This skill makes the dead weight visible with a number they can't argue with.

## When to run this

- "Audit / score / review this skill"
- "Why isn't this firing?" / "It triggers but nothing changes"
- The user shares a SKILL.md and asks if it's any good
- A freshly written skill, as a self-check before shipping
- Do NOT use this to rewrite — that is [[create-skill]]'s job. Audit ends at the verdict.

## The two tests

1. **Would-have-anyway** — for each instruction line, ask: would Claude have done this without the line? If yes, it's filler. "Write clean code" → yes, cut. "Prefer module-private state over the closure-returning factory we rejected last sprint" → no, keep.
2. **Trigger** — read only the description. Would Claude pick this skill from a list of twenty, including the implied cases where the user doesn't say the magic word? If it only fires on the literal keyword, it's Trigger-risk.

## The process

1. Read the whole SKILL.md first. A line that looks generic may be load-bearing when paired with a specific example two lines down — don't score in isolation.
2. Score the description against the trigger test.
3. Score every instruction line against the would-have-anyway test. Skip markdown headers, the opening failure statement, and pure prose framing — only judge lines that are meant to change behaviour.
4. Note what's Missing — no "trap to avoid" on a behaviour-change skill, opening that defines instead of naming a failure, no concrete example, no implied triggers in the description.
5. Count the kill. Lines scored, lines that survived as Keep.

## Scoring

| Score | Meaning |
|-------|---------|
| Keep | Specific, imperative, survives the would-have-anyway test, grounded in a real case |
| Weak | Claude would do it anyway, or passive/vague |
| Trigger-risk | Description too narrow or vague — skill may never load when needed |
| Missing | A failure case, trigger, or section the skill should have but doesn't |

## Output format

Open with the headline. Make it quotable and a little brutal — that number is the point.

```
23 lines. 6 survived.
```

Then:

**Description:** Keep / Trigger-risk — one-line why.

**Line-by-line:**
- `Line N` — Keep / Weak — one-line why.

**Missing:**
- (e.g.) No "trap to avoid" — behaviour-change skill, will become a nagging loop.
- (e.g.) Opens with a definition, not the failure it prevents.

No rewrites. No suggested replacements beyond what's needed to explain a Weak verdict. If the user wants the rewrite, point them at [[create-skill]] in rewrite mode.

## What good looks like

`Line 14 — Weak — "Test your changes before committing." Claude does this by default.`

`Line 22 — Keep — names the closure-factory rejection, Claude would not infer this.`

`Description — Trigger-risk — only fires on the literal word "diagram", misses "show me how this works" / "visualise the flow".`

## The trap to avoid

Don't be diplomatic. A skill with 6 surviving lines out of 23 needs to hear that, not "lots of good intent here." The brutality is the value — the user asked for the verdict because they want to act on it. The other trap: scoring prose framing and the opening failure statement as instructions. Those are judged under Missing (does the opening name a failure or just define the skill?), not line-by-line.
