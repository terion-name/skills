---
name: refactoring-and-reviewing-code
description: Use when asked to refactor, clean up, restructure, simplify, review, untangle, decouple, flatten, or improve existing code without changing its behavior; when diagnosing code smells; when preparing a codebase for a new feature by first making the change easy; or when the user says "this is messy / confusing / hard to follow / too complex" and wants it improved. Trigger on "refactor", "clean up", "restructure", "simplify", "review this code", "code smell", "tidy", "improve", "untangle", "decouple", "flatten", "extract", "rename", or when the user pastes code and asks what is wrong with it, what could be better, or how it could be more readable. Do NOT use when writing new code from scratch (use writing-good-code); do NOT use for the specific question of whether one abstraction is worth extracting (use abstraction-quality). When a task genuinely requires both behavior change and cleanup, refactor first under this skill, commit, then switch to writing-good-code for the behavior change.
---

# Refactoring and reviewing code

Improve existing code **without changing its behavior**, or review it to recommend changes. Safety and reversibility dominate speed. Move in tiny steps with working software between each.

## Core stance

1. **Two hats: wear one at a time.** You are either refactoring (behavior preserved, tests unchanged) or changing behavior (tests may change). Never both in one commit. If you find you must change behavior to complete a refactor, stop, revert, and do it in two steps.
2. **Structure and behavior go in separate commits.** Kent Beck's discipline. A reviewer reading a tidy commit should never have to ask "did this change what the code does?"
3. **Tiny, reversible moves.** If a refactor drifts beyond an hour without green tests, the scope is wrong. Stash, break it down, restart.
4. **Make the change easy, then make the easy change.** If a feature is hard to add, refactor first to make it easy, commit the refactor, then add the feature.
5. **Chesterton's Fence.** Never delete code whose purpose you cannot articulate. Before removing an odd-looking check, `git blame`, read the commit and linked ticket, search for bug reports that reference it. If you cannot find the reason after a bounded search, assume you are missing context and leave it.

## Pre-refactor checklist

Run this every time before touching the code:

1. **Are there tests for the code I am about to change?** If yes, read them. If no, this is legacy code (Michael Feathers: legacy = code without tests). Find a **seam** — a point where behavior can be altered without editing at that place — and write a **characterization test** that pins the *current* behavior, bugs included. Only then refactor. See `references/refactoring-safely.md`.
2. **What is the behavior I must preserve?** State it in one sentence. If you cannot, read more before touching code.
3. **What is the smallest step toward my goal?** Name the first Beck tidying (`references/tidyings.md`) or Fowler refactoring (`references/smell-catalog.md`) that moves the code toward the goal without changing behavior.
4. **Is this code about to be deleted?** If so, do not tidy. The cheapest tidying is the one you do not do.

## How to diagnose

Do not rely on feeling — count. Open the code and score it on these axes. Each failing axis suggests one or more refactorings. See `references/smell-catalog.md` for remedies.

| Axis | Warning threshold | Likely smell |
|---|---|---|
| Function length | >~40 lines *and* mixed abstraction levels | Long Function |
| Nesting depth | >3 | Deeply Nested Conditionals |
| Parameters | >4 or any flag parameter | Long Parameter List, Wrong Abstraction |
| Class size | >~200 lines doing >1 thing | Large Class, Divergent Change |
| Files changed per feature | >3 | Shotgun Surgery |
| Public interface / body ratio | Close to 1 | Shallow Module, Lazy Element |
| Conditional count inside a shared helper | Growing over time | Wrong Abstraction (Metz decay) |
| Message chain depth | `a.b().c().d()` | Train Wreck / Demeter violation |
| Comments restating code | Any | Comments as deodorant |
| Suffixes like `*Manager`, `*Helper`, `*Util` | Any not justified by domain | Name-as-concealment |

## Order of operations

Apply refactorings in this order; they compose.

1. **Rename** for clarity. Free, reversible, lowers cognitive load before any other move.
2. **Extract explaining variables** for complex expressions. Name sub-booleans, sub-computations, literal constants.
3. **Flatten control flow.** Guard clauses for preconditions; early returns; invert negative conditions. Target nesting depth ≤ 3.
4. **Collapse shallow abstractions.** Inline pass-through methods, single-line helpers that only rename, one-implementation interfaces that serve no real seam. If you cannot articulate what an abstraction hides, inline it.
5. **Separate concerns that are truly separate.** Apply Extract Function, Move Function, Extract Class only after the above, and only when the extracted piece has a name in the domain.
6. **Fix data clumps and primitive obsession.** Group fields that always travel together; introduce small value types with meaningful constructors (Parse, don't validate).
7. **Rework wrong abstractions by going back.** If a shared helper has accumulated flag parameters, **inline it back into each caller**, delete the branches each caller does not use, then look for a new honest abstraction if one emerges. See `references/worked-refactors.md`.
8. **Improve error handling at the boundary.** Push exceptions out to edges; replace bool-and-sentinel returns with typed results; add context to wrapped errors.
9. **Only then consider larger structural moves** (splitting files, extracting packages, introducing layers). These come last because they are the hardest to reverse.

## What NOT to refactor

- Code that is about to be deleted or rewritten.
- Code you do not understand and cannot gain understanding of in bounded time (Chesterton's Fence).
- Code that works, is not in the path of any upcoming change, and has low confusion cost. Beck's "Never" column: not every mess is worth tidying.
- Style-only changes in code someone else owns, without discussion.

## When you are stuck

- If a refactor feels large, revert. Break it into a sequence of tidyings each of which keeps tests green.
- If tests do not exist and you cannot find a unit-level seam, write a higher-level characterization test (HTTP-level, snapshot of logs) and refactor under that instead of trying to carve unit tests where the code does not admit them.
- If the abstraction feels wrong but you cannot articulate why, run the decision procedure in the `abstraction-quality` skill.

## Reasoning tools to apply during review

Load `references/reasoning-tools.md` for detail. Key applications:

- **Chesterton's Fence** before deletion.
- **Hyrum's Law** before any API change: someone depends on every observable behavior, including error message text, iteration order, timing, and serialization.
- **Gall's Law** before proposing any big-bang redesign: complex systems that work evolved from simple ones that worked; a complex system designed from scratch does not work and cannot be patched to work.
- **Postel's Law and its rebuttal.** At *internal* boundaries, be strict in what you accept. "Liberal in what you accept" becomes a technical-debt factory inside a trusted system (Martin Thomson's critique). Only at the outermost interop boundary with legacy systems does liberality earn its keep.
- **Conway's Law** when proposing module splits: modules end up mirroring team communication patterns. If the split does not match ownership, expect friction.

## Worked refactors

See `references/worked-refactors.md`: shallow→deep module; wrong-abstraction→duplication→right abstraction; pyramid-of-doom to guard clauses; parse-don't-validate replacing scattered `assert`s; layered shallow monolith to colocated deep module; characterization test before untangling legacy `calculateTax`.
