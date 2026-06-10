---
name: create-skill
description: Create a new agent skill that actually triggers and actually changes behaviour. Use this whenever the user wants to create, write, build, or rewrite a skill, says "turn this into a skill" or "make this a skill", or describes a repetitive workflow they keep re-explaining to Claude. Use it even when they don't say the word "skill" but are clearly describing a reusable process they want followed consistently.
---

# Skill Generator

## Quick start

Run this skill to produce a SKILL.md that passes two bars: it triggers at the right moment, and once loaded it changes what Claude does. Most skills fail one of those two. This skill is built to catch both failures before the skill ships.

## The two ways a skill fails

Hold these in mind the whole time. Everything in this skill serves one of them.

1. **It never triggers.** The description is too vague or too narrow, so Claude never loads it when it would help. Claude under-triggers skills by default, so this is the common one.
2. **It triggers but gets ignored.** The instructions are so generic that Claude would have done the same thing without the skill. A skill that only says what Claude already does is dead weight.

## The two tests

Apply these to everything you write. They are the core of this skill.

**The trigger test** (catches failure 1): Read only the description, as if you were Claude seeing it in a list of twenty skills. Would you know to pick it for the cases it's meant for — including the ones where the user doesn't say the magic word? If the description only fires on the exact word "skill" or the exact phrase the user used, it's too narrow. Widen it and lean pushy.

**The would-have-anyway test** (catches failure 2): For every instruction line, ask: "Would Claude have done this without being told?" If yes, the line is generic filler. Either make it specific enough to bite, or cut it. "Write clean code" — Claude would do that anyway, cut it. "Prefer module-private state over closure-returning factories, we rejected the factory version" — Claude would NOT reliably do that, keep it. This is the brutal one. Most weak skills are 80% lines that fail it.

## Process

### Phase 1: Extract before you ask

The workflow is usually already in front of you. The user said "make this a skill" because they just did the thing or just explained it. Before asking anything, pull from the conversation:

- The actual steps, in the order they happened
- Real tool names, file names, commands, numbers
- Every correction the user made — a correction is a rule the skill should encode
- The specific failures or frustrations that motivated this — these become the "why" and the concrete examples

The bar for asking a question: if the conversation already answers it, don't ask. If there is no conversation to draw on and the user is starting cold, then ask — but ask for the specifics that make a skill bite: "What's gone wrong before that this should prevent? Give me a real example."

### Phase 2: Ask only the gaps

Share what you extracted first — "Here's the workflow I picked up:" — and let the user correct it. Then ask only what's missing:

- When exactly should this trigger? What phrases, what contexts, what implied cases?
- Any real footgun or failure case I should encode? (This is the most important question. Generic skills come from skipping it.)
- Does it need a script, or just instructions?

### Phase 3: Write the SKILL.md

Before writing, read [REFERENCE.md](REFERENCE.md) — it holds three working skills to imitate, the good/bad line pairs, and the audit scoring table. Match the shape of the examples there. Then follow the structure below, and run both tests on the result before showing the user.

### Phase 4: Review

Present the draft and ask: does the description trigger at the right times, is anything in here something Claude would do anyway, is the real failure case captured.

## SKILL.md structure

```md
---
name: skill-name
description: [What it does, one sentence.] Use this whenever [triggers, including implied ones]. Use it even when [the case where the user doesn't say the obvious keyword].
---

# Skill Name

[1-2 sentences: the specific failure this skill prevents. Not "helps with X" —
the actual bad thing that happens without it. This is what makes Claude take
it seriously instead of skimming.]

## When to run this

[Concrete triggers, including the implied cases.]

## The process / The rules

[Imperative, specific, grounded in real detail.]

## Output format

[The exact shape, where output shape matters.]

## What good looks like

[1-2 examples using real specifics, not placeholders.]

## The trap to avoid

[How this skill goes wrong if followed too literally. Optional but valuable
for behaviour-change skills — e.g. an "align before acting" skill must warn
against becoming a permission-loop.]
```

## Hard rules

- **Open with the failure, not a definition.** The first line after the H1 says what goes wrong without the skill. "The expensive failure isn't bad code, it's good code building the wrong thing fast" beats "This skill helps explore options."
- **Imperative voice.** "Read the reference end-to-end first," never "it might be good to consider reading the reference."
- **Description leans pushy and includes implied triggers.** "Use this whenever the user mentions diagrams OR wants to visualise a process, even if they don't say 'diagram'." Under-triggering is the default failure.
- **Every instruction must survive the would-have-anyway test.** Specific footguns, real tool names, actual rejected approaches. No generic best-practice filler.
- **Length follows specificity, not a cap.** As short as possible while keeping the examples and the why. Most land 50-150 lines. Don't pad; don't amputate the parts that make it work to hit a number.
- **No time-sensitive info** that will go stale (current model names, "the latest version of X").
- **One named example beats three abstract rules.** If you're explaining a rule, show the real case it came from.

## Modes

**Create** — new skill. Extract from conversation, ask the gaps, write, run both tests.

**Rewrite** — existing skill underperforming. Read it, run both tests on every line, and report: which lines fail the would-have-anyway test (candidates to cut or sharpen), whether the description fails the trigger test, and what real specifics are missing. Then rewrite, keeping the original name unchanged.

**Audit** — score an existing skill without rewriting. For each line, mark: keeps (specific, survives both tests), weak (too generic, would-have-anyway), or trigger-risk (description too narrow/vague). Summarise with concrete fixes.

## What good looks like

A weak skill line: "Before implementing, make sure you understand the requirements." Claude would do this anyway — fails the would-have-anyway test. Cut it.

A strong skill line, same intent: "Before writing code, lay out 2-3 real approaches with tradeoffs and wait for the user to pick — the failure this prevents is Claude confidently building the wrong thing fast, which costs far more than the two-minute pause." Specific, names the failure, Claude does NOT do this by default. Keep it.

A weak description: "Helps create diagrams." Fails the trigger test against any other visual skill.

A strong description: "Create flowcharts, architecture diagrams, and process visuals. Use this whenever the user wants to see how something works, mentions a diagram or flowchart, or describes a system with moving parts — even if they don't ask for a diagram explicitly."
