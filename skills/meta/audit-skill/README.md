# audit-skill

A skill that reads an existing SKILL.md, scores every instruction line, and reports how many survived — so you can see the dead weight instead of staring at a wall of lines that all feel like instructions.

## Why

Most weak skills aren't broken — they're padded. They trigger, Claude loads them, and then 80% of the lines are things Claude would have done anyway. The skill changes nothing, but you can't tell which lines are dead because every line *feels* like a rule.

This skill makes the kill count visible: `23 lines. 6 survived.` That number is the gut-punch that makes you act.

It does only the audit. It does not rewrite — that's [create-skill](../create-skill/SKILL.md)'s job.

## Workflow

```
1. Point Claude at a SKILL.md (or run /audit-skill)
2. Skill reads the whole file end-to-end
3. Runs the trigger test on the description
4. Runs the would-have-anyway test on every instruction line
5. Reports the headline kill count, then a per-line verdict, then what's missing
```

## The two tests

- **Would-have-anyway** — for each line, would Claude have done this without being told? If yes, it's filler. Mark **Weak**.
- **Trigger** — read only the description. Would Claude pick this from a list of twenty skills, including implied cases? If it only fires on the literal keyword, mark **Trigger-risk**.

## What you get back

- A quotable headline: `23 lines. 6 survived.`
- A verdict on the description: Keep or Trigger-risk + why.
- A line-by-line list of Keep / Weak with one-line reasons.
- A Missing section — no "trap to avoid", opens with a definition instead of a failure, no concrete example.

No rewrites. No suggested replacements beyond what's needed to explain a Weak verdict. If you want the rewrite, chain to `create-skill` in rewrite mode.

## What makes this different

- **Brutal by design** — the value is the number and the bluntness. A diplomatic audit ("lots of good intent here") wastes your time.
- **Ignores prose framing** — markdown headers and the opening failure statement aren't scored as instructions. They're judged under Missing instead.
- **One job** — no rewriting, no fixing, no "here's how I'd reword line 14." Audit ends at the verdict.

## Usage

```
/audit-skill path/to/SKILL.md
```

Or just paste a skill and ask Claude to audit / score / review it.
