# Errors and boundaries

How code fails matters as much as how it succeeds. The principles below reduce the set of possible bugs by construction and make the remaining ones loud.

## Core principles

1. **Errors at boundaries, not everywhere.** The outer edges of your system (HTTP handlers, CLI main, message consumers, DB repositories) convert raw errors into domain errors or user-facing messages. Inner code trusts its types and fails loudly when the types are violated.
2. **Parse, don't validate** (Alexis King). Refine data into a type once at the boundary. After that point, the type guarantees the properties, and inner code does not re-check.
3. **Make illegal states unrepresentable.** Use discriminated unions, branded types, non-empty collections, and mutually-exclusive fields expressed as union variants rather than optional flags.
4. **Define errors out of existence where possible** (Ousterhout). The best error handling is the one you do not need.
5. **Fail loud, fail early.** A crash with a stack trace is better than a silent wrong answer.

## "Parse, don't validate"

### The old pattern (shotgun parsing)

```ts
function createOrder(input: any) {
  if (!input.userId || typeof input.userId !== "string") throw new Error("bad userId");
  if (!Array.isArray(input.items) || input.items.length === 0) throw new Error("no items");
  for (const it of input.items) {
    if (typeof it.sku !== "string") throw new Error("bad sku");
    if (typeof it.qty !== "number" || it.qty < 1) throw new Error("bad qty");
  }
  // ...now operate on input as if trusted, but TypeScript still sees `any`
  return db.insertOrder(input.userId, input.items);
}
```

Problems: `any` everywhere; validation and use interleaved; downstream code re-checks the same properties defensively; error messages ad hoc; no single place to see the schema.

### The replacement

```ts
import { z } from "zod";

const OrderInput = z.object({
  userId: z.string().uuid(),
  items: z.array(z.object({
    sku: z.string().min(1),
    qty: z.number().int().min(1),
  })).nonempty(),
});
type OrderInput = z.infer<typeof OrderInput>;

export async function createOrder(raw: unknown): Promise<Order> {
  const input = OrderInput.parse(raw);   // boundary — once
  return db.insertOrder(input.userId, input.items);  // typed, trusted
}
```

One parse at the boundary; downstream code is guaranteed by types. New validation rules go into the schema, not scattered through the call tree. The schema doubles as documentation.

Language equivalents:

- **Python** — Pydantic, `attrs` + validators, `msgspec`.
- **C#** — `System.Text.Json` + source-generated contracts, FluentValidation at the edge, records for the parsed type.
- **Go** — a hand-written `Parse` function returning `(Order, error)`; use `encoding/json` struct tags for shape, but validate semantics in the parser.

### The rule

External data is `unknown` until parsed. Parse once, trust afterward. Inside the trust boundary, the type is the contract — no `assert`s re-checking fields.

## Make illegal states unrepresentable

### Discriminated unions for state machines

```ts
// Bad — each field optional, combinations unclear
type Request = {
  status: string;
  response?: string;
  error?: string;
  retryAfter?: number;
};

// Good — status determines which other fields exist
type Request =
  | { status: "pending" }
  | { status: "succeeded"; response: string }
  | { status: "failed"; error: string; retryAfter: number };
```

Now a reader knows that `retryAfter` exists only on failures, and a writer cannot forget to set it. TypeScript's exhaustiveness checking makes missing a case a compile error.

### Branded types for domain identity

```ts
type UserId  = string & { readonly __brand: "UserId" };
type OrderId = string & { readonly __brand: "OrderId" };

function transfer(from: UserId, to: UserId, amount: number) { /* ... */ }

// transfer(orderId, userId, 100); // compile error — catastrophic bug prevented at edit time
```

The overhead is zero at runtime (strings remain strings). The gain is that accidentally swapping an order id for a user id becomes a compile error. Same pattern works with Python (`NewType`), C# (record wrappers), Go (defined types).

### Non-empty collections

```ts
type NonEmptyArray<T> = [T, ...T[]];

function first<T>(xs: NonEmptyArray<T>): T { return xs[0]; }  // no null/undefined path
```

If a function requires at least one element, say so in the type; do not check at runtime.

### Mutually-exclusive fields

Prefer a discriminated union to two optional fields that should never both be set.

## Error handling styles

Choose one per code path; do not mix exceptions and result types casually.

### Result / Either type — when the failure is expected and the caller must decide

