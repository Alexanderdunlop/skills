---
name: slop-audit
description: Audit a codebase for the places where agents write slop, and name the strongest check that can stop each one. Walks 12 steps from measurement through codebase, static analysis, verification and prose, and writes a dated report with numbers to track month by month. Use when the user says "slop audit", "audit this codebase for agents", "why do agents keep getting this wrong", or wants to make a repo safer for AI-written code.
---

# Slop Audit

Agents copy the code around them. Every place that needs judgment, and every rule held only in prose, is a place where slop gets in. This skill finds those places and names a check for each. It does not fix them.

## Quick start

1. Run `bash <skill-dir>/scripts/probe.sh <src-dirs>` from the repo root.
2. Walk the 12 steps in [REFERENCE.md](REFERENCE.md), using the probe output as evidence.
3. Write the report to `docs/slop-audit/YYYY-MM-DD.md`.
4. Ask the user to pick one finding to act on.

## The ladder

Each finding gets the strongest rung that can hold it. A weaker rung becomes the next template agents copy.

1. **Codebase** — the wrong state cannot exist: types, API shape, architecture, one canonical helper.
2. **Static analysis** — the wrong code fails CI: lint rule, banned API, type check, test.
3. **Verification** — a runtime or formal check finds what is left: E2E, property, model checking.
4. **Prose** — rules, skills, AGENTS.md. Only for real judgment calls.

## Process

### Phase 1: Probe

- [ ] Read CLAUDE.md, AGENTS.md, lint config, CI workflows, and the test setup.
- [ ] Find a correction log, if one exists. Pass it as `CORRECTIONS=<file>`. If there is none, search the Claude Code session history for this repo (see Step 2 in [REFERENCE.md](REFERENCE.md)). If that is empty too, say so under Step 2 and move on.
- [ ] Add stack-specific nuance APIs with `NUANCE='api1|api2'`.
- [ ] Run the probe script. Keep the output.
- [ ] Find the last report in `docs/slop-audit/`. You compare against it.

### Phase 2: Walk the 12 steps

Follow [REFERENCE.md](REFERENCE.md). For each step, record:

- the audit question,
- the evidence: a number, a file list or a quote from config,
- the rung that could hold the finding, or "No finding", or "Skipped" and why.

Read code before you claim a finding. A count is a lead, not a verdict. Open the top hotspot files and confirm the pattern.

### Phase 3: Verification inventory

Fill the inventory table in [REFERENCE.md](REFERENCE.md). Mark each technique `have`, `partly` or `not found`, with the evidence. "Not found" means not found in this repo.

### Phase 4: Report

Write `docs/slop-audit/YYYY-MM-DD.md` from the template in [REFERENCE.md](REFERENCE.md), with:

1. Frontmatter: `repo`, `date`, `skill: slop-audit`, `status: open`.
2. A numbers table, with last report's numbers next to this one's.
3. All 12 steps, in order. A finding gets evidence, then the proposed rung and check. A step with nothing to report says "No finding" plus one line of evidence. A step you could not check says "Skipped" and why. Never leave a step out.
4. The verification inventory.
5. A ranked shortlist of at most 5 findings. Rank by fix churn first, then correction count, then cost.

Then ask the user which one finding to act on. Offer to open one ticket for it.

## Rules

- **Audit, do not fix.** No code changes in this skill. The output is the report.
- **Evidence for every claim.** A number, a path or a quote. No "probably".
- **Checks use the repo's standard files.** Point every fix at `package.json` scripts, the ESLint config, test files or CI workflows. Never at a third-party tool's config folder.
- **Strongest rung wins.** Never propose prose when a type or a lint rule can hold the lesson.
- **One ticket per run.** A list of 20 fixes gets none done.
- **Clean but unenforced comes first.** A boundary that holds today and has no check is the cheapest thing to lock.
- **Do not count gaps as debt.** A missing technique matters only where a bug class already hurts.
- **Use POSIX classes in `git grep`.** macOS `git grep -E` ignores `\s` and `\b`. Use `[[:space:]]` and explicit boundaries.

## Credits

The method follows Lauren Tan's talk "Turning slop into gold". The inventory follows Cindy Sridharan's chart of testing techniques. The ladder follows "encode lessons in structure" from pstack.
