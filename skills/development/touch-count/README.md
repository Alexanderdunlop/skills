# touch-count

A skill that counts how many human actions each merged pull request needed, then reads the worst one to find out what they were about.

## Why

Agents made building fast. The time now goes on pull requests that are already "finished": answering review comments, pushing fixes, nudging things along. Time to production does not show that. A count of touches does.

I ran this on 312 pull requests at work. Half needed 4 touches or fewer. One needed 147. On that one, 20 of the 29 human comments were about names, and the review bot found every real bug.

## What counts as a touch

1. A review by someone who is not the author
2. A comment from a reviewer
3. A reply from the author
4. A commit authored after the first review

Bots are left out and counted on their own.

## Usage

```
/touch-count
```

Or tell Claude: "count touch to production for this repo".

To run only the script:

```bash
python3 scripts/touches.py                       # this repo, last 90 days
python3 scripts/touches.py --repo owner/name --days 30
```

It needs the `gh` CLI, logged in. Python standard library only.

## What you get

- Median, 75th percentile, 90th percentile and highest touch count
- How many pull requests merged with no touch at all
- The ten with the most touches, with lines changed
- `touches.csv` with the numbers for every pull request
- The worst one's review comments, sorted into naming, real bug, style, question, other
- One change to try

## What it can't see

- Reviews that happen in chat or on a call
- Anything outside GitHub
- It makes about five API calls per pull request, so a very busy repo takes a few minutes
