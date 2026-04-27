# Readability

Readability is not decoration. It is the cost-of-entry for every future change. Code that cannot be understood in a single sitting cannot be safely modified, which means it is already broken. This reference gives concrete, observable properties you can apply.

## Line-of-sight

The **happy path should run straight down the left margin.** Preconditions fail fast and return; the main flow sits at the baseline indent.

```ts
// Before: happy path is buried
function process(req: Request) {
  if (req.user) {
    if (req.user.isActive) {
      if (req.payload) {
        return charge(req.user, req.payload.amount);
      } else {
        return { error: "payload" };
      }
    } else {
      return { error: "inactive" };
    }
  } else {
    return { error: "no user" };
  }
}

// After: happy path at margin
function process(req: Request) {
  if (!req.user)            return { error: "no user" };
  if (!req.user.isActive)   return { error: "inactive" };
  if (!req.payload)         return { error: "payload" };
  return charge(req.user, req.payload.amount);
}
```

The reader scans four preconditions in four lines, then reaches the real work. The original forced a mental stack of four "if" contexts.

## Single Level of Abstraction per function (SLAP)

A function should operate at one conceptual level. If a function calls `sendInvoiceEmail(order)` *and* writes raw bytes to a socket, the granularity jumps mid-read and the reader loses the thread.

```ts
// Bad — mixed levels
function placeOrder(order: Order) {
  validateOrder(order);
  const conn = net.connect({ host: "payments", port: 443 });
  conn.write(`POST /charge HTTP/1.1\r\n...`);
  // ...dozens of lines of HTTP wire protocol...
  notifyWarehouse(order);
}

// Good — one level
function placeOrder(order: Order) {
  validateOrder(order);
  chargeCustomer(order);       // hides HTTP wire protocol
  notifyWarehouse(order);
}
```

## Locality of behavior

Code that you need to read together should *live* together. Carson Gross: *"The behaviour of a unit of code should be as obvious as possible by looking only at that unit of code."*

Fight the instinct to split a feature across five layers when one file would do. A React component that contains its click handler and its styles has higher locality than one that dispatches to three other files. The trade-off is real — locality vs DRY — and locality usually wins for glue code, while DRY wins for true business rules.

**Test:** to understand what this unit does, how many files must the reader open? Target 0–1; 2 acceptable; 3+ is a bad smell.

## Guard clauses and early returns

Prefer:

```ts
if (!isValid(input)) return defaultValue;
if (cache.has(input)) return cache.get(input)!;
// …main path
```

Over:

```ts
if (isValid(input)) {
  if (!cache.has(input)) {
    // …main path
  } else {
    return cache.get(input)!;
  }
} else {
  return defaultValue;
}
```

Each guard removes one dimension of the reader's mental state.

## Name intermediate booleans and results

When an expression spans more than three terms, name the pieces:

```ts
// Before
if (user && user.active && !user.banned && (user.role === "admin" || user.overrides.includes("edit")))

// After
const isActive = user && user.active && !user.banned;
const canEdit = user?.role === "admin" || user?.overrides.includes("edit");
if (isActive && canEdit)
```

The second form compiles to the same code and adds no runtime overhead; it does add working-memory slots of names — which is the point.

## Predictable control flow

- `get_*` does not write. `is_*` returns bool, does not throw. `create_*` creates.
- Functions do what their name promises, and only that. No side-effects hidden under a pure-looking name.
- Iteration does not mutate its input.
- Methods do not reach through multiple objects (`a.b.c.d.e()`). See Law of Demeter + `references/errors-and-boundaries.md`.

## Consistency beats local optimality

When editing an existing codebase, match its dominant conventions — naming, error style, file layout, import order, comment style — unless you have a specific reason to deviate. Each deviation costs the next reader a working-memory slot.

If you think the convention is wrong, that is a separate conversation (and a separate commit). Do not silently introduce a second convention.

## Least astonishment

- A function named `save` that sometimes does not save is astonishing. Either rename it or make it always save.
- An iteration operator that mutates its input is astonishing.
- An operator overload that allocates is astonishing.
- Default arguments that differ from the name's implication (a `timeout = -1` default that means "no timeout") are astonishing. Use a sentinel with a real name, or a separate no-timeout variant.

When in doubt, follow the language's and framework's strongest conventions — not your personal preference.

## Comments: for why, not what

Good comments answer questions the code cannot:

- **Why this order?** "Release the lock before logging to avoid holding it across I/O."
- **What invariant?** "Assumption: list is sorted ascending by timestamp."
- **What contract?** "Caller owns the returned handle and must close it."
- **What non-obvious fact?** "This runs at startup before the DI container is ready, so it uses the raw config."

Bad comments restate the code:

```ts
// Bad
// increment i by 1
i++;

// Bad
// check if user is active
if (user.isActive) { … }
```

If a comment would just restate the code, the *name* is wrong. Rename until the comment is redundant, then delete the comment.

**Ousterhout's "write the comment first"** is a design tool: try to write a one-line contract for the function before implementing it. If you cannot, the design is not ready. The comment you would have written becomes the function's docstring.

## Hidden information that must be surfaced

Some things must be in comments or types because the code alone cannot say them:

- Units (`seconds` vs `milliseconds`, `USD cents` vs `USD dollars`). Prefer encoding in the type: `type Cents = number & { __brand: "Cents" }`.
- Ranges and nullability not visible from types.
- Performance guarantees (O(n) expected, O(n²) worst case).
- Thread-safety guarantees.
- Ownership and lifetime.

Surface these in types when possible; comment them when not.

## Visual density

A wall of dense code fatigues. Small paragraph-like groupings with a blank line between each conceptual phase help the reader chunk:

```ts
function settleInvoice(invoice: Invoice) {
  // 1. Validate state
  if (invoice.state !== "issued") throw new InvalidState();

  // 2. Apply payment
  const payment = charge(invoice.customer, invoice.amount);

  // 3. Update records
  invoice.state = "settled";
  invoice.paidAt = now();
  return payment;
}
```

The numbered comments are optional; the blank lines alone chunk the mental model. Both count as readability tools when used sparingly.

## What not to do

- Do not put multiple statements on one line.
- Do not use one-letter names for anything that outlives 5 lines.
- Do not use abbreviations that are not standard in your domain (`usr`, `cnt`, `idx` — unless the codebase already does).
- Do not leave commented-out code. Git remembers; the file should not.
- Do not leave `TODO`s without a name and a date; undated TODOs become permanent.
- Do not write `// here be dragons`; say what the dragon is.

## A final filter

Before marking code done, try this: picture yourself reading it six months from now, under time pressure, trying to fix a production bug. Would your future self thank past you? If not, change it now; your future self cannot.
