# Anti-patterns catalog

A catalog of named anti-patterns to recognize and avoid. Each entry names the pattern, describes the signal, and gives the remedy. Most AI-generated code fails here before it fails anywhere else.

## Over-engineering family

### Shallow Module

**Signal:** many small classes or functions where a few deep ones would do. Interface-to-implementation ratio near 1.
**Example:** `UserRepository.getById` that only calls `db.query("select * from users where id=?")`.
**Remedy:** inline until a boundary that actually hides something appears. Introduce the wrapper only when the underlying API is legitimately being hidden or adapted.

### Speculative Generality

**Signal:** hooks for imagined future needs. Unused parameters. Abstract classes with one concrete subclass. Plugin systems with one plugin. Config for things that never vary.
**Example:** `IPaymentProvider` interface with one `StripeProvider` implementation "in case we switch providers."
**Remedy:** delete until the second real need arrives. When it does, you will know the real shape of the variation — which is almost never the shape you guessed.

### Lazy Element

**Signal:** a class, function, or file that does not pay its way. A one-line wrapper. An `IFoo` with a single implementation. A `utils.ts` with two functions.
**Remedy:** inline.

### Pattern Cargo-Cult

**Signal:** Factory, Strategy, Observer, Decorator, Builder applied because "it is a design pattern," not because the forces the pattern resolves are actually present.
**Example:** `OrderFactory.create(orderType)` that is a 3-case switch, used from one place.
**Remedy:** use patterns only when the forces they resolve are present. A function beats a Strategy when there is one strategy. A switch beats a Factory when there are three subtypes.

### Enterprise-Java-in-every-language

**Signal:** `IAbstractServiceProviderFactoryFactory`. Deeply layered ceremonies. DI container configurations longer than the logic they wire.
**Remedy:** a sealed class with clear methods. Delete every `Factory` you can. "Framework disease" thrives in systems that pretend to be replaceable but never are.

### Utility Grab Bag

**Signal:** `utils.ts`, `helpers.py`, `common/`, `lib/` with a dozen unrelated functions.
**Remedy:** move each function next to the concept it serves. If no concept exists, the function may not need to exist. If a function is genuinely cross-cutting (a date formatter used everywhere), give it a specific name (`dateFormatting.ts`), not `utils.ts`.

### Over-Layered Architecture

**Signal:** Controller → Service → UseCase → Repository → Mapper → Gateway for what is essentially CRUD.
**Remedy:** collapse to the layers that hide real secrets. A repository that only wraps `db.query` hides nothing. A service that only forwards to the repository hides nothing.

### Interface per Class

**Signal:** `IUserRepository` + `UserRepository`, one implementation, introduced "for testability."
**Remedy:** keep the class. Most test doubles can be created by other means (passing a function, using a test subclass, using a module-level mock). Introduce the interface when the second implementation exists, or when a test genuinely cannot be written otherwise.

### Dependency Injection for Its Own Sake

**Signal:** injecting `IClock` to mock time when `Date.now()` would work fine with a simple override; injecting `ILogger` through every class; DI containers wiring half the codebase.
**Remedy:** use DI where real variation exists (multiple real implementations, or a genuine test seam). Use direct dependencies otherwise. Module-level singletons for logging are fine.

### Premature Microservices

**Signal:** a service-per-domain-concept for a team of five engineers. Cross-cutting changes require coordinating four deploys.
**Remedy:** merge services that always change together. Use a modular monolith until service boundaries are forced by scaling, team structure, or technology needs.

## Wrong Abstraction family

### Flag-Parameter Helper

**Signal:** `render(user, { includeAvatar, compact, legacyMode })` — each boolean toggles a branch inside.
**Remedy:** split into functions named for each case (`renderCompactUser`, `renderLegacyUser`). Inline if the branches are unrelated. See `errors-and-boundaries.md` and `abstraction-quality/SKILL.md`.

### Conditional Drift

**Signal:** a shared helper grows new `if`s keyed on callers' shape over time. Each new caller adds a new flag.
**Remedy:** Metz's go-back move — inline into each caller, delete dead branches per caller, re-derive only what genuinely re-extracts cleanly.

### Parameterized Everything

**Signal:** abstracting around the *differences* rather than around a concept, producing a "generic" function that is essentially a big switch.
**Remedy:** name the concept. If you cannot, duplicate.

### Cross-Domain Shared Validator

**Signal:** one `validateLength(min, max)` used for usernames (3–20), comments (1–2000), and tweets (1–280).
**Remedy:** three named validators (`validateUsername`, `validateComment`, `validateTweet`). The constants matter more than the shared logic. The "duplication" of the `min <= len && len <= max` pattern is trivial and not worth coupling three unrelated rules.

### Middleman Abstraction

**Signal:** class or module whose every public method forwards to another object's method, adding nothing.
**Remedy:** Inline. Remove Middle Man (Fowler).

### Premature Extract Function

**Signal:** a one-use helper extracted "for readability" on the first write. Reader must jump to understand it.
**Remedy:** inline. Extract only when the name *adds* information the code alone does not convey, and when the body is used at least twice (or is genuinely complex in isolation).

## Readability family

### Pyramid of Doom

**Signal:** deeply nested conditionals; happy path buried three or four indents deep.
**Remedy:** guard clauses; early returns. See `readability.md`.

