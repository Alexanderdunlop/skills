# test-interrogate

A skill that interrogates you on what tests to write after implementing a feature — without writing them for you.

## Why

Writing tests after the fact is easy to phone in. You merge a PR, slap on some happy-path tests, and move on. The edge cases, the subtle business logic, the assumptions baked into your if-statements — those slip through.

This skill fixes that by making you defend every testable decision in your diff before you write a single test. Think of it as a code review, but exclusively focused on test coverage and done *before* the tests exist.

## Workflow

```
1. Implement feature with Claude Code
2. Open / prepare PR
3. QA the PR yourself
4. Run /test-interrogate
5. Get interrogated one question at a time
6. Agreed cases tracked in /tmp/test-plan.md as you go
7. Confirm the full test plan
8. Tests get implemented all at once
9. Suite runs → failures triaged with you one at a time
```

## What it does

- Reads the diff against the base branch
- Identifies every testable surface: business logic, error paths, data transformations, integration points
- Asks one question at a time about intended behaviour and assumptions
- Tracks agreed cases in `/tmp/test-plan.md` as you go — nothing gets lost
- Suggests core test cases and challenges you on edge cases
- After all questions: prints the full plan and asks for confirmation
- Implements the full test plan in one pass
- Runs the suite and triages any failures with you:
  - **(a) Bug in implementation** → fixes the code
  - **(b) Bad test / wrong assumption** → fixes or removes the test
  - **(c) Missing requirement** → flags it for discussion, doesn't silently fix

## What it doesn't do

- Write test code during the interrogation phase — that comes after confirmation
- Skip ahead — it walks every branch of the decision tree sequentially
- Silently fix failing tests — every failure gets triaged with you first

## Usage

After your feature is ready and PR is up:

```
/test-interrogate
```

Or just tell Claude: "interrogate me on tests for this PR"

> **Note:** This skill doesn't just cover your new code. It also inspects the surrounding codebase and surfaces existing test gaps in code your changes touch or depend on.
