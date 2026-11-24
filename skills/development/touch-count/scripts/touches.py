#!/usr/bin/env python3
"""Count human touches per merged pull request. Needs the gh CLI, logged in.

  python3 touches.py                      # the repo in this folder, last 90 days
  python3 touches.py --repo owner/name --days 30 --out touches.csv

A touch is one human action between a PR opening and it merging:
  1. a review by someone who is not the author
  2. a comment from a reviewer
  3. a reply from the author
  4. a commit authored after the first review
Bot accounts are left out and counted on their own.
"""
import argparse, csv, datetime as dt, json, re, subprocess, sys


def gh(path):
    """One GET against the GitHub REST API, all pages."""
    out, page = [], 1
    while True:
        sep = "&" if "?" in path else "?"
        r = subprocess.run(["gh", "api", f"{path}{sep}per_page=100&page={page}"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"gh api {path} failed: {r.stderr.strip()}")
        data = json.loads(r.stdout)
        if isinstance(data, dict):
            return data
        out += data
        if len(data) < 100:
            return out
        page += 1


def this_repo():
    r = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
    m = re.search(r"github\.com[:/]+([^/]+/[^/]+?)(?:\.git)?/?$", r.stdout.strip())
    if not m:
        sys.exit("Could not read the repo from git. Pass --repo owner/name.")
    return m.group(1)


def is_bot(user):
    return not user or user.get("type") == "Bot" or user.get("login", "").endswith("[bot]")


def when(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def merged_prs(repo, cutoff):
    """Newest first. Stops at the first PR not updated since the cutoff."""
    found, page = [], 1
    while True:
        r = subprocess.run(["gh", "api", f"repos/{repo}/pulls?state=closed&sort=updated"
                            f"&direction=desc&per_page=100&page={page}"], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"Could not list pull requests: {r.stderr.strip()}")
        batch = json.loads(r.stdout)
        for pr in batch:
            if when(pr["updated_at"]) < cutoff:
                return found
            if pr.get("merged_at") and when(pr["merged_at"]) >= cutoff:
                found.append(pr)
        if len(batch) < 100:
            return found
        page += 1


def count(repo, pr):
    n, author = pr["number"], (pr.get("user") or {}).get("login")
    reviews = [r for r in gh(f"repos/{repo}/pulls/{n}/reviews") if r.get("submitted_at")]
    comments = gh(f"repos/{repo}/pulls/{n}/comments") + gh(f"repos/{repo}/issues/{n}/comments")
    commits = gh(f"repos/{repo}/pulls/{n}/commits")
    detail = gh(f"repos/{repo}/pulls/{n}")

    others = [r for r in reviews if (r.get("user") or {}).get("login") != author]
    human_reviews = [r for r in others if not is_bot(r.get("user"))]
    human = [c for c in comments if not is_bot(c.get("user"))]
    reviewer_comments = [c for c in human if c["user"]["login"] != author]
    author_replies = [c for c in human if c["user"]["login"] == author]
    bot_comments = len(comments) - len(human)

    first = min((when(r["submitted_at"]) for r in others), default=None)
    # authored date, not committed date: a rebase resets the committed date on every commit.
    late = [c for c in commits if first and when(c["commit"]["author"]["date"]) > first]

    row = {"number": n, "title": pr["title"], "author": author, "merged_at": pr["merged_at"],
           "lines_changed": detail.get("additions", 0) + detail.get("deletions", 0),
           "files": detail.get("changed_files", 0), "commits": len(commits),
           "reviews": len(human_reviews), "reviewer_comments": len(reviewer_comments),
           "author_replies": len(author_replies), "commits_after_review": len(late),
           "bot_comments": bot_comments}
    row["touches"] = (row["reviews"] + row["reviewer_comments"] + row["author_replies"]
                      + row["commits_after_review"])
    return row, reviewer_comments


def pct(sorted_vals, p):
    """Nearest rank."""
    if not sorted_vals:
        return 0
    k = max(1, -(-len(sorted_vals) * p // 100))
    return sorted_vals[int(k) - 1]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo"); ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--out", default="touches.csv")
    a = ap.parse_args()
    repo = a.repo or this_repo()
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)

    prs = merged_prs(repo, cutoff)
    if not prs:
        sys.exit(f"No pull requests merged in {repo} in the last {a.days} days.")
    rows, worst_comments = [], {}
    for i, pr in enumerate(prs, 1):
        print(f"\r{i}/{len(prs)}", end="", file=sys.stderr)
        row, rc = count(repo, pr)
        rows.append(row); worst_comments[row["number"]] = rc
    print(file=sys.stderr)

    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    t = sorted(r["touches"] for r in rows)
    rows.sort(key=lambda r: -r["touches"])
    clean = sum(1 for r in rows if r["touches"] == 0 and r["bot_comments"] == 0)
    print(f"# Touch to production: {repo}, last {a.days} days\n")
    print(f"Merged pull requests: {len(rows)}")
    print(f"Median touches:       {pct(t, 50)}")
    print(f"75th percentile:      {pct(t, 75)}")
    print(f"90th percentile:      {pct(t, 90)}")
    print(f"Highest:              {t[-1]}")
    print(f"No touch and no bot comment: {clean} of {len(rows)}\n")
    print("## Ten with the most touches\n")
    print("| PR | touches | reviews | reviewer comments | author replies | commits after review | lines |")
    print("|---|---|---|---|---|---|---|")
    for r in rows[:10]:
        print(f"| #{r['number']} | {r['touches']} | {r['reviews']} | {r['reviewer_comments']} | "
              f"{r['author_replies']} | {r['commits_after_review']} | {r['lines_changed']} |")
    worst = rows[0]
    wc = worst_comments[worst["number"]]
    if wc:
        name = f"worst-pr-{worst['number']}-comments.md"
        with open(name, "w") as f:
            f.write(f"# Reviewer comments on #{worst['number']}: {worst['title']}\n\n")
            for c in sorted(wc, key=lambda c: c["created_at"]):
                where = f" ({c['path']})" if c.get("path") else ""
                f.write(f"- **{c['user']['login']}**{where}: {' '.join((c.get('body') or '').split())}\n")
        print(f"\nReviewer comments on the worst one (#{worst['number']}) saved to {name}")
    print(f"Per-PR numbers saved to {a.out}")


if __name__ == "__main__":
    main()
