# CLAUDE.md Generator - Reference

## Apple's Actual Files

These are Apple's leaked CLAUDE.md files. Study the style — this is what the skill should produce.

### File 1: Chat System

```markdown
# Chat - Conversational Support (Juno AI + Live Agents)

- Uses **AsyncStream** for real-time updates, NOT Combine (unlike rest of app). Streams are recreated on each access; old ones are finished.
- Service providers are **actors** (not `@MainActor` classes) for thread-safe concurrent message handling.
- **Multi-backend via protocol:** `ChatViewModelServiceProvider` abstracts Juno AI (`SupportAssistantAPIProvider`), live agents (`ChatKitChatServiceProvider`), and dev mocks. View model doesn't know which backend is active.
- **Conditional compilation is heavy:** `#if JUNO_ENABLED`, `#if canImport(CCChatKit)`, `#if DEV_BUILD`. Some files nest these. Check xoconfig for enabled flags.
- **Three participant roles:** `.client` (user), `.agent` (live Apple Support), `.assistant` (AI). Route message handling per role.
- Messages are wrapped in `MessageGroup` (UUID container) to avoid SwiftUI ID collisions (rdar://164022273). Don't flatten.
- CCChatkit is callback-based; bridged to async/await via `Task` wrappers in `ChatFacadeServiceProvider`.
- Session persistence: Keychain for `ChatInfo` (reconnection), file cache in `CachesDirectory/TemporaryChatTranscripts/` for transcripts
```

### File 2: Component Library

```markdown
# SAComponents - Shared UI Component Library

- Components are purely UI - no business logic, no service dependencies.
- UIKit components use `UIContentConfiguration` protocol with preset factory methods (e.g., `.cell()`, `.callToActionProminent()`).
- SwiftUI components provide convenience modifiers on `View` (e.g., `platterBackground()`, `frame(square:)`).
- Presets live in `Presets/` as static factory methods on enums.
- Platform variants use `#if os(visionOS)` guards. iOS version conditionals use `#available`.
- DocC catalog in `SAComponents.docc/` with contributor guide. Update docs when adding components.
- Always include `#Preview {}` showing multiple states for new components.
```

## What To Notice

Apple's files are NOT structured with section headers. They are:

- **One H1** with a one-line project identity
- **Flat bullet list** — no H2s, no "Architecture" / "Commands" / "Conventions" sections
- Every bullet is a **self-contained instruction** that mixes what, why, and what-not-to-do
- **Bold on the key term**, not the category
- Commands are inline where relevant, not in their own section
- Architecture decisions and footguns live side by side — no separation

## The 6 Rules

1. **Under 200 lines.** Claude's adherence drops when files get bloated.
2. **Treat the file as public.** Never include API keys or credentials.
3. **Be direct.** "Uses AsyncStream for real-time updates, NOT Combine." Not "consider using" or "it might be good to."
4. **Only what Claude can't infer.** Don't waste lines on format rules or things visible in the code. Architecture decisions, protocol abstractions, footguns — the stuff you can't figure out unless told.
5. **Version control it.** Don't listen to people saying otherwise after the leak. This would be like saying don't leave documentation in your repo.
6. **Add a CI gate that strips CLAUDE.md from builds.** The lesson Apple learned the hard way.

## Template

The output should look like Apple's files. One heading, flat bullets, no section headers:

```markdown
# [Project Name] - [One Line Identity]

- [Architecture decision with WHY and what is NOT used]
- [Key abstraction and what it hides from the rest of the codebase]
- [Known footgun — what breaks and why. Reference ticket if available]
- [Build/deploy constraint that Claude can't infer from code]
- [Framework version caveat or breaking change warning]
- [Convention that isn't enforced by tooling]
- [What "done" means — tests, previews, manual verification, etc.]
- `[command]` — [what it does and when to use it, only if non-obvious]
```

**Do not** generate separate sections for Architecture, Commands, Conventions, Build System, Avoid, and Definition of Done. Weave them together as flat bullets like Apple does. Group related bullets near each other but without headers.

## Style Rules

Each bullet should read like Apple's:

**Good (Apple's style):**
- "Uses **AsyncStream** for real-time updates, NOT Combine (unlike rest of app)."
- "Service providers are **actors** (not `@MainActor` classes) for thread-safe concurrent message handling."
- "Messages are wrapped in `MessageGroup` (UUID container) to avoid SwiftUI ID collisions (rdar://164022273). Don't flatten."
- "**Conditional compilation is heavy:** `#if JUNO_ENABLED`, `#if canImport(CCChatKit)`, `#if DEV_BUILD`. Some files nest these."
- "Always include `#Preview {}` showing multiple states for new components."

**Bad — vague or passive:**
- "Consider using Zustand for state management."
- "Follow existing patterns for chat usage."

**Bad — Claude can read the code and figure this out:**
- "The project uses Next.js with the app router." (visible in package.json and directory structure)
- "Prisma generates into `src/generated/prisma/`." (visible from the directory and imports)
- "Auth uses HMAC signature with 30-day expiry." (visible by reading the auth code)
- "Environment validation uses `@t3-oss/env-core` in `src/env.ts`." (visible from the file)
- "Import the client from `@/generated/prisma/client`." (visible from existing imports throughout codebase)
- "`pnpm build` runs migrations first." (visible in package.json scripts)
- Listing your entire stack as bullet points
- Separate "Commands" section that just lists `pnpm dev`, `pnpm build`, `pnpm lint`

Apple's Chat system is a **massive** codebase. They covered it in 8 bullets. If Apple can document their entire conversational AI support system in 8 lines, your project doesn't need 16.

## Audit Scoring

When auditing an existing CLAUDE.md:

| Score | Meaning |
|-------|---------|
| Present | Imperative, specific, has WHY or NOT |
| Weak | Vague, duplicates tooling, passive voice, or just states facts without decisions |
| Missing | Topic not covered at all |

Immediate fixes:

- Secrets or credentials anywhere in the file
- Lines like "follow best practices" or "use clean code" (vague, useless)
- Lines that just state what framework is used without a decision or warning
- Duplicated linter/formatter rules (waste of budget)
- File over 200 lines
- Separate section headers where flat bullets would work (Apple doesn't use them)

## Secrets Detection

When scanning, check for:

- `sk-`, `pk-`, `api_key`, `API_KEY`, `token`, `secret`
- Connection strings: `mongodb://`, `postgres://`, `mysql://`, `redis://`
- URLs with credentials: `https://user:pass@`
- Base64 strings longer than 40 chars
- Environment variable values (not names)
- Internal hostnames or IP addresses

If found, flag but never display the value. Tell the user which line to remove.
