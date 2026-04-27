---
name: writing-good-code
description: Use when writing new code in any language — implementing a feature, adding a module, sketching a design, writing a script, building an endpoint, or extending existing code with a new piece. Covers naming, module shape, abstraction depth, error handling, readability, language idioms, and practical tactics against over-engineering. Trigger whenever the user asks to "write", "implement", "build", "add", "create", "design", "prototype", or "extend" code, a function, a class, a module, a component, a script, an endpoint, or a feature — even when they do not say "quality" or "clean code". Also trigger when the user says they want code that is "simple", "clean", "readable", "maintainable", "elegant", or "idiomatic". Do NOT use for pure refactoring of existing code without behavior change (use refactoring-and-reviewing-code); do NOT use for a focused decision about whether one specific abstraction is worth extracting (use abstraction-quality).
---

# Writing good code

Write new code that is **simple, readable, and correct**, biased against over-engineering. The root causes of bugs are complexity and surprise; your job is to reduce both. Applies to TypeScript, Python, C#, Go, and most mainstream languages.

## The five claims

Before writing anything, internalize these. Every rule below descends from them.

1. **Working code is not enough.** The unit of progress is code that makes the *next* change easy — not hypothetical future changes. If you are optimizing for flexibility you have not needed yet, stop.
2. **You are writing for the next reader.** If a reader would be confused, the code is wrong, not the reader. You cannot feel confusion, so use the mechanical proxies in `references/cognitive-load.md` as your substitute for the feeling.
3. **Duplication is cheaper than the wrong abstraction.** When uncertain, duplicate. Extract only when the third occurrence makes the shared concept obvious and you can name it in domain terms.
4. **Depth beats cleverness.** A module with a small interface and a substantial implementation is a gift to every future reader. A pile of tiny helpers that together do one thing is not.
5. **Different is different.** Two code sites that look similar but behave differently are a bug factory. If two things are the same, make them the same; if they are different, make them visibly different.

## Pre-flight before you write anything

Seconds of thought save hours of rework. Run this every time.

1. **Restate the task in one sentence of domain language.** If you cannot, you do not understand it yet — ask or read more. The sentence should use the words the user would use, not framework or pattern words.
2. **Name the data.** What shapes go in and out? What is the identity of each entity? Draw the data first, code after. If the shape is uncertain, prototype with a literal example value.
3. **Pick the boundary.** What is the seam between this code and its callers? Keep the interface narrow. Everything in the interface is a promise you will pay to keep (Hyrum's Law: users will depend on every observable behavior, intended or not).
4. **Check for existing shapes.** Scan the codebase for the nearest existing function or module doing something similar. Match its naming, error style, file layout, and test patterns unless you have a concrete reason to deviate. Consistency with nearby code is worth more than local optimality.
5. **Choose the language idiom.** Load `references/lang-<language>.md` if you are about to write non-trivial code in a language you have not just been editing.

## Decision procedure while writing

Apply these in order. Earlier rules override later ones on conflict.

### Rule 1 — Keep it concrete until it resists

Write procedurally and inline first. Resist pre-extracting helpers, pre-introducing interfaces, pre-creating folders. Architecture emerges from iterated compression; it is rarely designed well up front.

- If a block has a clear single purpose, a stable shape, and can be named in the domain's vocabulary, then extract it.
- If it has none of those, leave it inline. Extracting too early plants the seed of a bad abstraction.
- Apply the **Rule of Three**: first time, write it. Second time, wince and duplicate. Third time, *consider* extraction — and only if all three uses share a concept, not just a shape. See `references/anti-patterns.md` "Wrong Abstraction".

### Rule 2 — Make modules deep, not shallow

A module (function, class, file, package) should hide substantially more complexity than its interface exposes. Depth is the single best abstraction metric.

- **Depth test:** count parameters + method signatures in the public interface; count non-trivial lines in the implementation. If the first number is close to the second, the module is shallow. Either inline it or redesign it so the interface can be smaller.
- Pass-through methods and pass-through variables are red flags. If a method only forwards to another method with the same signature, delete one of them.
- Push complexity **down**, not up. The implementer suffers so callers do not. Prefer computing a sensible default internally over adding a config knob; prefer clamping indices internally over making callers check bounds.

### Rule 3 — Name things as they exist in the domain

Names are a diagnostic. If you cannot name a function or class crisply in the domain's language, the abstraction is wrong.

- Prefer nouns from the problem domain: `Invoice`, `RetryPolicy`, `Session`, `OrderLine`. Avoid generic suffixes: `Manager`, `Helper`, `Handler`, `Processor`, `Util`, `Wrapper`, `Info`, `Data`, `Context`, `Base`, `Abstract*`, `*Impl`. If the best name you can find uses one of these, the module probably does not correspond to a real concept.
- Name length should correlate with scope. Loop index: `i`. Local temporary: `count`. Module-level symbol: `activeUserCount`. Public API: precise multi-word name.
- See `references/naming.md` for the full guide.

### Rule 4 — Cap cognitive load

Use these numeric proxies for reader load. Each is a warning threshold, not a hard limit — crossing one without reason is a smell.

- **Nesting depth ≤ 3.** Beyond, invert with guard clauses and early returns.
- **Conditions per `if` ≤ 3.** Beyond, extract named boolean intermediates.
- **Function parameters ≤ 4.** Beyond, introduce a parameter object, preserve a whole object, or split the function.
- **Flag parameters: 0 is ideal, ≥2 is strong evidence of the Wrong Abstraction.**
- **Inheritance depth ≤ 2.** Prefer composition.
- **File-hops to understand one behavior unit: 0–1 ideal, 2 OK, 3+ is a Locality of Behavior violation.**

See `references/cognitive-load.md` for the full checklist with remedies.

### Rule 5 — Handle errors with intention

Errors at boundaries, not sprinkled through every function. Choose one of:

- **Return a typed result** (`Result<T, E>`, discriminated union, `(value, error)` tuple) when the failure is expected and the caller must decide what to do.
- **Throw / panic** when the failure is a programmer error or unrecoverable; let it propagate to a boundary that logs and maps.
- **Define the error out of existence** when possible: return an empty list instead of null; clamp indices; make "already exists" a no-op when that matches intent.

Never silently catch and swallow. Never use exceptions for control flow in the common case. See `references/errors-and-boundaries.md`.

### Rule 6 — Parse at the boundary, trust inside

External data — HTTP, DB, env vars, IPC, user input, filesystem — is `unknown` until validated. Parse it once into a refined domain type, then operate on that type. Use a schema library (Zod, Pydantic, FluentValidation, equivalent) instead of scattering ad-hoc guards through the call tree.

Make illegal states unrepresentable. Use `NonEmptyList`, branded IDs, discriminated unions for state machines. If field A is only meaningful when field B is set, model that in the type, not in runtime assertions. See `references/errors-and-boundaries.md`.

### Rule 7 — Colocate by default

Code that changes together should sit together. A component's behavior should be visible in that component (Carson Gross's "Locality of Behavior"). Resist splitting a feature across `controllers/`, `services/`, `repositories/`, `mappers/`, `dtos/` when the codebase does not already demand it. Organize top-level folders by **domain** (`patients/`, `billing/`), not by **layer** (`models/`, `views/`, `services/`).

