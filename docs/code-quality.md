# What this skillset is, and why it exists

## The problem

AI coding agents have a characteristic failure mode that's different from the failure modes humans have. A junior developer writes code that's confused but small. A senior developer writes code that's clear and confident. An AI agent — left to its own devices — writes code that's *plausible*: it looks like good code, it uses the vocabulary of good code, and it falls apart on contact with reality.

The specific patterns recur:

**Over-engineering.** Three layers of interfaces where one function would do. Factories for a single product. `IUserService` and `UserService` as separate files because that's what enterprise codebases tend to look like. Generic parameter knobs for variations that will never exist.

**Wrong abstractions.** A shared helper extracted from two call sites that happen to look similar but model different things. Six months later, the helper has accumulated flag parameters and conditional branches as each caller's needs diverge — and removing it has become a refactoring project.

**Shallow modules.** Many small classes and helper functions, each one a thin wrapper around a one-liner. To understand any single behavior, the reader hops through four files. Each layer hides nothing real.

**Pattern cargo-culting.** Strategy, Observer, Decorator, Factory — applied because the agent has seen the patterns in training, not because the forces these patterns resolve are actually present in the code.

**Cosmetically clean, structurally wrong.** Code that looks like a textbook example. Names that follow conventions. Comments that explain what each function does. And underneath, an architecture that punishes every future change.

The root cause is that **agents don't experience confusion**. A human writing code feels the cognitive load of bad structure — the slight friction of "wait, where does this come from?", the irritation of jumping between files, the unease of code they don't quite trust. Those signals are what stop a competent human from producing the patterns above. Agents have nothing to feel them with. They optimize for surface-level plausibility because surface-level plausibility is what their training rewards.

This skillset is an attempt to give agents *substitutes* for the feelings they lack — concrete, observable properties of code that correlate with the things humans would notice, plus decision procedures that activate when an agent is about to fall into a known trap.

## The philosophy

The skillset is grounded in a particular tradition of thought about software, and rejects another. A short version of both.

**What it endorses:**

The view that **complexity is the enemy** — not bad style, not missing tests, not the wrong language, but complexity itself. John Ousterhout's *A Philosophy of Software Design* defines complexity as "anything related to the structure of a software system that makes it hard to understand and modify," and identifies its root causes as obscurity (information you need is not where you look) and dependencies (changing one thing forces you to change another). Every other design rule in the skillset descends from this: depth, locality, naming, abstraction quality — all of them are angles of attack on complexity.

The view that **modules should hide secrets, not steps**. David Parnas in 1972 made the case that the right way to decompose a system is by the design decisions likely to change, not by the order things happen in. A module's interface should be small relative to what it hides. A module that only forwards calls to another module hides nothing and pays the interface tax for nothing.

The view that **simple is not the same as easy**. Rich Hickey's distinction: *simple* means not-braided-together, not-complected, made of independent concerns. *Easy* means familiar, near at hand, what you already know. Familiar tools are often complex (objects fuse state and behavior; ORMs fuse domain and persistence; inheritance fuses contract and implementation). Genuinely simple constructs — pure values, narrow functions, plain data — are often less familiar and therefore feel harder. The skillset prefers simple over easy.

The view that **duplication is far cheaper than the wrong abstraction**. Sandi Metz's argument, repeatedly validated in real codebases: when you abstract too early, on the basis of apparent duplication that turns out to be coincidence, the abstraction calcifies. Each new caller adds a flag parameter or a conditional branch. The "shared" code becomes a knot of accidentally-coupled cases, and unwinding it is harder than the duplication ever would have been. The right move is to wait — duplicate first, watch what changes, and abstract only when the real concept is visible.

The view that **beauty is a correctness heuristic**. DHH's claim, drawing on Christopher Alexander: code that reads well, sits well in its language, and matches the shape of its domain is usually more correct than code that doesn't. Not because aesthetic appeal magically produces correctness, but because the same skills — clarity, taste, fit — produce both at once. Code that is hard to read is usually hard to be right about.

The view that **cognitive load is the real budget**. Humans hold roughly four things in working memory at once. Code that requires tracking more cannot be safely changed. Artem Zakirullin's *Cognitive Load Developer's Handbook* makes this concrete: nested conditionals, flag parameters, deep inheritance, scattered logic, custom DSLs — each is a tax on the next reader. The skillset names mechanical proxies for these costs (nesting depth, parameter count, file-hop count, suspect-suffix names) so an agent can avoid them without needing to feel them.

