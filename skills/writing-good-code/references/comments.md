# Comments

Comments are part of the design. The position that "good code needs no comments" is a misreading of older practice that has been formally rebutted by every serious treatment of the subject. Even McConnell — whose `Code Complete` is often cited as the source of the "self-documenting code" maxim — has clarified he never meant comments should be absent, only that *bad* comments are worse than none. Ousterhout makes the case directly: "good comments can make a big difference in the overall quality of a system." Every author worth reading on this — Hunt & Thomas, Boswell & Foucher, Stroustrup, Raskin, Knuth — agrees. So does practical experience: code without comments may be readable today and incomprehensible in three months, because the *why* is gone.

This is especially important for AI-generated code. Agents tend to under-comment because they have absorbed "self-documenting code" as a hard rule rather than a heuristic, and because comments cost output tokens with no immediate visible payoff. The result is code that looks clean in isolation and becomes opaque the moment a human (or another agent) tries to maintain it.

**Default stance: write the comments.** Lean toward more rather than fewer. Skip them only when a reasonable reader who knows the language and domain would learn nothing from them. The cost of a missed comment is paid by every future reader; the cost of a redundant one is paid only once.

## What code structurally cannot say

The single sharpest test for whether a comment is justified: ask whether the information it carries can be expressed in code. If yes, fix the code. If no, write the comment. The categories below are the cases where code, by its nature, cannot speak.

### Rationale — *why this and not the other*