### Clever One-Liner

**Signal:** a comprehension, chain, or ternary nested past the point where the reader can predict the result at a glance.
**Remedy:** split into named temporaries. Kernighan: if you wrote it as cleverly as possible, you cannot debug it.

### Stacked Negations

**Signal:** `if (!a && !b && !(c || !d))`.
**Remedy:** name each predicate, or re-state positively. Double negatives compound reader load.

### Comments as Deodorant

**Signal:** a comment that explains what a badly named thing does.
**Remedy:** rename until the comment is redundant. Delete the comment.

### Hungarian Revival

**Signal:** `strName`, `iCount`, `arrUsers`, `m_foo` in languages where types are visible.
**Remedy:** delete the prefixes.

### Message Chain / Train Wreck

**Signal:** `a.b().c().d().e()`. Reader traces five contexts in one expression.
**Remedy:** Hide Delegate, or apply Tell-Don't-Ask. Expose an intent-level method (`a.doTheThing()`) instead of forcing the caller to navigate.

### Magic Numbers

**Signal:** unexplained constants embedded in code. `if (retries > 5)` — why 5?
**Remedy:** named constants in the module where the policy lives.

### Inconsistent Vocabulary

**Signal:** `fetchUser`, `getUser`, `loadUser`, `retrieveUser` all used for the same operation.
**Remedy:** pick one, document, enforce.

## Boundary family

### Validate-Then-Use

**Signal:** `assert`s or type guards repeated throughout the call tree re-checking the same invariants.
**Remedy:** parse into a refined type once at the boundary; trust the type afterward.

### Shotgun Parsing

**Signal:** processing input and validating it interleaved. Mutation occurs before the input is fully validated.
**Remedy:** parse first (completely), act second.

### Liberal Acceptance Inside Trusted Code

**Signal:** silent fallthroughs, `try: int(x) except: return 0`, accepting inputs with unknown fields and ignoring them.
**Remedy:** strict parsing at the boundary. Surface errors. Reject unknown fields. Postel's "be liberal" was not meant for internal boundaries.

### HTTP Status Code Smuggling

**Signal:** `401` meaning "token expired" vs `403` meaning "role lacks permission" where the HTTP spec does not imply that distinction.
**Remedy:** self-describing error codes in the response body: `{ "error": "TOKEN_EXPIRED", "retryable": true }`.

### Silent Catch

**Signal:** `try { … } catch (_) { }`.
**Remedy:** never. At minimum log with context and re-throw; ideally return a typed result the caller must handle.

### Null Sentinels

**Signal:** `indexOf(x) === -1` style; functions that return `-1`, `""`, or `0` to mean "not found."
**Remedy:** `null` / `undefined` / `Option<T>` / `Result<T, E>`.

## Process family

### Mixing Structure and Behavior in One Commit

**Signal:** a commit message says "refactor and add X."
**Remedy:** split into two commits. One refactor (behavior preserved, tests unchanged), one behavior change.

### Big Refactor That Never Lands

**Signal:** a multi-day branch that cannot be merged because it has diverged from `main`.
**Remedy:** stash and break into tidyings each of which ships green. If you cannot land a refactor in a day, the scope is wrong.

### Preserving a Bad Abstraction Out of Sunk Cost

**Signal:** "we already built the framework, let's extend it."
**Remedy:** go back. Inline, delete dead branches per caller, re-derive. The time already spent is not relevant to the decision.

### Deleting Code You Do Not Understand

**Signal:** "this check seems redundant, I'll remove it."
**Remedy:** Chesterton's Fence. `git blame`, find the commit, read the ticket. If no reason is findable within a bounded search, assume you are missing context and leave the check.

### Refactoring Without Tests

**Signal:** changing untested code "carefully."
**Remedy:** find a seam, write a characterization test pinning current behavior (bugs included), then refactor.

## Language-specific appearances

These show up cross-language:

- **TypeScript:** `as any`, `!` non-null assertions in production code, barrel files that hide circular imports, `namespace`, `enum` with string values used for discrimination (discriminated unions work better), over-generic utility types.
- **Python:** mutable default arguments, `except:` without a type, `type(x) == X`, metaclass abuse, deep inheritance, `from module import *`.
- **C#:** `IFoo`-per-`Foo`, service-locator in place of DI, `async void`, blocking on async with `.Result` or `.Wait()`, over-use of reflection, inheritance-first design, "Enterprise Java" factories.
- **Go:** large interfaces at package boundaries ("accept interfaces, return structs"), `interface{}` in public APIs, reflection outside reflection-specific libraries, `init()` with logic, naked returns in non-trivial functions, `panic` for ordinary errors.

See each `lang-*.md` for detail.

## Quick scan

Before finishing code, grep for:

- `Manager|Helper|Handler|Util|Processor|Wrapper|Info|Data|Base|Abstract` — each must justify itself.
- `any`, `interface{}`, `object`, `Object` — each must be at a true boundary with `unknown` narrowing immediately.
- `// TODO` without owner and date.
- Non-domain-language names in domain code.
- Boolean parameters in public APIs.
- Files over ~300 lines without TOC/section separators.
- `try { … } catch (_) { }`.
- Three or more levels of nesting.