The view that **code that changes together should sit together**. Carson Gross's "Locality of Behavior" — the idea that the behavior of a unit should be understandable by looking only at that unit. This is in productive tension with DRY (which says knowledge should have one representation). The skillset's resolution: DRY wins for true business rules; locality wins for coincidental shape similarity and glue code.

**What it rejects:**

The "Clean Code" tradition associated with the mid-2000s, especially Robert Martin's specific prescriptions: functions should be three lines; classes should be tiny; conditionals should always be replaced by polymorphism; comments are usually failures. These rules sound disciplined and produce, in practice, codebases of fragmented helpers where nothing is comprehensible at any single level. They optimize for a particular aesthetic of granularity rather than for readability or change-cost. Casey Muratori, John Carmack, Jonathan Blow and others have made the empirical case that this style produces worse code, not better — and the agent failure modes above are partly the result of training on codebases written in this style.

The skillset takes a different stance: **length is not the smell; mixed abstraction levels is.** A 200-line function that reads top-to-bottom like a recipe at a single level of detail is fine. A 30-line function that mixes domain logic with byte manipulation is not. Carmack's long, cohesive functions are better code than the textbook-clean fragmented version of the same logic.

It also rejects the tendency to treat **DRY and SOLID as commandments rather than tools**. Both contain useful insights. Neither survives literal application. SOLID's Single Responsibility Principle, taken too seriously, produces classes so fragmented that no one can find the responsibility. DRY, taken too seriously, fuses unrelated code that happens to look the same. Dan North's CUPID — Composable, Unix philosophy, Predictable, Idiomatic, Domain-based — is a more honest set of properties to aim for, because each is empirically observable in the resulting code.

It rejects the **pattern catalog as a checklist**. The Gang of Four book documented patterns that appeared organically in well-written object-oriented code. The pedagogical practice of teaching these patterns as templates to apply has produced two generations of code in which patterns are imposed rather than discovered, and where the patterns hide problems rather than solving them. The skillset's stance: use a pattern only when the forces it resolves are present in your code. Otherwise a function is enough.

It rejects **speculative generality**. The instinct to build hooks for needs that haven't materialized — interfaces with one implementation "in case we need another," configuration knobs that no one ever turns, plugin systems with one plugin. Martin Fowler's cost ledger: cost to build, cost of delay (it displaced a real feature), cost of carry (every reader must understand it), cost of repair (rip out when the guess turns out wrong). Four costs against a benefit that may never arrive.

## The approach

The skillset breaks the work into three narrow skills, each with a specific job.

**`writing-good-code`** is for greenfield authoring — when an agent is creating something new. It teaches the dispositions that should guide a first draft: stay concrete until forced to abstract; prefer deep modules over shallow ones; name in domain terms; cap cognitive load through specific numeric thresholds; parse external input once at the boundary and trust it afterward; handle errors by intent at the right level rather than reflexively at every level; colocate related code; write the comment you can't write in code.

