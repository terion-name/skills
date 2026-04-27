# Reasoning tools for review and refactoring

A handful of named principles repeatedly help you decide whether a change is safe, whether a redesign is real progress, and whether a "cleanup" might break something you cannot see. Apply them as checklist items in code review and as guardrails on your own changes.

## Chesterton's Fence

> "Reforms should not be made until the reason for the existing state of affairs is understood."

Before deleting any code that exists for an unclear reason, find out *why* it is there. Workflow:

1. **`git blame` the line(s).** Read the commit message.
2. **Read the linked ticket / PR description.** What problem was being solved?
3. **Search the bug tracker** for keywords from the suspect code.
4. **Search the codebase** for related comments, tests, related PRs.
5. **Ask** if you have someone to ask.

If, after a bounded search, you still cannot articulate what the code is for — assume you are missing context and **leave it alone**. Add a comment if helpful: `// purpose unclear, kept pending #4729`.

The most expensive bugs come from "I cleaned that up because it looked unnecessary."

## Hyrum's Law

> "With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody."

Even private behaviors people observe accidentally become contracts. Examples of "behaviors users will depend on":

- The exact text of error messages (parsed by clients).
- Iteration order over a set or map (assumed stable).
- Specific timing characteristics (used as a backpressure signal).
- The order in which side effects happen.
- The serialization format of dates / numbers.
- The precise set of headers in an HTTP response.
- The exact shape of returned JSON, including key order.
- How many database queries a function performs.
- Whether a method throws or returns null on missing input.

**Implications for review:**

- Any "purely internal" change to an API needs to consider what callers might be observing.
- Documented behavior is not the only contract; observable behavior is.
- Versioning policy on public APIs should be conservative.
- Adding features is safer than removing them, even when removal "looks safe."

When refactoring an internal API, ask: what observable behaviors am I changing? If the answer includes anything beyond the documented contract, treat it as a behavior change, not a refactor.

## Gall's Law

> "A complex system that works is invariably found to have evolved from a simple system that worked. A complex system designed from scratch never works and cannot be patched up to work. You have to start over with a working simple system."

When someone proposes a "ground-up rewrite" or a "new framework that will handle all our needs," remember Gall's Law. The complex system is not a system anyone designed — it is the accumulated consequence of dozens of small fixes to a simple system that grew. A clean-slate design omits all of them, often unwittingly.

**Practical applications:**

- Prefer evolution over rewrite. Strangle, don't replace.
- When forced to redesign, start from a simple system that works and grow it.
- Be skeptical of "it should work" arguments — production has a way of revealing what the design missed.

There are real cases where rewrite is correct (fundamental architectural mismatch, technology stack EOL). The rule is not "never rewrite," it is "presume rewrite is wrong until the case is overwhelming."

## Conway's Law

> "Organizations that design systems are constrained to produce designs which are copies of the communication structures of these organizations."

The architecture you ship will mirror your team structure. If three teams own a feature, you will ship a three-service feature.

**Implications for refactoring:**

- A proposed module split that does not match team ownership will be friction-laden. The boundary will be edited by both teams; PRs will require two reviews; ownership disputes will arise.
- A proposed merge of modules owned by different teams will be politically fraught.
- Sometimes the right answer is to change the organization, not the architecture (the *inverse Conway maneuver*).

When you propose a structural change, ask: who owns the result? If the answer is unclear or "two teams," the structure is wrong (or the org is).

## Postel's Law and Thomson's rebuttal

**Postel's Law (Robustness Principle):** *"Be conservative in what you do, be liberal in what you accept from others."*

Postel wrote this for TCP, in a world where independent implementations were trying to interoperate without coordination. It worked in that context. In modern systems, especially internal ones, "liberal acceptance" creates technical-debt time bombs.

**Martin Thomson's critique** (IETF draft, "The Harmful Consequences of the Robustness Principle"):

