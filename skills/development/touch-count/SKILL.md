---
name: touch-count
description: Count "touch to production" for a GitHub repo, the number of human actions each merged pull request needed before it shipped, then read the worst pull request to find what the touches were about. Runs a script over the last 90 days of merged PRs and sorts the worst one's review comments by type. Use when the user says "touch count", "touch to production", "count touches", "how much review do my PRs need", "where does my review time go", or wants a number for how much human attention AI-written pull requests cost.
---

# Touch Count

Time to production hides where the time goes. This counts the human actions on each pull request instead.

A touch is one human action between a pull request opening and merging:

1. A review by someone who is not the author.
2. A comment from a reviewer.
3. A reply from the author.
4. A commit authored after the first review.

Bot accounts are left out and counted on their own.

## Quick start

1. Run `python3 <skill-dir>/scripts/touches.py` from the repo root. It needs the `gh` CLI, logged in.
2. Read the summary it prints and the file `worst-pr-<number>-comments.md` it saves.
3. Sort the worst pull request's comments by type.
4. Report the numbers, the sort and one change to try.

Options: `--repo owner/name`, `--days 30`, `--out touches.csv`.

## Process

### Phase 1: Count

- [ ] Run the script. Do not count by hand or estimate.
- [ ] If it reports 0 touches everywhere, say so. A solo repo with no reviewers has no touches to count, and that is the finding.
- [ ] Keep `touches.csv`. Next month's run is compared against it.

The script uses the date a commit was authored, not the date it was committed. A rebase resets the committed date on every commit, so the committed date makes every commit look like it came after review.

### Phase 2: Read the worst one

The typical pull request tells you very little. The cost sits in the few with the most touches.

- [ ] Open `worst-pr-<number>-comments.md`.
- [ ] Put every comment in exactly one group: **naming**, **real bug**, **style**, **question**, **other**. A real bug is a comment that points at behaviour that is wrong. "This could be clearer" is style.
- [ ] Count each group.
- [ ] Check what the bots found on the same pull request. Count how many real bugs came from a bot and how many from a person.
- [ ] If the top ten are all large, say so, with the lines changed.

### Phase 3: Report

Give the user:

1. The numbers table: median, 75th percentile, 90th percentile, highest, and how many had no touch at all.
2. The ten with the most touches.
3. The comment groups for the worst one, with counts.
4. One change to try, aimed at the biggest group. For example: many naming comments means names get agreed before the code is written. Many questions means the ticket left them open.

Say what the number cannot see: reviews in chat or on calls, and who wrote most of the pull requests.

Do not propose more than one change. The point is to run this again next month and see if that one change moved the number.
