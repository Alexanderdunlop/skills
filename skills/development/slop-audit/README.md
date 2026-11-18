# slop-audit

A skill that audits a codebase for the places where agents write slop, and names the strongest check that can stop each one.

## Why

Agents copy the code around them. A workaround, a deprecated pattern or an API that needs judgment soon looks like "the way we do it here". A rule in CLAUDE.md asks the agent to remember. A rule in code makes the wrong thing fail.

This skill finds the weak spots and ranks them. It follows Lauren Tan's talk "Turning slop into gold": every correction becomes a deterministic check, and verification earns the trust to go fast.

## Workflow

```
1. Run /slop-audit in the repo root
2. The probe script prints counts: nuance APIs, escape hatches, fix churn, reverts
3. The agent walks 12 steps: measure, codebase, static analysis, verification, prose
4. It fills a verification inventory, from unit tests to on-call
5. It writes docs/slop-audit/YYYY-MM-DD.md
6. You pick one finding and turn it into one ticket
7. Next month, run it again and compare
```

## What it does

- Measures a baseline: revert rate, fix share, fix churn by file
- Finds nuance: APIs that need judgment, and the files where they cluster
- Counts escape hatches by rule: lint suppressions, casts, config exceptions
- Finds rules that live only in prose, and checks if the code obeys them today
- Takes a verification inventory across pre-production, deploy, release and post-release
- Proposes a rung for each finding: codebase, static analysis, verification or prose

## What it doesn't do

- Change code. The output is a report.
- Treat every missing technique as debt. A gap matters only where bugs already hurt.

## Usage

```
/slop-audit
```

Or tell Claude: "run a slop audit on this repo".

Options for the probe script:

```bash
CORRECTIONS=docs/corrections.tsv NUANCE='useSyncExternalStore|flushSync' DAYS=90 \
  bash scripts/probe.sh src
```