```ts
type Result<T, E> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function findUser(id: UserId): Promise<Result<User, "not_found" | "db_down">> {
  try {
    const row = await db.query("select ... where id = $1", [id]);
    return row ? { ok: true, value: toDomain(row) } : { ok: false, error: "not_found" };
  } catch (e) {
    return { ok: false, error: "db_down" };
  }
}
```

Good when:

- The failure is a normal part of the domain (not-found, already-exists, version-conflict).
- The caller likely has a meaningful alternative behavior for each error.

### Exceptions — when failure is unrecoverable or a programmer error

```ts
function assertAdmin(user: User): asserts user is AdminUser {
  if (user.role !== "admin") throw new PermissionError(user.id);
}
```

Good when:

- The failure should propagate to an outer boundary that maps and logs.
- The caller cannot reasonably handle the specific failure.
- It represents a precondition violation.

### Go / Rust pattern (errors as values)

```go
user, err := findUser(id)
if err != nil {
    return nil, fmt.Errorf("looking up user %s: %w", id, err)
}
```

The `%w` wrap preserves the causal chain while adding context. A caller can `errors.Is(err, ErrNotFound)` to check for specific failures without string matching.

## Loudness

- **Never silently swallow exceptions.** `try { … } catch (_) { }` is almost always a bug. At minimum, log with context; ideally, re-throw or return a typed result.
- **Never return a sentinel that a caller could confuse with success.** `indexOf` returning `-1` is a historical wart, not a model to emulate. Prefer `null`/`undefined` + narrow types, or a `Result`.
- **Prefer crashing loudly to proceeding with invalid state.** A 500 is a debuggable event; a silent wrong charge is not.

## Define errors out of existence

The goal is to make whole error categories impossible, not to handle them better.

- An `append` to a list that doesn't exist → create the list on first append; the "list doesn't exist" error disappears.
- `remove(x)` from a set that doesn't contain `x` → make it a no-op, not an error. The caller's intent ("ensure x is not in the set") is satisfied.
- `delete(file)` on a non-existent file → if intent is "ensure file is gone," no-op is right. If intent is "consume a file you placed," different function.
- Index out of range → clamp internally, or return empty slice, when that matches the caller's need.

Ousterhout's three patterns:

1. **Define errors away** (above).
2. **Mask errors** — handle them at the lowest level possible (e.g., a retry inside a connection pool; callers never see the transient failure).
3. **Exception aggregation** — a top-level handler converts internal errors into a single user-visible response, so the rest of the code does not repeat error-handling boilerplate.

## Strict at internal boundaries, strict at external boundaries

Postel's "be liberal in what you accept" was written for a specific historical moment (TCP in a world of non-interoperating implementations). Inside a modern system — between your own services — liberal acceptance is a technical-debt factory. It hides bugs, allows schema drift, and creates permanent backward-compatibility obligations (Hyrum's Law).

- **Internal boundaries:** strict. Reject unknown fields. Validate enums. Refuse partial data.
- **External public API consumed by third parties:** strict on format, document the schema precisely, and version explicitly.
- **External integration with a legacy system you cannot change:** here, liberal parsing earns its keep — but log every instance of fallback so you can see what the legacy sender is actually doing.

## Anti-patterns to avoid

- **Validate-then-use scattered.** `assert` statements repeated throughout the call tree re-checking the same invariants. Parse once.
- **Exception as control flow.** Using `try/catch` as an `if`/`else`, or throwing in the hot path. Makes every stack trace a false positive.
- **Catch-all at every layer.** `catch (Exception)` at every function swallows stack traces and prevents the outer handler from doing the right thing.
- **Boolean error returns.** `createOrder(...): boolean` loses information. Return the order or a typed error.
- **String-matched error handling.** `if (err.message.includes("timeout"))` — brittle; use typed errors with a discriminator.
- **HTTP status codes carrying business logic.** Returning `401` for "token expired" and `403` for "role missing" when the spec does not imply that — forces every client to learn your interpretation. Use a self-describing error body.

## Quick checklist

- [ ] Does external data pass through exactly one parse at the boundary?
- [ ] Do illegal states show up as compile errors, not runtime asserts?
- [ ] Are branded types used for domain identities that must not be mixed up?
- [ ] Are discriminated unions used for mutually-exclusive states?
- [ ] Does the function use exceptions only for unrecoverable or programmer errors?
- [ ] Are typed results used for expected failures the caller must handle?
- [ ] Is there no silent `catch` anywhere in the new code?
- [ ] Have you tried to define away any error, rather than handle it?