- Liberal acceptance hides bugs in senders. Senders are never punished for sending wrong data; the bug accumulates.
- Implementations diverge. Some accept malformed inputs; some don't. The de-facto interop spec becomes "whatever the most lenient implementation does."
- Backward compatibility becomes permanent. Once one liberal implementation accepts a bug, every other implementation must accept it too, forever.
- New implementations face an impossibly fuzzy spec.

**Practical rule:**

- **At internal boundaries between services / modules you control:** be strict. Reject unknown fields. Validate enums. Refuse partial data. Make sender bugs loud.
- **At public APIs consumed by third parties:** strict on format, document precisely, version explicitly, deprecate slowly.
- **At external integrations with legacy systems you cannot change:** liberal acceptance earns its keep — but log every fallback. Track what the legacy sender is actually doing so you can negotiate cleanup.

## KISS (Keep It Simple, Stupid)

A reminder, not a method. The point is direction:

- Between two solutions that meet the requirements, prefer the simpler.
- Simpler ≠ shorter. Sometimes the longer, more explicit version is simpler because it has fewer hidden behaviors.
- The right baseline is "boring." Boring solutions fail predictably.
- "Clever" is a yellow flag. The cleverness will land on a future debugger.

## Principle of Least Astonishment

A function, type, or operator should do what its name and shape suggest, and nothing more. Surprises are a tax on every reader.

- A `get_*` should not write.
- An `is_*` should return bool, not throw.
- Iteration should not mutate the iterable.
- An operator overload should not allocate or perform I/O.
- `==` should be reflexive, symmetric, and transitive (and yes, NaN is a known violator; do not invent more).
- A library function should not change global state without saying so in its name.

## Demeter and Tell-Don't-Ask (a tension)

**Law of Demeter:** *Only talk to your immediate friends.* `a.b.c.d` reaches across multiple objects' internals. Bad.

**Tell, Don't Ask:** Don't pull data out of an object to manipulate it externally — *tell* the object to do the work.

Both push you toward the same outcome (less coupling), but they conflict at the margins:

- A pure functional pipeline (`xs.filter(...).map(...).reduce(...)`) violates Demeter strictly read but is fine — these are immutable transformations on a value, not "asking" anything.
- A persistent-collection chain that ends in mutation is a smell.
- A getter chain that traverses business objects (`order.customer.address.country.taxRules.find(...)`) is the bad case Demeter targets — the caller now knows too much about the order's internals.

**Rule of thumb:** chains over collections of values are fine. Chains across business objects to extract decision data are a Hide Delegate / Move Function opportunity.

## YAGNI (You Aren't Gonna Need It)

Do not build for needs you have not seen. The cost of unneeded generality (Fowler):

- **Cost to build** — wasted if unused.
- **Cost of delay** — displaced a real feature.
- **Cost of carry** — every reader must understand it.
- **Cost of repair** — rip out when the guess turns out wrong.

Four costs against a benefit that may never arrive.

## Brooks's "No Silver Bullet"

> "There is no single development, in either technology or management technique, which by itself promises even one order-of-magnitude improvement within a decade in productivity, in reliability, in simplicity."

When evaluating a proposed framework, methodology, or AI tool that promises 10× improvement: skepticism. The history of software is the history of silver bullets that turned out to be ordinary lead.

## How to apply these in review

When reviewing a PR, ask:

- **Chesterton:** is anything being deleted whose purpose I cannot articulate?
- **Hyrum:** am I changing observable behavior? Who might depend on it?
- **Gall:** if this is a redesign, is it a rewrite from scratch (red flag) or an evolution (green flag)?
- **Conway:** does the proposed structure match team ownership?
- **Postel/Thomson:** at an internal boundary, are we strict? At an external one, are we documented?
- **YAGNI:** are we building for needs that exist or for needs we imagine?
- **Least Astonishment:** does each function do what its name suggests?

A "yes" to the right column on each is the bar.
