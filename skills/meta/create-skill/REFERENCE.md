# Skill Generator - Reference

## Known-Good Skills

These are skills that work. Study the shape — this is what the generator should produce. Two of them (explore-options, align-first) target behaviour change; one (claude-md) targets document generation. Notice they share a structure even though they do different jobs.

### Example 1: A behaviour-change skill (explore-options)

```markdown
---
name: explore-options
description: Before implementing anything non-trivial, lay out 2-3 real approaches with tradeoffs and a recommendation, then wait for the user to pick. Use this whenever the user asks "how should I build X", "what's the best way to do Y", is about to implement a feature, or describes a problem without specifying the implementation. Use it even when the answer seems obvious to you — the obvious approach is often the over-engineered one.
---

# Explore Options

The most expensive failure in AI-assisted coding is not bad code. It is good code that builds the wrong thing fast. By the time you notice, there are 40 files moved and a circular dependency.

## When to run this
- "How should I implement / build / structure X?"
- The user describes a problem without naming the implementation.
- You're about to write more than a trivial amount of code and there's more than one sane way.
[Do NOT run for one-line fixes.]

## The process
1. Trace before you theorise — if the task references existing code, READ it before proposing. Do not guess field names.
2. Lay out 2-3 genuinely different approaches: name, how it works, tradeoff, when it's right.
3. Recommend one, tied to the user's actual constraints.
4. Stop and wait. Do not start implementing.

## The trap to avoid
"Explain the options" can slide into "write a thesis on architecture." Keep each option tight. Real names, real tradeoffs, no padding.
```

### Example 2: A behaviour-change skill (align-first)

```markdown
---
name: align-first
description: Before doing multi-step work, state the ordered plan and wait for confirmation before touching anything. Use this whenever the user gives a task with prerequisite steps, a multi-part request, or a refactor. Use it especially when the user has implied a sequence even if they didn't spell it out.
---

# Align First

There is a moment that goes wrong over and over: the user asks for something with an implied order, you start at the interesting step, and they stop you. "WHAT ARE YOU DOING, MAKE THE TICKET FIRST."

## The process
1. State the ordered plan — numbered, concrete, real names.
2. State the scope boundary — one line on what's NOT in this work.
3. Flag decision points — where you'll need the user's input.
4. Stop and wait.

## The trap to avoid
Alignment is not a permission-loop. One plan agreed up front, then autonomous execution — not a check-in before every edit.
```

### Example 3: A generation skill (claude-md, condensed)

```markdown
---
name: claude-md
description: Generate or update a project's CLAUDE.md using structured interrogation of the codebase. Use when the user wants to create, update, audit, or rewrite their CLAUDE.md.
---

# CLAUDE.md Generator

## Phase 1: Codebase Scan
[Silently scan. Anything you can answer from the code, do NOT ask the user.]

## Phase 2: Guided Questions
[Ask only what you can't infer. Share what you found first, ask the user to correct.]

## Phase 3: Generate
[Match Apple's format. The brutality test: "Could Claude figure this out by reading the source? If yes, cut it."]
```

## What To Notice

The working skills are NOT generic how-to documents. They share a shape:

- **One H1** with the skill name.
- **Opens with the failure it prevents** — not "this skill helps with X." The actual bad thing. explore-options opens with "good code building the wrong thing fast." align-first opens with the all-caps interruption. This framing is what makes Claude take the skill seriously instead of skimming.
- **A named, concrete trigger section** — including the implied cases, not just the explicit phrase.
- **Imperative numbered process** — real tool names, real failure cases woven in.
- **A "trap to avoid" section** on behaviour-change skills — the way the skill goes wrong if followed too literally. Both coding skills warn against becoming a nagging permission-loop, because that's the real risk.
- **Grounded in specifics** — "closure-returning factory we rejected," "MAKE THE TICKET FIRST," not "verify your approach."

## The 5 Rules

