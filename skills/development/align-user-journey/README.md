# align-user-journey

A skill that stops Claude from building a feature until you've confirmed the user-visible experience — what the person sees, does, and gets, step by step.

## Why

The expensive failure isn't broken code, it's working code that ships the wrong experience. You ask for "a connect-your-account flow", Claude builds a clean OAuth integration, and only when you click through it do you realise you wanted a magic-link step first, or no consent screen, or both integrations connected in one pass. The code works. The journey is wrong. Unwinding a working implementation costs more than the two minutes of agreeing the journey up front would have.

## Workflow

```
1. You ask to build a feature, flow, or product surface
2. Skill triggers (or you run /align-user-journey)
3. Claude states the journey as numbered steps from the user's seat
4. Claude surfaces the forks where the experience could go either way
5. Claude states the one-line scope boundary (what this does NOT cover)
6. You confirm or correct the journey
7. Claude builds the whole thing autonomously — no per-step check-ins
```

## When it triggers

- You ask to build a feature or flow a person moves through: signup, onboarding, connect-an-integration, checkout, settings surface
- The request names the feature but not the experience: "build the login", "add Google Analytics connection", "make the upload work"
- There's more than one reasonable user-experience and you haven't said which
- **Not** for pure mechanism with no human in the loop (cron jobs, data transforms, internal API endpoints nothing renders), or when you've already spelled out the experience you want

## What makes this different

- **Experience, not architecture** — the steps are what the user sees and does, in user-visible language. "Clicks Connect Google Analytics, sees Google's consent screen, lands back on settings as Connected" — not "client hits the well-known endpoint, exchanges the code".
- **Forks named, not buried** — the decisions that change what the user feels (consent once or every time, in-page or redirect, where a failure lands them) get surfaced as choices, not silently baked into the build.
- **Scope boundary stated in one line** — "covers connecting, not disconnecting" lets you catch a missing surface now instead of after merge.
- **One alignment, then autonomous build** — not a permission-loop. Journey gets signed off once, then Claude makes every implementation decision without checking back.

## What it doesn't do

- Re-litigate the technical plan, file structure, or library choice
- Ask you to approve the database schema or function names after the journey is agreed
- Run on internal mechanism with no user-visible surface
- Loop back to confirm at every step of the build

## Usage

When you're about to ask for a feature with a user in the loop:

```
/align-user-journey
```

Or just describe the feature and the skill will trigger.
