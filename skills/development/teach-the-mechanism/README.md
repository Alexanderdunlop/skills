# teach-the-mechanism

A skill that stops Claude from scaffolding code on an unfamiliar standard and instead walks you through the user-visible flow, then maps each step to the mechanism underneath — before any code gets written.

## Why

The expensive failure when learning a new standard is not bad code. It's working code you can't debug. Claude scaffolds an OAuth server, an auth flow, a protocol handler — it compiles, it runs — but you didn't hold the mental model going in, so when it breaks you're stranded. The code was never the gap. The model in your head was. Handing over more correct code widens that gap instead of closing it.

## Workflow

```
1. You describe a task on a standard / protocol / architecture new to you
2. Skill triggers (or you run /teach-the-mechanism)
3. Claude lays out the user-visible sequence — what the human sees, in order
4. Claude walks the same sequence again, attaching the mechanism to each step
5. Names the actors once, plainly, mapped to your real setup
6. Stops and asks whether to now wire it up or redirect the existing plan
```

## When it triggers

- You name the thing as new: "it's a new standard", "I'm still learning this", "I don't fully understand it yet"
- You ask to be taught instead of handed code: "explain it rather than writing it off", "walk me through how this works"
- You ask for the user-visible flow, the user journey, or "what does the person actually see"
- You asked for an implementation, but there's a signal you can't yet debug what you'd get
- **Not** when you clearly already hold the model and just want the code shipped, or for one-step tasks with no underlying model to teach

## What makes this different

- **Sequence first, mechanism second** — the user-visible flow is the scaffold the mechanism hangs on. Concepts land when pinned to a step you can already picture, not when delivered as a standalone list.
- **Plain mechanism, not cute metaphor** — describes the actual call (client sends a bearer token, server validates it, looks up stored credentials), not "Claude rings the bell and the server opens the filing cabinet". You're an engineer, not a child.
- **Actors named once, mapped to your setup** — if the standard has named roles (resource server, authorization server, client, resource owner), each gets one line that says which real thing in your project it is.
- **One pass, then offer to build** — explain first does not become explain forever. One pass through the flow, one pass through the mechanism, then the offer.

## What it doesn't do

- Start implementing inside the explanation
- Narrate mechanics in metaphor that obscures the actual calls
- Loop through three more "even simpler" passes instead of offering to build
- Run when you already hold the model and just want the code

## Usage

When you're about to build something on a standard, protocol, or architecture new to you:

```
/teach-the-mechanism
```

Or just say it's new and ask to be walked through it — the skill will trigger.