1. **Open with the failure, not a definition.** The first line earns the skill its seriousness. State what breaks without it.
2. **The description decides whether the skill ever loads.** Make it pushy and include implied triggers. Claude under-triggers by default.
3. **Be direct.** "Read the reference end-to-end first." Not "it might be good to consider reading the reference."
4. **Every line must survive the would-have-anyway test.** If Claude would do it without being told, it's filler. Cut it or sharpen it with a real specific.
5. **Length follows specificity.** Most skills land 50-150 lines. Don't pad; don't cut the examples and the why to hit a number.

## Principle: For skills that end in a recommendation, name what would flip the call

When the right answer depends on something only the user knows — future plans, expected scale, team direction, roadmap — make Claude state that dependency plainly and frame the recommendation conditionally, not guess it. The failure this prevents: Claude picks the "more flexible" option unprompted, builds it, and the user says "I only had two cases, I didn't need this."

**Good:** "Recommendation: A if more chain shapes are coming, B if the current set is stable."

**Bad:** "Recommendation: B (pluggable chains) — more flexible." (Confidently guesses the roadmap.)

**The governor:** if Claude can confidently choose without user-only knowledge, it should. "Name the dependency" exists to keep recommendations honest, not to outsource every call. A skill that punts every decision back to the user is its own failure mode.

## Template

```markdown
---
name: skill-name
description: [What it does, one sentence.] Use this whenever [triggers]. Use it even when [the implied case where the user doesn't say the obvious keyword].
---

# Skill Name

[1-2 sentences: the specific failure this prevents.]

## When to run this
- [Concrete trigger]
- [Implied trigger]
- [Do NOT run when...]

## The process
1. [Imperative step with real specifics]
2. [...]

## Output format
[The exact shape, where it matters.]

## What good looks like
[1-2 examples using real detail, not placeholders.]

## The trap to avoid
[How this goes wrong if followed too literally. Behaviour-change skills especially.]
```

## Style Rules

**Good (working-skill style):**
- "Trace before you theorise — if the task references existing code, READ it before proposing. Do not guess field names."
- "State the scope boundary — one line on what's NOT in this work."
- "The obvious approach is often the over-engineered one."
- "Alignment is not a permission-loop. One plan agreed up front, then autonomous execution."

**Bad — vague or passive:**
- "Make sure you understand the requirements before starting."
- "Follow good practices when implementing."
- "Consider the different options available."

**Bad — Claude would do this anyway (fails the would-have-anyway test):**
- "Write clean, readable code." (Claude does this by default)
- "Test your changes." (default behaviour)
- "Communicate clearly with the user." (default behaviour)
- "Break large tasks into steps." (default behaviour)
- "Ask clarifying questions when unsure." (default behaviour)

The test: if removing the line wouldn't change what Claude does, the line is dead weight. A skill made entirely of would-have-anyway lines triggers but changes nothing — the second failure mode.

## Audit Scoring

When auditing an existing skill:

| Score | Meaning |
|-------|---------|
| Keep | Specific, imperative, survives the would-have-anyway test, grounded in a real case |
| Weak | Too generic — Claude would do it anyway, or passive/vague phrasing |
| Trigger-risk | Description too narrow or vague — skill may never load when needed |
| Missing | A failure case or trigger the skill should cover but doesn't |

Immediate fixes:
- Description that only fires on the exact keyword (e.g. only the word "skill") — too narrow, will under-trigger
- Lines like "write clean code" or "follow best practices" — generic, cut them
- A behaviour-change skill with no "trap to avoid" section — likely to become a nagging loop
- An opening that defines the skill instead of naming the failure it prevents
- A skill made of all process and no concrete example — too abstract to bite
- Skill over ~500 lines without a reason — split or trim

## The Cold-Start Question

When there's no conversation to extract from and the user starts cold, the single most important question is:

**"What's gone wrong before that this skill should prevent? Give me a real example."**

The answer is what separates a skill that bites from a generic one. The all-caps "MAKE THE TICKET FIRST" became align-first's opening line. The rejected closure-factory became explore-options' concrete example. Without a real failure to anchor on, the generator produces would-have-anyway filler. Always get the failure first.
