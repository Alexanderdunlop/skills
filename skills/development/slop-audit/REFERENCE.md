# Slop Audit Reference

## The 12 steps

Each step has an idea, an audit question, and how to find the evidence.

### Phase A: Measure

**1. Set a baseline.**
Speed means nothing without a quality number next to it.
- Ask: What is the revert rate? What share of commits are fixes? Which user-facing timings are measured?
- Evidence: the History block of the probe. Search CI and docs for performance budgets.

**2. Collect every correction.**
Each time a human corrects an agent, that is a lesson. Lessons that stay in chat are lost.
- Ask: Where do corrections go? Can you count them by theme? Which theme repeats 3 times or more?
- Evidence: the correction log, if any. Human review comments on the last 50 merged PRs:

```bash
gh pr list --state merged --limit 50 --json number --jq '.[].number' \
  | while read -r n; do
      gh api "repos/{owner}/{repo}/pulls/$n/comments" \
        --jq '.[] | select(.user.type == "User") | "\(.path)\t\(.body | gsub("\n"; " "))"'
    done > review-comments.tsv
```

Group the comments by theme. Whatever humans still comment on is the backlog.

No correction log is fine. Search the Claude Code session history for this repo instead:

```bash
dir=~/.claude/projects/$(pwd | tr '/.' '--')
jq -r 'select(.type == "user" and (.message.content | type) == "string") | .message.content' "$dir"/*.jsonl \
  | grep -iE "^(no|don.t|stop|wrong|actually)\b|instead|not what i"
```

If there is no history either, say so under Step 2 and move on.

**3. Find the nuance.**
An API that needs judgment on every use leads to slop. React's `useEffect` is the classic case.
- Ask: Which APIs need judgment? In which files do they cluster? Which files take repeated fixes?
- Evidence: the Nuance and fix churn blocks. A file high on both lists is where the model is hard to use.

### Phase B: Codebase

**4. Weed the garden.**
Workarounds and deprecated code look like the established pattern, so agents copy them.
- Ask: Is there more than one way to do the same job? Ask a fresh agent "what is the pattern for X here?" Is its answer the one you want?
- Evidence: count imports per library for forms, data fetching, state, errors and toasts. Two libraries for one job is a finding. Also check for stray files in the repo root.

**5. Put context in the directory structure.**
A folder name can be a rule when a dependency check enforces it. Example: two top-level folders with imports between them banned.
- Ask: Which boundaries exist only in prose? Is each one clean today?
- Evidence: grep for imports across each documented boundary. Zero hits and no check means lock it now.

### Phase C: Static analysis

**6. Turn corrections into checks with good messages.**
The error message must name the root-cause fix. A bare "not allowed" invites a workaround.
- Ask: For each correction theme at 3 or more, which rung can hold it? Does each custom rule's message say what to do instead?
- Evidence: the correction tags, the custom lint rules and their messages.

**7. Close the escape hatches.**
Agents use comments and docs to justify a quick fix. A comment is not enforceable.
- Ask: How many suppressions and casts exist, by rule? Which config exceptions exist, and does code outside them copy them?
- Evidence: the Escape hatches block and the justification-word count. List every override block in the lint config. A rule with many suppressions does not model a real case.

For comments in particular:
1. Measure comment lines added per PR over the last 30 PRs.
2. Sample 20 added comments. Sort each into "why the code cannot show" or "narrates the code".
3. Find shapes that are always narration, such as a docblock on a private function.
4. Check if the linter can match those shapes. If not, a diff-scoped grep check can.

### Phase D: Verification

**8. Give agents runtime verification and a feature map.**
The agent must run the app and use the same debug tools as a person. A feature map lists every feature in user words, so "the thing in the sidebar" has one name.
- Ask: Can an agent start, drive and screenshot the app with one command? Is there one list of screens and features?
- Evidence: dev scripts, browser-driving skills, a glossary or a site map.

**9. Find the laws and test them as properties.**
Some code obeys a law: roundtrip, idempotent, order-free. Property-based tests check the law on random input. Bombadil does the same for web UIs: it explores the UI and checks properties you write.
- Ask: Which functions obey a law? Which UI facts must hold after any sequence of actions?
- Evidence: serializers, parsers, mappers and transforms. Cross them with fix churn. UI candidates: no console error after any action; a save then reload shows the same data.

**10. Model the big flows as state charts.**
A state chart from the user's side shows if the agent understood the intent. Model checkers such as TLA+ can check it.
- Ask: Can two people draw the same chart for the largest flow? Where they differ, the agent must guess.
- Evidence: the flow with the most decision records or the most bugs.

**11. Take a verification inventory.**
Agents make costly techniques cheap. Most token spend should go to checking, not writing.
- Ask: For each technique below, do you have it? Where do the tokens go?
- Evidence: dependencies, CI workflows and grep.

### Phase E: Prose, then automate

**12. Shrink prose, then build the outer loop.**
Prose comes last. Automate only on solid foundations, or the loop makes more slop.
- Ask: Can a rung above hold each line of CLAUDE.md or AGENTS.md? Which loop would you trust to run unattended?
- Evidence: lines that say "not automated", "no check", "remember to" or "by hand".

```bash
grep -niE "not automated|no check|remember to|by hand|on you" CLAUDE.md AGENTS.md docs/**/*.md
```

## Verification inventory

After Cindy Sridharan's chart. Mark each row `have`, `partly` or `not found`, with evidence.

| Stage | Techniques |
|---|---|
| Pre-production | unit, functional, component, fuzz, property-based, formal verification, static analysis, mutation, coverage, benchmark, contract, lint, acceptance, regression, smoke, usability, UI/UX, penetration, threat modelling, performance |
| Deploy | integration, tap compare, load, shadowing, config, soak |
| Release | canary, monitoring, traffic shaping, feature flags, exception tracking |
| Post-release | teeing, profiling, logs and events, chaos, monitoring, A/B, tracing, dynamic exploration, real user monitoring, auditing, on-call |

Where to look:
- Dependencies: test runners, property libraries, mutation tools, a11y checkers, error trackers, flag SDKs.
- CI workflows: which suites run, on which event, and which block a merge.
- Source: flag hooks, exception capture calls, analytics init.

## Report template

List all 12 steps, in order. Never leave a step out.

```md
---
repo: <owner/name>
date: YYYY-MM-DD
skill: slop-audit
status: open
---

# Slop audit YYYY-MM-DD

| Signal | Last | Now |
|---|---|---|

## Steps

### Step 1: Set a baseline
Evidence: ...
Rung: codebase | static analysis | verification | prose
Check: <the change, in package.json scripts, ESLint config, test files or CI workflows>

### Step 2: Collect every correction
No finding. <one line of evidence>

### Step 3: Find the nuance
Skipped. <why it could not be checked>

... through Step 12.

## Verification inventory
| Technique | Status | Evidence |

## Shortlist
1. ...
```
