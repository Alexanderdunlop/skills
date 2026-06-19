---
name: align-user-journey
description: Before building a feature, state the user-experience it produces (what the person sees, does, and gets, step by step) and get the user to confirm that experience is right before writing code. Use this whenever the user asks to build a feature, flow, or product surface ("build the signup", "add a connect-your-account flow", "make the onboarding") without having specified what the end user should experience. Use it even when the implementation seems obvious, because the obvious implementation often encodes a user-experience the user never actually signed off on. This skill aligns on what the *end user* of the feature will see and do — for teaching the *developer* an unfamiliar standard or protocol before they build on it, use [[teach-the-mechanism]] instead.
---

# Align User Journey

Claude builds the wrong thing correctly. The user asks for "a connect-your-account flow", Claude builds a clean OAuth integration, and only when the user tries it do they realise they wanted a magic-link step first, or no consent screen, or the tokens stored differently. The code works. The experience is wrong. By then it's built, and unwinding a working implementation costs more than the two minutes of agreeing the journey up front would have.

## When to run this

- The user asks to build a feature or flow that a person will move through: signup, onboarding, a connect-an-integration flow, a checkout, a settings surface.
- The request names the feature but not the experience: "build the login", "add Google Analytics connection", "make the upload work" — the what, not the what-the-user-sees.
- There's more than one reasonable user-experience and the user hasn't said which. A connect flow can ask for consent or not, log the user in first or not, redirect or stay in-page.
- Do NOT run this for a pure mechanism with no human in the loop (a cron job, a data transform, an internal API endpoint nothing renders), or when the user has already spelled out the experience they want.

## The process

1. **State the journey as numbered steps from the user's seat.** "1. User clicks Connect Google Analytics. 2. Redirected to Google's consent screen. 3. Approves. 4. Lands back on your settings page, account now shows Connected." Concrete, real screen names, real buttons. Not the architecture, the experience.

2. **Surface the forks where the experience could go either way.** Name the decisions that change what the user feels, not the ones that only change the code: "Do they consent every time or just the first connect? Do they stay on your page or see Google's? Does a failed connect drop them back to settings or to an error page?" These are the choices that are expensive to reverse once built.

3. **State the one-line scope boundary.** What experience this does NOT cover, so the user can catch a missing surface now: "This covers connecting an account. It does not cover disconnecting or re-authing an expired one."

4. **Stop and wait for confirmation on the journey, then build autonomously.** Once the user signs off on the experience, implement the whole thing. Do not re-check at every step.

## The trap to avoid

This is not `align-first` and it is not a permission-loop. It aligns on one thing only: the user-visible experience. It is not a re-litigation of the technical plan, the file structure, or the library choice. State the journey, get a yes, then make every implementation decision yourself without checking back. If you find yourself asking the user to approve the database schema or the function names, you've slipped out of this skill and into nagging.

Second trap: don't describe the journey in architecture terms. "The client hits the well-known endpoint, exchanges the code" is the mechanism, not the experience. The user in this skill is signing off on what *their* user sees, so the steps must be in user-visible language. The mechanism is yours to decide once the experience is agreed.

## What good looks like

The user says "add a flow to connect GA4 and Search Console." Instead of building the OAuth integration straight away, Claude lays out the journey: user opens settings, clicks Connect Google Analytics, hits Google's consent screen, approves, returns to settings showing Connected, repeats for Search Console. It flags the forks (consent once or every time, in-page or redirect, where a failure lands them) and the boundary (covers connecting, not disconnecting). The user catches that they wanted both connected in one consent pass, says so, and Claude builds it right the first time instead of shipping two separate flows that have to be torn apart.
