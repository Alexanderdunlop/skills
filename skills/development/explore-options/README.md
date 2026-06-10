# explore-options

A skill that forces Claude to stop, lay out 2-3 real approaches with tradeoffs, and wait for you to pick before writing any code — on work with a design choice in it.

## Why

The expensive failure in AI-assisted coding is not bad code. It's good code building the wrong thing fast. AI picks an implementation the moment you describe a task — usually a more complicated one than you'd have chosen — and runs with it. By the time you notice, you're 40 files into the wrong design and unwinding costs more than the original task would have.

Two real failures this skill prevents:

- **Guessed field names.** Asked to add search to a page that already had search elsewhere → AI invented filter shapes and column names instead of reading the existing one. Three iterations to get there.
- **Unprompted abstraction.** Built a closure-returning factory where plain module state would have done in a third of the code.

## Workflow

```
1. You describe a task with a design choice in it
2. Skill triggers (or you run /explore-options)
3. Claude greps and reads existing code first — non-negotiable
4. Lays out 2-3 genuinely different approaches with tradeoffs
5. Names what the choice depends on, if it hinges on something only you know
6. Recommends one and names the rejected siblings
7. Stops and waits for you to pick
8. Once you pick: autonomous execution, no permission-loop
```

## When it triggers

- The task introduces or reshapes a pattern, abstraction, or layer (factory, hook, service, data model, route shape)
- The task references a feature the codebase already has (search, auth, pagination, modal, form, table)
- You ask "how should I build / structure / approach X" — explicitly or by describing a problem without naming the implementation
- **Not** on mechanical changes — renames, dep bumps, formatter passes, one-line fixes. File count isn't the trigger; design choice is.

## What makes this different

- **Trace before theorise** — if the task references existing code, the skill reads it first. "Existing code I read first: none" is a self-caught violation when the task names a feature the repo already has.
- **Names what would flip the call** — when the recommendation hinges on something only you know (future plans, expected scale, roadmap), it frames conditionally ("A if more chain shapes are coming, B if the current set is stable") instead of guessing.
- **Names the rejected siblings** — you see what was considered and why it lost, not just the winner.
- **Not a permission-loop** — one upfront moment, then autonomous execution.

## What it doesn't do

- Ask permission for every edit after you've picked
- Manufacture fake alternatives when only one approach is sane after tracing
- Guess your roadmap to look confident
- Run on mechanical work — a 30-file rename has no design choice in it

## Usage

When you're about to start a task with a design choice in it:

```
/explore-options
```

Or just describe the task and the skill will trigger.
