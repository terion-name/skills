# Tidyings — Kent Beck's small, reversible improvements

From *Tidy First?* (2023). A tidying is a tiny refactoring — reversible in minutes, leaves tests green, and usually fits in a handful of lines. They compose; a sequence of tidyings can transform messy code without ever leaving it broken.

## The discipline

- **Structure and behavior in separate commits.** Never mix tidying with a feature change. A reviewer reading a tidy commit should not have to ask "did this change what the code does?"
- **Tidy after, sometimes before, rarely never.** The default is "tidy after" — land the change, then tidy. "Tidy first" when the change is hard without preparation. "Tidy later" when you find a mess unrelated to the current work. "Never" when the code will be deleted soon.
- **If in doubt, don't.** A tidying that takes more than a few minutes is actually a refactoring — budget it separately.

## The fifteen tidyings

### 1. Guard Clauses

Invert the body's outermost condition and return early.

```ts
// Before
function score(p: Player) {
  if (p.active) {
    // 40 lines of logic
  } else {
    return 0;
  }
}

// After
function score(p: Player) {
  if (!p.active) return 0;
  // 40 lines, un-indented
}
```

**When:** deep nesting whose outermost condition handles a trivial or error case.

### 2. Dead Code

Remove it.

**When:** unreachable branches, unused variables, commented-out blocks, orphan imports.

### 3. Normalize Symmetries

Make code that does the same thing look the same, and code that does different things look different.

```ts
// Before — inconsistent
if (!user) return null;
if (user.banned === true) return null;
if (user.role !== "admin") return null;

// After — symmetric
if (!user)               return null;
if (user.banned)         return null;
if (user.role !== "admin") return null;
```

**When:** you notice identical operations in several places written in slightly different ways. Make them match so real differences stand out.

### 4. New Interface, Old Implementation

Add a new function with the desired signature; have it call the old one.

```ts
// Old function has a clumsy signature you don't want to keep
function processOrder(order: Order, includeTax: boolean, audit: boolean) { … }

// New interface, calling the old implementation
function placeOrder(order: Order)                  { return processOrder(order, true, true); }
function placeOrderNoAudit(order: Order)           { return processOrder(order, true, false); }
```

**When:** you want to migrate callers to a cleaner API without changing behavior yet. Later, migrate callers one at a time, and finally delete the old function.

### 5. Reading Order

Rearrange declarations and functions in the order a reader will want them, top to bottom. Public API first; private helpers after.

**When:** a file reads in an arbitrary order and you keep scrolling to follow the logic.

### 6. Cohesion Order

Group related declarations together. Fields that are set together; methods that operate on the same state; constants that belong to the same subsystem.

**When:** declarations are scattered. Move them adjacent without changing any behavior.

### 7. Move Declaration and Initialization Together

```ts
// Before
let total;
doStuff();
computeOther();
total = calculateTotal();   // used later

// After
doStuff();
computeOther();
const total = calculateTotal();
```

**When:** a variable is declared far from its first use, making the reader hold "what is this for?" in working memory across unrelated code.

### 8. Explaining Variable

```ts
// Before
if (user.orders.length > 0 && user.orders[user.orders.length - 1].status === "paid") { … }

// After
const lastOrder = user.orders[user.orders.length - 1];
const hasPaidLastOrder = lastOrder && lastOrder.status === "paid";
if (hasPaidLastOrder) { … }
```

**When:** a sub-expression is non-trivial or used twice.

### 9. Explaining Constant

```ts
// Before
if (retries > 5) abort();

// After
const MAX_RETRIES = 5;
if (retries > MAX_RETRIES) abort();
```

**When:** a literal appears in a conditional without a name.

### 10. Explicit Parameters

Replace reading from a wide object (or global) with explicit parameters in the function signature.

```ts
// Before
function computeFee() {
  return config.base * config.multiplier * config.currency.factor;
}

// After
function computeFee(base: number, multiplier: number, currencyFactor: number) {
  return base * multiplier * currencyFactor;
}
```

**When:** a function's dependencies on its environment are invisible from its signature.

### 11. Chunk Statements

Separate related groups of lines with blank lines to visually chunk them.

```ts
function settle(invoice: Invoice) {
  validateState(invoice);
  assertNotPaid(invoice);

  const payment = charge(invoice);
  recordPayment(invoice, payment);

  notifyAccountant(invoice);
  return payment;
}
```

Three paragraphs: validation, charge, notification. Zero behavior change.

**When:** a function reads as a wall of code.

### 12. Extract Helper

Pull a cohesive chunk into its own function.

**When:** after you have chunked (Tidying 11) and named each chunk mentally, one chunk is genuinely reusable or long enough to warrant a name. **Not** before — over-extracting is a larger sin than under-extracting. Pair with Tidying 13.

### 13. One Pile

The counter-tidying to Extract Helper. If a function has been over-extracted — many tiny helpers that no one but this function calls — inline them into one pile and re-read. Often a simpler structure emerges that did not fit the fragmented version.

**When:** you inherit code where every function is 3 lines and each calls two others. Pile it up, then re-extract the *real* concepts.

This is the tidying that directly counters the "extract reflex" that coding agents default to.

### 14. Explaining Comments

Add a short comment when the *why* is non-obvious: a workaround, a performance note, an invariant, a coupling that must be preserved.

**When:** the code cannot express intent alone.

### 15. Delete Redundant Comments

Remove comments that restate the code, or that were true at one point but drifted out of date.

**When:** the code and name already say what the comment says.

## The tidying decision matrix

| Column | Meaning | When |
|---|---|---|
| **Tidy First** | Tidy before the behavior change | When the change is hard without preparation — untangle a function before inserting new logic. |
| **Tidy After** | Ship the change, then tidy | Default. Adding a feature revealed a messy shape; clean it up now that you see it. |
| **Tidy Later** | Log a tidying for later | You noticed a mess unrelated to the current change. Write it down; do not expand scope. |
| **Never** | Leave it | The code will be deleted or rewritten soon; the cost of tidying will not be recovered. |

## Sequencing

A sequence of tidyings typically looks like:

1. Rename (Tidying 1 from `smell-catalog.md` — always rename first).
2. Explaining Constants (9), Explaining Variables (8), Explaining Comments (14).
3. Guard Clauses (1), Reading Order (5), Cohesion Order (6).
4. Move Declaration and Initialization Together (7), Chunk Statements (11).
5. One Pile (13) if the existing extraction is fragmented.
6. Extract Helper (12) where true concepts emerge.
7. Delete Redundant Comments (15), Dead Code (2).

Commit each tidying separately. Tests stay green between each. A pull request full of one-tidying-per-commit is easy to review and easy to revert.

## What tidyings don't do

Tidyings do not change behavior. If you find yourself about to change behavior mid-tidying — stop, revert, split. The discipline of two hats is worth more than the efficiency of combining them.
