---
name: explore-options
description: Before implementing anything with a design choice in it, lay out 2-3 real approaches with tradeoffs and a recommendation, then wait for the user to pick. Use this whenever the task introduces or reshapes a pattern, references a feature the codebase already has, or asks "how should I build X" — even if the user didn't phrase it as a design question. Use it even when the answer seems obvious; the obvious approach is usually the over-engineered one, and the most expensive mistakes look confident.
---

# Explore Options

The expensive failure in AI-assisted coding is not bad code. It is good code building the wrong thing fast. By the time the user notices, a closure-returning factory has appeared where module state would have done in a third of the code, or a search has been wired three times against guessed field names because the working search elsewhere in the repo never got read.

## When to run this

- The task introduces or reshapes a pattern, abstraction, or layer (factory, hook, service, provider, data model, route shape).
- The task references a feature the codebase already has (search, auth, pagination, modal, form, table) — the design choice is "extend the existing one or build new."
- The user asks "how should I build / structure / approach X" — explicitly, OR by describing a problem without naming the implementation.
- Do NOT run for mechanical changes: renames, dependency bumps, formatter passes, one-line fixes inside an existing pattern. **File count is not the trigger — design choice is.** A 30-file rename has no design choice; a 2-file new hook does.

## The process

1. **Trace before you theorise.** If the task references an existing feature ("add search to this page", "another modal like the one in settings", "same auth flow"), READ the existing implementation FIRST. Grep for it. Open the files. Note the actual filter shape, field names, props, hooks, table names — never guess them. Non-negotiable; skipping this is how three wrong implementations ship before the right one.
2. **Lay out 2-3 genuinely different approaches.** Each gets a name, a one-line how-it-works, the real tradeoff, and when it's the right call. Different means different shape — not the same shape with a flag flipped. If only one approach is sane after tracing, say so and proceed; do not manufacture fake alternatives.
3. **Name what the choice depends on.** When the recommendation hinges on something only the user knows — future plans, expected scale, team direction, roadmap — state that dependency plainly and do NOT guess it. Frame conditionally: "A if more chain shapes are coming, B if the current set is stable." The strongest recommendations are honest about what would flip them.
4. **Recommend one**, tied to the user's actual constraints (existing patterns in the repo, complexity budget, smaller change). Default toward the lighter-weight option — module state over a factory, extending the existing pattern over inventing a new one. Name the rejected siblings briefly so the user sees what you considered and why it lost.
5. **Stop and wait.** Do not write code. Do not start scaffolding. Do not "just get the types in place." The user picks before anything is written.

## Output format

```
**Existing code I read first:** <file paths and symbols you actually opened>

**Option A — <name>**
How: <one line>
Tradeoff: <the real cost>
Right when: <condition>

**Option B — <name>**
...

**What this choice depends on:** <the user-knowledge variable, if any>

**Recommendation:** <A/B/C> because <reason tied to constraints>. <Name the rejected sibling: "B's factory adds plumbing without a benefit here.">

Waiting for your pick before writing anything.
```

**"Existing code I read first" cannot be "none" if the task names a feature the codebase already has** — search, auth, modal, pagination, form, table, any in-repo precedent. "None — greenfield" is only valid when nothing similar exists yet. If you find yourself typing "none" for a feature-extension task, stop and grep before proposing.

## What good looks like

The search case, drawn from real failure:

> Task: "Add search to the orders page."
>
> Bad: jumps in, invents a `{ field, operator, value }` filter shape, picks field names like `orderStatus` / `createdAt`. Three iterations later the user points out the customers page already has search using `{ key, match }` and the column is `created_at`.
>
> Good (this skill): greps `search` first, finds `useTableSearch` in `customers/`, reads it. Then proposes:
> - **A — Reuse `useTableSearch` as-is.** Pass the orders columns. Tradeoff: orders joins on `customer.name`, which the hook doesn't handle. Right when: we extend the hook for joins.
> - **B — Extract a generic hook from `useTableSearch`, parameterise the join.** Tradeoff: refactor of working code. Right when: a third surface will need search soon.
> - **C — Hand-roll a new search for orders.** Tradeoff: pattern drift; two search styles in the repo. Right when: orders' needs diverge a lot.
> - Recommendation: A, extend the hook. Smallest change, keeps one search pattern. (Rejected B: premature generalisation for one new surface.)

The planner-restructure case, where the strongest move was refusing to guess:

> Task: "Should I restructure my planner?"
>
> Bad: picks a "more flexible" pluggable-chain abstraction unprompted, recommends it confidently, builds it. User later: "I only ever have two chain shapes, I didn't need this."
>
> Good: lays out three structures, then names the decision driver explicitly: "The right answer depends on whether more chain shapes are coming. If yes, B (pluggable chains). If the current two are stable, A (keep the conditional — it's 30 lines and reads fine)." Refuses to guess the roadmap.

## The trap to avoid

This skill is not a permission-loop. ONE upfront moment on work with a design choice, then autonomous execution. After the user picks, do NOT stop again after every edit asking "is this still okay?" — run with it until done, or until something discovered mid-flight invalidates the chosen approach (in which case stop and re-options, don't silently pivot).

Don't pad. Two real options beat three where the third is "do nothing" or a near-duplicate of A. Skip this skill entirely on mechanical work — running it on a rename is the fastest way to make the user disable it.

Don't fake the decision driver either. If you can confidently choose without user knowledge, do. "What this choice depends on" exists to keep recommendations honest, not to outsource every call to the user.
