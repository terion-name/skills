# Code smells — catalog and remedies

A smell is not a bug. It is a signal that the code may be structured in a way that makes future change harder. Each entry names the smell, describes the signal, and gives the remedy (Fowler's refactorings plus pragmatic variants). Apply the order in the parent SKILL.md: rename first, flatten control flow, inline shallows, then larger structural moves.

## Bloater smells

### Long Function

**Signal:** A function whose body spans many screens, and especially whose body mixes abstraction levels — domain logic next to byte manipulation next to logging.
**Caveat:** length alone is not the smell. A long function that stays at one level and reads top-to-bottom like a recipe can be perfectly fine (Carmack).
**Remedies:** Extract Function by abstraction level; Replace Temp with Query; Decompose Conditional; Introduce Parameter Object. Split by level, not by line count.

### Long Parameter List

**Signal:** more than ~4 parameters.
**Remedies:** Introduce Parameter Object (group related fields into a type); Preserve Whole Object (pass `user` not `user.id, user.name, user.email`); Replace Parameter with Query (let the function look up what it needs from an injected dependency); **Remove Flag Argument** (split into two functions named for each case).

### Large Class

**Signal:** a class with too many fields or methods; likely doing more than one thing.
**Remedies:** Extract Class (split out a cohesive set of fields + methods); Extract Subclass (if the split is along an "is-a" axis — rare, prefer Extract Class); Extract Interface (if consumers only need part of the class).

### Primitive Obsession

**Signal:** `string`s for emails, `float`s for money, bare ints for identities. Validation scattered.
**Remedies:** Replace Primitive with Object (`Money`, `EmailAddress`, `UserId`); Extract Class for data clumps. In TypeScript use branded types; in C# use records; in Go use defined types; in Python use `NewType` or dataclasses.

### Data Clumps

**Signal:** the same group of fields traveling together in many signatures (`start, end`, `x, y`, `street, city, zip`).
**Remedies:** Extract Class for the cluster; Introduce Parameter Object.

## Object-orientation abusers

### Switch Statements / Repeated Switches

**Signal:** the same `switch` on the same enum appearing in multiple places. A change to the enum requires updating all switches.
**Remedies:** **Choose based on shape.** If the enum is closed and stable and there are genuinely multiple behaviors per case, Replace Conditional with Polymorphism. If the enum is small or likely to be extended with data-only variations, a dispatch table (`Map<Case, Handler>`) or a `switch` expression keeps things flat and local. Do not introduce a class hierarchy for the sake of avoiding `switch`.

### Temporary Field

**Signal:** a field on an object that is only set under specific circumstances; most of the time it is null or default.
**Remedies:** Extract Class containing the field and the code that uses it; Introduce Special Case for the "missing" state.

### Refused Bequest

**Signal:** a subclass inherits methods it does not use or actively overrides to throw.
**Remedies:** Push Down Method/Field; Replace Subclass with Delegate (composition over inheritance).

### Alternative Classes with Different Interfaces

**Signal:** two classes do similar jobs but have different method names.
**Remedies:** Change Function Declaration to align names; Extract Superclass only if the concept is genuinely shared.

## Change preventers

### Divergent Change

**Signal:** one module has to be edited for many unrelated reasons (add a field, add a UI concern, add a persistence concern).
**Remedies:** Split Phase (separate input parsing from processing); Move Function to the module that owns the concern; Extract Class for each reason for change.

### Shotgun Surgery

**Signal:** one conceptual change forces edits across many modules.
**Remedies:** Move Function and Move Field to consolidate the concern; Combine Functions into Class; Inline in-Function Module that fragments the concept.

### Parallel Inheritance Hierarchies

**Signal:** every time you make a subclass in one hierarchy, you must make a corresponding subclass in another.
**Remedies:** Move Function and Move Field so one hierarchy references the other; prefer composition.

## Dispensables

### Comments (as deodorant)

**Signal:** a comment explains what a badly named thing does.
**Remedies:** Rename; Extract Function using the comment's text as the new name; delete the comment once the code is self-explanatory.

### Duplicated Code

**Signal:** identical or near-identical code in two or more places.
**Remedies:** **Stop and think before extracting.** Is the duplication coincidental or does it represent shared knowledge? If shared, Extract Function or Pull Up Method. If coincidental, leave duplicated — extraction will produce the Wrong Abstraction. See the `abstraction-quality` skill.

### Lazy Element

**Signal:** a class, function, or file that does not earn its keep. A one-line wrapper; a base class with no subclasses; a factory with one product.
**Remedies:** Inline Function; Inline Class; Collapse Hierarchy.

### Speculative Generality

**Signal:** abstract classes, unused parameters, plugin hooks, configuration knobs — all for needs that have not materialized.
**Remedies:** Collapse Hierarchy; Inline Class; Remove Dead Code; Remove Parameter. Delete first, ask questions later if someone misses it.

### Data Class

**Signal:** a class that is just a bag of public fields with getters/setters and no behavior.
**Caveat:** sometimes a DTO or record is the right design (wire format, config). Not every data-holder is a problem.
**Remedies:** Move Function to the data class if behavior elsewhere repeatedly manipulates its fields (Tell-Don't-Ask); Encapsulate Record/Collection when mutation needs invariants.

### Dead Code

**Signal:** unreachable branches, unused variables, functions no one calls.
**Remedies:** delete. `git` remembers.

## Couplers

### Feature Envy

**Signal:** a method uses another object's data far more than its own.
**Remedies:** Move Function to the object it envies.

### Inappropriate Intimacy

**Signal:** two classes poking at each other's internals (private state access, mutual knowledge of implementation).
**Remedies:** Move Function and Move Field; introduce a shared abstraction if one genuinely exists; Replace Inheritance with Delegation (if intimacy comes from a bad superclass relationship).

### Message Chains / Train Wrecks

**Signal:** `a.b().c().d().e()` — caller traces multiple contexts.
**Remedies:** Hide Delegate (add an intent-level method on `a`); Extract Function + Move Function to relocate the chain behind a meaningful name. See Law of Demeter with its Tell-Don't-Ask counterpart.

### Middle Man

**Signal:** a class whose public methods mostly forward to another object's methods, adding nothing.
**Remedies:** Remove Middle Man (call the delegate directly); Inline Function.

### Insider Trading

**Signal:** modules that share too much internal knowledge, usually by exposing internal state between "collaborators."
**Remedies:** Move Function and Move Field to consolidate; Hide Delegate; introduce a clearer bounded context.

## Other smells

### Mysterious Name

**Signal:** a name that does not tell you what the thing is or does.
**Remedy:** Rename. Before any other refactoring, rename. It is free, reversible, and shifts the conversation.

### Mutable Data

**Signal:** data mutated in far-away places causes hard-to-trace bugs.
**Remedies:** Encapsulate Variable (hide direct access behind getters/setters, then add invariants); Split Variable (one variable used for two distinct meanings); Separate Query from Modifier (a function that reads should not also write); Replace Derived Variable with Query (compute on demand instead of caching).

### Global Data

**Signal:** module-level mutable state reachable from anywhere. Tests become coupled; debugging becomes hard.
**Remedies:** Encapsulate Variable behind a narrow interface; make the state explicitly injected where it is needed.

### Loops

**Signal:** an imperative loop that is actually a pipeline (filter → map → reduce).
**Remedy:** Replace Loop with Pipeline when the pipeline reads at a glance. Keep the loop when the pipeline would be obscured by intermediate captures or side effects.

### Repeated Assertion

**Signal:** the same input check is performed at multiple layers of the call tree.
**Remedy:** Parse, don't validate. One parse at the boundary; downstream trusts the type. See `writing-good-code/references/errors-and-boundaries.md`.

## Mapping table

| Smell | First-choice remedy | See also |
|---|---|---|
| Mysterious Name | Rename | `writing-good-code/references/naming.md` |
| Duplicated Code | Extract Function, *if* Rule of Three + name + shared concept | `abstraction-quality` skill |
| Long Function | Extract Function by abstraction level; Decompose Conditional | `tidyings.md` |
| Long Parameter List | Introduce Parameter Object; Remove Flag Argument; Preserve Whole Object | — |
| Global/Mutable Data | Encapsulate Variable; Split Variable | — |
| Divergent Change | Split Phase; Move Function; Extract Class | — |
| Shotgun Surgery | Move Function; Combine Functions into Class | — |
| Feature Envy | Move Function | — |
| Data Clumps | Extract Class; Introduce Parameter Object | — |
| Primitive Obsession | Replace Primitive with Object; Extract Class | — |
| Repeated Switches | Replace Conditional with Polymorphism *or* dispatch table | — |
| Loops | Replace Loop with Pipeline (when readable) | — |
| Lazy Element | Inline Function; Inline Class; Collapse Hierarchy | — |
| Speculative Generality | Collapse Hierarchy; Remove Dead Code | `anti-patterns.md` |
| Temporary Field | Extract Class; Introduce Special Case | — |
| Message Chains | Hide Delegate; Extract + Move Function | — |
| Middle Man | Remove Middle Man; Inline Function | — |
| Insider Trading | Move Function; Hide Delegate | — |
| Large Class | Extract Class; Extract Subclass | — |
| Alternative Classes | Change Function Declaration; Extract Superclass | — |
| Data Class | Move Function in (Tell-Don't-Ask) — or keep if truly a DTO | — |
| Refused Bequest | Push Down Method; Replace Subclass with Delegate | — |
| Comments (as deodorant) | Rename; Extract Function named by the comment | — |
