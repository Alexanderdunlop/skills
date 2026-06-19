---
name: teach-the-mechanism
description: When the user is about to build something on an unfamiliar standard, protocol, or architecture, explain the user-visible flow first and map each step to the mechanism underneath before writing any code. Use this whenever the user asks how to implement something they say is new to them ("new standard", "still learning", "I don't fully get it"), asks "can you explain X instead of building it", or asks for the user process / user journey of a system. Use it even when the user originally asked for an implementation and working code would technically answer them, if there's any signal they don't yet hold the mental model. This skill teaches the *developer* an unfamiliar protocol so they can debug what gets built — for aligning on what the *end user* will experience in a feature, use [[align-user-journey]] instead.
---

# Teach the Mechanism

The user ends up with working code they can't debug. Claude scaffolds an OAuth server, an auth flow, a protocol handler, and it compiles, but the user didn't hold the mental model going in, so when it breaks they're stuck. The code was never the gap. The model in their head was. Handing over more correct code widens that gap instead of closing it.

## When to run this

- The user names the thing as new to them: "it's a new standard", "I'm still learning this", "I don't fully understand it yet".
- The user explicitly asks to be taught instead of handed code: "explain it rather than writing it off", "can you explain the user process", "walk me through how this works".
- The user asks for the user-visible flow, the user journey, or "what does the person actually see".
- The user asked for an implementation, but there's a signal they can't yet debug what they'd get. Building it anyway leaves them stranded the moment it breaks.
- Do NOT run this when the user clearly already holds the model and just wants the code shipped, or for a one-step task with no underlying model to teach.

## The process

1. **Lead with the user-visible sequence.** What the human at the keyboard actually sees, in order. "You paste the URL. A browser window opens. You log in. You consent. The connector flips to Connected." No internals yet. This is the scaffold everything else hangs on, and it's the part the user can already picture, so it's where understanding starts.

2. **Map each visible step to the mechanism underneath it.** Go back through the same sequence, one step at a time, and attach what's actually happening: "When the browser opens, the client fetched the well-known doc, found the auth server, and redirected you there with a PKCE challenge." The ordering is the whole trick. Mechanism lands when it's pinned to a step the user already understands, not delivered as a standalone list of concepts.

3. **Name the actors once, plainly.** If the standard has named roles (resource server, authorization server, client, resource owner), state each in one line and say which real thing it maps to in the user's setup. Don't make the user infer which box is their app.

4. **Offer to build only after the model is in place.** Close by asking whether to now wire it up, or redirect the existing plan. Do not start implementing inside the explanation. The user came for the model, not the code.

## The trap to avoid

Teaching the journey is not narrating mechanics in cute metaphor. "Claude rings the bell, the server opens the filing cabinet" is the failure, not the goal. Describe the actual call: the client sends a bearer token, the server validates it and looks up the stored credentials. Plain mechanism mapped to plain steps. The user is an engineer, not a child.

Second trap: don't let "explain first" become "explain forever". One pass through the visible flow, one pass mapping the mechanism, then offer to build. This is a teaching move, not a stall.

## What good looks like

The user is building an OAuth-protected MCP server, says "it's a new standard so explain it rather than writing it off." Instead of scaffolding the auth code, Claude lays out what the user sees connecting a custom connector (paste URL, browser opens, login, consent, Connected), then walks the same five steps again attaching the discovery fetch, the PKCE redirect, the code exchange, the token storage. The user, who had read three explainers and retained nothing, holds the broker pattern after one pass, because the mechanism was pinned to a sequence they could already picture.