**`refactoring-and-reviewing-code`** is for improving existing code without changing what it does. It teaches a specific discipline drawn from Kent Beck's *Tidy First?*: separate structure changes from behavior changes; move in tiny reversible steps; never delete code whose purpose you can't articulate (Chesterton's Fence); pin current behavior with characterization tests before refactoring legacy code; apply refactorings in a specific order that compounds (rename first, then flatten, then collapse shallows, then larger structural moves). It also catalogs the named code smells from Fowler's *Refactoring* and pairs each with its primary remedy.

**`abstraction-quality`** addresses the recurring decision that sits underneath both: should I extract this? Is this the right abstraction? It provides a six-step decision procedure for whether to extract anything (the concept must be nameable in the domain, three real call sites must share it, all callers must need the same behavior, the interface must be smaller than the implementation, inlining must produce visibly worse code, the domain must be stable enough that the shape won't shift). It also documents Sandi Metz's "go back" recovery: when an abstraction has gone wrong, inline it back into each caller, delete the dead branches, and re-derive only what genuinely re-extracts cleanly.

The three skills are designed to be mutually exclusive at trigger time — for any given task, exactly one fires. For tasks that need both refactoring and new behavior (a common case), the skills enforce sequencing: refactor first under a clean commit, then add behavior under a separate commit. The "two hats" discipline.

## What good code looks like, in this view

A function or module that is good by the skillset's standards has these properties:

It can be described in one sentence, in domain language, without "and."

Its interface is much smaller than its implementation. The caller sees a small surface; the implementation hides substantial complexity behind it.

Its name is from the problem domain — not `Manager`, `Helper`, `Util`, `Wrapper`, `Handler`, `Processor`, or any of the suffix-confessions that mean "I couldn't find a word."

It fails loudly. When something goes wrong, callers get a typed error or a crash, not a plausible wrong answer.

Its illegal states aren't representable. Combinations that shouldn't exist are compile errors, not runtime checks.

Its happy path runs straight down the left margin. Preconditions fail fast. Nesting stays under three.

It works at one level of abstraction at a time. It doesn't mix domain logic with wire protocol; it doesn't mix business rules with byte manipulation.

It's reversible. You could inline it back into its callers without structural loss. The fact that you don't have to is what makes it a good abstraction; the fact that you could is what proves it's not over-engineered.

It's the boring solution. Boring solutions fail predictably.

## What this skillset can't do

The skillset doesn't make a coding agent become a senior engineer. The signals a senior engineer uses to navigate a real codebase — knowledge of the team, intuition about which parts are about to be touched, judgment about which conventions are load-bearing and which are vestigial — aren't capturable in any document.

What it can do is reduce the rate at which agents produce the specific failures listed at the top: the over-engineered initial drafts, the wrong abstractions, the shallow modules, the cargo-culted patterns. It can give an agent reasons to wait before extracting, names for things it shouldn't do, and a procedure for noticing when it's about to do them anyway. That's the unit of progress: not perfect code, but fewer of the predictable mistakes.

The deeper bet is that an agent equipped with this skillset, working alongside a human who reviews its output, can produce code that's actually maintainable — not just code that ships. The standard for "shipped" is whether tests pass; the standard for "maintainable" is whether the next person can change it. Those are different bars, and the gap between them is where most of software's pain lives. This skillset is aimed at narrowing that gap.

## A note on tone

The skill files are written imperatively, with explicit thresholds and named procedures, because that's what works for agents. They're sharp because vague advice doesn't survive contact with a model that's optimizing for plausibility. If a particular rule reads as overconfident — "nesting depth ≤ 3," "extract only after the third caller," "interfaces with one implementation should be inlined" — that's deliberate. The threshold gives the agent something concrete to defer to. The accompanying explanation gives it the reasoning to override the threshold when overriding is right.

The same applies to the strong opinions about Clean Code, design patterns, and SOLID. These are positions held by working engineers who've watched the alternatives play out in real codebases for twenty years. They're not the only defensible positions, but they're more defensible than their opposites — and they're aligned with the kind of code most teams find pleasant to maintain three years later. If your team holds different views and your code stays maintainable, those views are working for you and you should keep them. The skillset is opinionated because opinions are what an agent can act on; humans always have the final say.

## Bibliography and sources

### Classical design philosophy
- Parnas, David. "On the Criteria To Be Used in Decomposing Systems into Modules," *Communications of the ACM*, Dec 1972. Used for: information hiding, secrets as the decomposition criterion, KWIC example.
- Ousterhout, John. *A Philosophy of Software Design*, 2nd ed., 2021. Used for: complexity = obscurity + dependencies; deep vs shallow modules; pull complexity down; define errors out of existence; strategic vs tactical; comments as design; the whole spine of the skillset.
- Alexander, Christopher. *The Timeless Way of Building* (1979), *A Pattern Language* (1977). Used for: quality without a name, habitability, pattern-language-not-catalog, why GoF drifted from the original.

### Modern practical school
- Hickey, Rich. "Simple Made Easy," Strange Loop 2011. Used for: simple ≠ easy, complecting, the construct→simpler-alternative table.
- Beck, Kent. *Tidy First?*, O'Reilly 2023. Used for: the 15 tidyings; structure vs behavior separation; tidy-first / after / later / never; coupling/cohesion as economic constructs.
- Hansson, David Heinemeier. *Rails Doctrine*; "Dependency injection is not a virtue"; "Test-induced design damage"; RailsConf keynotes. Used for: beauty as correctness heuristic, conceptual compression, critique of SOLID literalism, sharp knives, "Ruby is like Play-Doh."
- North, Dan. "CUPID — for joyful coding." Used for: Composable / Unix / Predictable / Idiomatic / Domain-based, critique of SOLID.
- Metz, Sandi. "The Wrong Abstraction"; POODR; Ruby Rogues #87 (Sandi's Rules). Used for: duplication > wrong abstraction, the go-back move, the 100/5/4 rules-of-thumb framing (and their "break with reason" caveat).
- Fowler, Martin. *Refactoring* 2e (JS); bliki on YAGNI, Workflows of Refactoring, Preparatory Refactoring. Used for: smell catalog, two hats, Rule of Three, make-the-change-easy, four costs of presumptive features.
- The Grug Brained Developer, grugbrain.dev (Carson Gross). Used for: saying no, cut points, factoring discipline, integration-test preference, DRY pragmatism, microservices skepticism.
- Muratori, Casey. "Clean Code, Horrible Performance"; "Semantic Compression." Used for: abstractions have measurable costs; inline-first then compress; procedural-first.
- Carmack, John. Inlining email (2007) + 2014 addendum; "Functional programming in C++." Used for: "function that doesn't exist can't cause a problem"; prefer inline over single-use extract in hot paths; purity pushes state to the edges.
- Blow, Jonathan. "Preventing the Collapse of Civilization." Used for: abstraction accretion as a civilizational risk; fewer layers.
- Pike, Rob. *Notes on Programming in C*; Gopherfest 2015. Used for: the 5 rules, data dominates, clear > clever, Go proverbs.
- Hunt & Thomas. *The Pragmatic Programmer*, 20th anniversary ed. Used for: DRY as knowledge-dedup (not text-dedup), orthogonality, ETC.

### Cognitive load, abstraction, readability, reasoning tools
- Zakirullin, Artem. "Cognitive Load developer's handbook," github.com/zakirullin/cognitive-load. Used for: the full catalog of high-load constructs and remedies; the onboarding test; DDD rituals critique; status-code smuggling.
- Cowan, Nelson. "The magical number 4 in short-term memory," 2001. Used for: the ~4-item working-memory bound.
- Spolsky, Joel. "The Law of Leaky Abstractions," 2002. Used for: leaky abstraction definition and canonical examples (TCP, SQL, SMB, 2D arrays, C++ strings).
- Wright, Hyrum, Titus Winters et al. hyrumslaw.com; *Software Engineering at Google*. Used for: with sufficient users, every observable behavior will be relied on.
- Thomson, Martin. "The Harmful Consequences of the Robustness Principle," IETF draft. Used for: strict-at-boundaries rebuttal to Postel.
- Gross, Carson. "Locality of Behaviour," htmx.org/essays. Used for: LoB principle and contrast with scattered jQuery.
- Torvalds, Linus. Linux kernel coding style. Used for: 3-level indentation rule.
- King, Alexis. "Parse, don't validate," lexi-lambda.github.io, 2019. Used for: parser vs validator, make illegal states unrepresentable, shotgun parsing.
- Bernhardt, Gary. "Boundaries / Functional Core, Imperative Shell," Destroy All Software. Used for: pure logic + thin effect shell; test strategy implications.
- Feathers, Michael. *Working Effectively with Legacy Code*, 2004. Used for: seams, characterization tests, sprout/wrap method-or-class, legacy defined as "code without tests."
- Acton, Mike. "Data-Oriented Design," CppCon 2014. Used for: design backward from data shape and volume.
- Gall, John. *Systemantics*. Used for: complex systems evolve from simple ones; clean-slate redesign presumed broken.
- Conway, Melvin. "How Do Committees Invent?", 1968. Used for: system reflects org structure; inverse maneuver for module design.
- Chesterton, G. K. *The Thing*, 1929 (the fence passage). Used for: do not remove what you cannot explain.

### Language-specific
- **TypeScript:** typescriptlang.org handbook; Matt Pocock (totaltypescript.com, mattpocock.com); Dan Vanderkam, *Effective TypeScript* 2e; TkDodo on barrel files; typescript-eslint docs.
- **Python:** PEP 8, 20, 257, 484, 585, 604; Astral (ruff, uv) docs; Brett Slatkin, *Effective Python* 3e; Raymond Hettinger PyCon talks.
- **C#:** learn.microsoft.com (C# coding conventions, Framework Design Guidelines, primary constructors tutorial); Stephen Toub on ConfigureAwait; Andrew Lock, Milan Jovanović, Nick Chapsas on primary-constructor caveats; Meziantou.Analyzer docs.
- **Go:** go.dev/doc/effective_go; go.dev/wiki/CodeReviewComments; go-proverbs.github.io; dave.cheney.net (Practical Go); Ian Lance Taylor "When To Use Generics"; Google Go Style Guide.