### Rule 8 — Write the comment you cannot write in code

Code expresses *what* and *how*. Comments are for *why*, *contract*, and *intent not expressible in types*:

- Units, invariants, preconditions, postconditions.
- Non-obvious rationale ("this order prevents a deadlock on X").
- Cross-module contracts ("caller owns the returned handle").

Do not write comments that restate the code. If a comment would just restate, the name is wrong — rename until the comment becomes redundant. Ousterhout's "write the comment first" is a design tool: if you cannot write a one-line contract for a function, its design is not ready.

## Language idioms

Load the matching reference when writing non-trivial code in that language:

- `references/lang-typescript.md` — strict tsconfig, discriminated unions, branded types, `as const` + `satisfies`, parse-don't-validate with Zod, Result types, classes sparingly, barrel-file warning.
- `references/lang-python.md` — PEP 8/20, typing at boundaries, Protocol vs ABC, dataclass vs Pydantic, EAFP, tooling (ruff/mypy/uv).
- `references/lang-csharp.md` — records, pattern matching, nullable reference types, primary-constructor caveat, async all the way, DI without overkill, no `IFoo` per `Foo`.
- `references/lang-go.md` — small interfaces at the consumer, accept interfaces / return structs, errors as values with wrap, zero value useful, generics sparingly.

## Anti-patterns to sanity-check against

Before calling the code done, scan `references/anti-patterns.md`. The top offenders in AI-generated code:

- **Shallow modules** — many small classes/functions where a few deep ones would do.
- **Speculative generality** — interfaces, generics, plugin hooks for needs that are not real.
- **Premature design patterns** — Factory/Strategy/Observer applied where a function or a switch would suffice.
- **Wrong abstractions with flag parameters** — one function, many `if` branches, growing callers.
- **Utility dumping grounds** — `utils.ts`, `helpers.py`, `common/` with unrelated functions piled together.
- **Over-layered code** — Controller → Service → UseCase → Repository → Gateway when the domain is CRUD.
- **Interface-per-class** — `IFoo` + `Foo` with one implementation, added "for testability".
- **Clever one-liners** — comprehensions, pipelines, ternaries nested until the reader cannot predict the result.
- **Comments as deodorant** — commenting around a bad name instead of renaming.

## When uncertain

- Prefer the boring solution. Boring solutions fail predictably.
- Prefer the solution that is easiest to **delete** or reverse.
- Prefer the solution with the smallest diff to existing code.
- If still uncertain, write the shortest version that works, note your uncertainty in a comment, and stop. Do not generalize preemptively.

## Worked examples

See `references/worked-examples.md` for before/after demonstrations of shallow→deep modules, wrong-abstraction recovery, clever-vs-clear, error-by-type-vs-runtime, parse-don't-validate, guard clauses, and branded types.