Code shows what it does. It cannot show why this approach was chosen and other approaches rejected. Without that record, the next reader has two failure modes (CodeOpinion's "two phases of legacy code"): they assume your decision must have been correct and is unsafe to change, *or* they assume you were wrong and "fix" it — only to rediscover the original constraint at runtime, in production.

Jef Raskin's example, often quoted:

```ts
// A binary search turned out to be slower than the Boyer-Moore algorithm
// for the data sets of interest, so we use the more complex but faster
// method even though this problem does not at first seem amenable to
// a string-search technique.
```

Without that comment, anyone seeing Boyer-Moore where binary search would "obviously" work will swap it back, and re-discover the slowdown weeks later in production.

Write the rationale comment whenever:

- You chose between real alternatives and the chosen one isn't obviously best.
- A simpler-looking implementation was tried and rejected.
- The "natural" approach has a non-obvious flaw the comment can save the next reader from rediscovering.

### Invariants and contracts

Type systems express *what* but rarely *what's required and what's promised*. Document:

- **Preconditions** — what must be true before this is called.
- **Postconditions** — what is true after it returns.
- **Invariants** — what stays true throughout.
- **Ownership** — who is responsible for cleanup, closing, freeing.
- **Side effects** — what state outside this function changes.
- **Concurrency** — thread-safety guarantees, locking discipline, blocking behavior.

```ts
/**
 * Acquires an exclusive lease on the resource.
 *
 * Caller owns the returned Lease and MUST call `release()` exactly
 * once. Holding the lease past `expiresAt` is a programmer error and
 * will throw on the next operation.
 *
 * Thread-safe. Blocking; may wait up to `timeoutMs` if another
 * lease is currently held.
 */
async function acquireLease(resource: ResourceId, timeoutMs: number): Promise<Lease> { ... }
```

This information is invisible from the signature and impossible to recover from the body without reading the whole call graph.

### Units, ranges, and shapes the type system can't express

```ts
// `delay` is in milliseconds, NOT seconds — careful when porting from the
// shell script that uses seconds.
function backoff(delay: number) { ... }

// Values are in USD cents. Never store as floats.
type Money = number & { readonly __brand: "USDCents" };

// Sorted ascending by `timestamp`. Code below relies on this; do not
// re-sort or insert without preserving order.
const events: ReadonlyArray<Event>;
```

The first example is the kind of thing branded types should encode (`type Milliseconds = number & {...}`). When you can encode it in the type, do that instead. When you can't (a list whose ordering matters, an integer with a domain-specific range, an object whose validity depends on context), comment it.

### "Why this is here at all"

Some code exists for reasons unrelated to its mechanics — a workaround for a third-party bug, a regulatory requirement, a compatibility shim, an order-dependence imposed by a library. The next reader will see "this looks unnecessary" and remove it.

```ts
// Workaround for upstream bug PostgreSQL #17421 — without an explicit
// ORDER BY, pg_dump occasionally emits rows in inconsistent order across
// runs, breaking our golden-file test. Remove once the fix lands in 16.x.
const ordered = rows.sort((a, b) => a.id - b.id);

// PCI-DSS 3.2.1 §3.4 — must be hashed at rest, never logged.
const hashed = await bcrypt.hash(card.number, 12);

// Must run BEFORE the auth middleware, because auth populates `req.user`
// from the same cookie this clears.
app.use(clearStaleSessionCookies);
```

This is the strongest case for Chesterton's Fence prevention: the code looks deletable but isn't. The comment is the fence's reason.

### Surprising or non-obvious behavior

Boswell & Foucher: "Anticipate which parts of your code will make readers say 'Huh?'" Document those.

```ts
// Returns the entries in INSERTION order, not key order. We rely on
// Map's ordering guarantee here; do not switch to a plain object.
function recentEvents(): ReadonlyArray<Event> { ... }

// NOTE: This connects to an external service and may take up to 1 second.
// Do not call from a hot HTTP handler.
async function sendNotification(user: User): Promise<void> { ... }
```

A reader who would otherwise have been surprised was just rescued. That's a comment doing real work.

### TODOs and known flaws — with owner and date

```ts
// TODO(terion, 2026-04): swap to streaming once the upload service supports
// chunked transfer. See ticket BAAS-1247.
const buffered = await loadEntireFile(path);

// HACK: lowercases the host because some legacy clients send "Example.com".
// Remove when 100% of clients are on >=v3 (target Q3 2026).
const host = req.headers.host.toLowerCase();
```

Every TODO without a name and date will outlive everyone who knew what it was for. Make them traceable. The same goes for `XXX`, `FIXME`, `HACK` — pick one convention per codebase and enforce it.

## Big-picture comments — the kind agents skip most often

Boswell & Foucher: "Use 'big picture' comments at the file/class level to explain how all the pieces fit together. Summarize blocks of code with comments so the reader doesn't get lost in the details."

This is the comment category most often missing from agent-generated code, and the most expensive when it's missing. Code reads bottom-up; humans read top-down. They want to know *what is this file, what is it for, where does it sit in the system* before they read any function. A 30-word file header often saves more reader time than the next thirty function-level comments combined.

### Module-level header

Every non-trivial file should start with a short header that answers:

- **What is this?** One sentence.
- **What does it do?** Its responsibilities.
- **Where does it sit?** Who calls it; what it calls.
- **Anything cross-cutting?** Concurrency posture, error policy, performance characteristics if relevant.

```ts
/**
 * orders/checkout.ts
 *
 * Orchestrates the checkout flow: validates the cart, reserves inventory,
 * charges the customer, writes the order. Exposed via `placeOrder`.
 *
 * Called from: orders.api.ts (HTTP), orders.consumer.ts (queue).
 * Calls: payments/, inventory/, notifications/.
 *
 * On any failure after reservation, releases inventory before propagating
 * the error. Charges are NEVER created without a successful reservation;
 * see `placeOrder` for the ordering rationale.
 */
```

Three minutes to write; saves every future reader fifteen.

### Class / type / large-function header

Same purpose at smaller scope. A non-trivial class deserves a header explaining its lifecycle, what owns it, and what invariants it maintains. A non-trivial function deserves a contract: inputs, outputs, side effects, error modes.

```ts
/**
 * Maintains a token-bucket rate limit per key.
 *
 * Buckets are evicted lazily — there is no background task. Memory
 * grows with the number of distinct keys seen until eviction kicks in
 * at `maxKeys`. For high-cardinality keyspaces, configure `maxKeys`
 * carefully or use the Redis-backed variant.
 *
 * Not thread-safe. Use a separate instance per worker, or wrap in a mutex.
 */
class RateLimiter { ... }
```

### Section / block summaries inside long functions

When a function is long because the work is genuinely sequential (a request handler, a build pipeline, a setup routine), summary comments at the top of each conceptual block are a navigation aid. They let a reader skim the function's structure before reading the details.

```ts
async function placeOrder(cmd: PlaceOrder): Promise<Order> {
  // 1. Validate and refine the input
  const order = OrderInput.parse(cmd);

  // 2. Reserve inventory atomically — releases on any later failure
  const reservation = await inventory.reserve(order.items);

  try {
    // 3. Charge the customer; this is the point of no return
    const charge = await payments.charge(order.customer, order.total);

    // 4. Persist the order; if this fails after charging we'll need
    //    a manual reconciliation, see runbook RB-007
    return await db.insertOrder({ ...order, chargeId: charge.id });
  } catch (e) {
    await inventory.release(reservation);
    throw e;
  }
}
```

Each comment is a chapter heading. A reader looking for "where do we charge the customer" finds it in seconds.

## What NOT to comment

Hunt & Thomas: "comments should discuss why something is done, its purpose and its goal. The code already shows how it is done." That's the line.

### Don't restate the code

```ts
// BAD
i++;                     // increment i
if (user.isActive) {…}   // check if user is active
const sum = a + b;       // add a and b
return user.email;       // return the email
```

These add nothing and cost reader attention. Worse, they drift out of sync with the code; once one of them is wrong, no one trusts any of them.

### Don't compensate for bad names

If the comment exists to explain what `tmp2` or `processData` does, the comment is wrong — the *name* is wrong. Rename until the comment is redundant, then delete the comment. Boswell & Foucher call these "crutch comments."

```ts
// BAD
const x = u.f();        // get the user's friends count
// GOOD
const friendsCount = user.countFriends();
```

### Don't leave commented-out code

Git remembers. The file should not. If you might want it back, leave a commit reference: `// experimented with binary search here; see commit a3f4e1b`. Otherwise delete.

### Don't write comments that lie

Stale comments are worse than none. A comment that contradicts the code makes the reader trust neither. McConnell: "if a programmer comes in and looks at the comment and sees code that doesn't match, there is a chance that the programmer will modify the code to match the comment — and now the code is wrong."

When you change code, find and update its comments in the same commit. Treat them as part of the code's diff.

### Don't write comments to look thorough

A comment that adds nothing is noise, even if it follows JSDoc/docstring conventions:

```ts
// BAD — looks professional, says nothing
/**
 * Get user.
 * @param id The id.
 * @returns The user.
 */
function getUser(id: UserId): User { ... }
```

Either the comment carries information the signature doesn't, or it should be deleted. Auto-generated docstring scaffolds need to be filled in or removed. (Linters can be configured to enforce this.)

## Where comments belong

Several conventions are well-established and worth following.

### Above, not beside

Comments belong on the line(s) before the code they describe, not trailing it (with rare exceptions for very short clarifications). McConnell: "Use comments to prepare the reader for what is to follow." Trailing comments fight the reader's eye and run out of horizontal space.

```ts
// GOOD
// Skip drafts; they don't have totals yet.
const totals = orders.filter(o => o.status !== "draft").map(orderTotal);

// OK for short, single-line clarification
const ratio = matched / total;  // 0..1
```

### In the code, not the commit log

Ousterhout, *A Philosophy of Software Design*: "Comments belong in the code, not the commit log." A reader six months from now is reading the file, not running `git blame` on every line that puzzles them. If the rationale matters to anyone reading the code, it goes in the code. The commit message can summarize the change; the file holds the persistent context.

This is the inverse of the also-common claim that "the commit explains everything." Commits are great for the *change*; they are not great for the *current state* of the code, because the current state is the sum of many commits and most readers will never reconstruct that history.

### Architecture decisions: ADRs, with pointers from code

For decisions that span multiple files or affect the architecture — choice of database, message broker, auth model, error-handling strategy — write an Architecture Decision Record (ADR) in `docs/adr/`. ADRs are short markdown files that capture **context, decision, alternatives considered, and consequences** (Michael Nygard's original format, refined by Martin Fowler and AWS prescriptive guidance).

In code, point to the ADR rather than restating it:

```ts
// We do not retry charges automatically — see ADR-0014 for the
// idempotency-token rationale.
return payments.chargeOnce(order, idempotencyKey);
```

This is the right place for sustained reasoning. The code comment is a one-line pointer; the ADR carries the argument.

ADR template (Nygard, abbreviated):

```markdown
# ADR-0014: Manual retry for failed charges

## Status
Accepted, 2026-03-12.

## Context
Payment gateway occasionally times out without confirming whether the charge
landed. Automatic retry creates a duplicate-charge risk our risk team has
explicitly forbidden.

## Decision
Charges are issued exactly once per request. On timeout, we surface a
"verify_status" UI to the operator. We do NOT retry automatically.

## Alternatives considered
- Idempotency keys with auto-retry. Rejected: the gateway's idempotency
  window (24h) doesn't cover our SLA for resolution.
- Side-channel reconciliation job. Rejected: introduces a 30-min worst-case
  user-visible delay.

## Consequences
- Operations on-call must handle a small volume of "verify_status" cases.
- Code paths in `payments/` MUST NOT contain retry logic for charge.
```

Keep ADRs short, immutable (write a new one to supersede), numbered, and in the repo. They are the project's institutional memory in a form that survives staff turnover.

### High-level over low-level (for maintenance)

Ousterhout: "higher-level comments are easier to maintain." A comment that says "process the request" stays correct across many changes to the implementation; a comment that says "increment the retry counter and check against MAX_RETRIES" is invalidated by any change to the loop. Prefer the level above the code, not at the code.

## Write comments first, sometimes

Ousterhout's "write the comments first" is a design technique. Before implementing a function, draft its docstring: what it does, what it requires, what it returns. If you can't write that crisply, the design isn't ready. Hunt & Thomas reach the same conclusion from the other side: "Sometimes it is uncomfortable to document the design of source code because the design isn't clear in your mind; it's still evolving." That discomfort is signal — it means it's time to think, not type.

This pairs naturally with type signatures: the type signature is half of the contract; the docstring is the other half. Together they say: here's what this is, here's how to call it, here's what you'll get back, here's what could go wrong, and here's why the design is this way.

## Style and tooling

### Use the language's documentation conventions

- **TypeScript / JavaScript:** JSDoc/TSDoc above declarations. Most editors render them on hover. Use `@param` only when the parameter needs more than its name implies; rely on types for the rest.
- **Python:** Docstrings (PEP 257). Triple double quotes. One-line summary, blank line, body. Pick a style — Google, NumPy, or reStructuredText — and stick with it across the codebase. Don't restate types annotated via PEP 484.
- **C#:** XML doc comments (`///`). Show up in IntelliSense.
- **Go:** A doc comment is a sentence-style comment immediately preceding a top-level declaration, starting with the declared name. Read by `go doc`.

Match the codebase's existing convention. Consistency beats correctness-in-isolation.

### Tooling that helps

- **Doc generators** — TypeDoc, Sphinx, DocFX, godoc — turn structured comments into reference docs. Worth setting up once for any non-trivial library.
- **Linters** — flag missing docstrings on public APIs, undated TODOs, JSDoc with empty bodies. ESLint's `valid-jsdoc`, ruff's `D` rules, StyleCop's documentation rules.
- **Markdown ADRs in `docs/adr/`** with a numbered filename pattern (`0001-use-postgresql.md`). Tools like `adr-tools` automate creation.

## Quick checklist

Before you finish a piece of code, scan for:

- [ ] Does the file have a header explaining what it is and where it sits?
- [ ] Does each public type/function have a contract comment (or rich type) describing inputs, outputs, side effects, error modes?
- [ ] Is every non-obvious choice explained? ("Why Boyer-Moore?")
- [ ] Are units, ranges, ownership, thread-safety stated where the type can't?
- [ ] Are workarounds, regulatory constraints, ordering dependencies marked?
- [ ] Are surprising behaviors flagged?
- [ ] Are TODOs dated and owned?
- [ ] No commented-out code? No comments restating the code? No comments papering over bad names?
- [ ] For architecture-level decisions, is there an ADR linked from the code?

## A summary disposition

Write comments that explain **why**, **what's required**, **what's promised**, and **what's surprising**. Skip comments that explain **what** when the code already does. When in doubt, lean toward writing the comment — the cost of a missing one is paid by every future reader, while the cost of a redundant one is paid only once.
