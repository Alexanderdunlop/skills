---
name: claude-md
description: Generate or update a project's CLAUDE.md file using structured interrogation of the codebase and user. Follows Apple's leaked CLAUDE.md patterns and Anthropic's best practices. Use when user wants to create, update, improve, audit, or rewrite their CLAUDE.md file, or when starting a new project that needs AI context.
---

# CLAUDE.md Generator

## Quick start

Run this skill against any project to generate a production-grade CLAUDE.md. The skill interrogates the codebase and asks targeted questions to produce a file that follows Apple's internal documentation patterns.

## Process

### Phase 1: Codebase Scan

Before asking anything, silently scan the project. Be thorough — anything you can answer from the code, you should NOT ask the user about.

- [ ] Read existing CLAUDE.md (if any)
- [ ] Check package.json / Cargo.toml / pyproject.toml / Package.swift for stack info
- [ ] Scan directory structure (2 levels deep)
- [ ] Identify test framework and test location
- [ ] Identify build/lint/test commands from scripts or config
- [ ] Check for .claude/ directory, rules, or existing skills
- [ ] Identify CI/CD config files (.github/workflows, Dockerfile, etc.)
- [ ] Count lines in existing CLAUDE.md (if over 200, flag for pruning)
- [ ] Read source code of key files to understand patterns, not just config
- [ ] Check monorepo structure, workspaces, and internal vs external packages
- [ ] Read README, CONTRIBUTING, or any onboarding docs

### Phase 2: Guided Questions

Ask the user **only what you genuinely cannot figure out from the code**. Ask as many questions as needed to build a complete picture — don't rush this phase.

**The bar for asking a question:** If you could answer it by reading source files, config, directory structure, git history, or docs — don't ask. The scan phase exists so the user doesn't have to explain things the codebase already tells you. Questions about what a package is, what a directory contains, what framework is being used, or whether something is first-party or third-party should never reach the user.

**What to ask about:** Architecture *decisions* (the WHY behind choices), team conventions not captured in config, known footguns from experience, definition of done, and anything that only exists in someone's head.

Start by sharing what you found in the scan: "Here's what I picked up from your codebase:" and list your inferences. Then ask the user to correct anything wrong before moving on.

Questions should be **easy to answer** — offer what you found and ask the user to confirm, correct, or add detail. Use yes/no and multiple-choice where possible. Examples:

- "I see you're using Next.js with the app router and Zustand for state. Anything about that setup I should call out, like why Zustand over Redux?"
- "Looks like tests live in `__tests__/` and use Vitest. Anything else I should know about your test setup?"
- "I found these build scripts: `build`, `dev`, `lint`. Are there any others you use regularly, or any flags I should know about?"
- "Has anything bitten you or a teammate before? Like a pattern that looks fine but breaks things, or a package you've learned to avoid?"
- "When you finish a PR, what does 'done' look like for you? Tests passing? Preview deployed? Docs updated? Or just green CI?"

Keep going until you have enough to fill every relevant section of the CLAUDE.md. If the user gives short answers, ask natural follow-ups. If they give detailed answers, move on.

### Phase 3: Generate CLAUDE.md

Write the file following Apple's actual style in [REFERENCE.md](REFERENCE.md). Study the two leaked files in the reference — match that format exactly.

**Structure:**

- One `# H1` heading with project name + one-line identity. That's the only heading.
- Flat bullet list underneath. **No H2 section headers.** No "Architecture", "Commands", "Conventions" sections. Apple doesn't use them.
- Each bullet is a self-contained instruction mixing what, why, and what-not-to-do.
- Bold the **key term**, not the category.
- Group related bullets near each other, but without headers.

**Hard rules:**

- Under 200 lines. No exceptions.
- No secrets, API keys, credentials, or sensitive endpoints.
- Imperative voice. "Uses X, NOT Y." Never "consider using" or "it might be good to."
- No lines that just state facts ("The project uses Next.js"). Every line must contain a decision, a warning, or a constraint.
- No linter/formatter rules that are already enforced by tooling.
- Don't list your entire stack. Only mention technology when paired with a decision or footgun.
- Commands only when non-obvious. Don't list `pnpm dev` unless there's a caveat.

**The brutality test — apply to every bullet before including it:**

Apple documented a massive codebase in 8 bullets. Your output should be equally ruthless. For each bullet, ask: "Could Claude figure this out by reading the source file?" If yes, cut it. Specifics:

- If it's visible in `package.json` scripts → cut it
- If it's visible from directory structure or file names → cut it
- If Claude would see it by reading the relevant source file → cut it
- If it describes how auth works and the auth code is readable → cut it
- If it explains what a config file does and that config file exists → cut it
- If it describes import paths that are already used throughout the codebase → cut it

**What survives the test:** decisions that aren't in the code (why X over Y), constraints you'd only know from experience (re-running this is safe because...), things that look wrong but are intentional (this file is named X not Y because...), and footguns where the obvious approach breaks something.

### Phase 4: Review

Present the generated CLAUDE.md and ask:

- "Does this cover your architecture accurately?"
- "Anything missing that a new engineer would need to know?"
- "Any lines here that contain sensitive info that shouldn't be public?"

## Updating An Existing CLAUDE.md

When updating rather than creating:

1. Run the codebase scan
2. Diff the current CLAUDE.md against what the scan reveals
3. Flag: stale rules, missing sections, lines over the 200 line budget, any secrets or credentials
4. Propose specific additions, removals, and rewrites
5. Ask user to confirm before applying

## Audit Mode

When the user asks to "audit" or "review" their CLAUDE.md:

- Check line count (flag if over 200)
- Check for secrets or credential patterns (API keys, tokens, connection strings)
- Check for vague instructions ("follow best practices", "use good patterns")
- Check for linter/formatter duplication
- Check for missing sections (project identity, architecture, commands, avoid, done criteria)
- Score each section: present, missing, or weak
- Output a summary with specific fix suggestions

See [REFERENCE.md](REFERENCE.md) for the full section template and Apple's patterns.
