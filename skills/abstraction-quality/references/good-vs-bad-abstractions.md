# Good vs bad abstractions — paired TypeScript examples

Each example shows a **bad abstraction** and a **good abstraction** for the same problem. Diagnosis explains *why* the bad version fails and what makes the good version pay its keep.

---

## 1. Deep vs shallow module

### Bad — shallow

```ts
// arrayUtils.ts
export function isEmpty<T>(xs: T[]): boolean { return xs.length === 0; }
export function isNonEmpty<T>(xs: T[]): boolean { return xs.length > 0; }
export function first<T>(xs: T[]): T | undefined { return xs[0]; }
export function last<T>(xs: T[]): T | undefined { return xs[xs.length - 1]; }
export function head<T>(xs: T[]): T | undefined { return xs[0]; }      // duplicate
export function tail<T>(xs: T[]): T[] { return xs.slice(1); }
```

**Why bad:** every function is a shallow wrapper around a one-line stdlib expression. Interface surface ≈ implementation. The module hides nothing — readers must learn six new names plus their semantic differences (`first` vs `head`?). The wrapper makes code *less* readable, not more.

### Good — deep

```ts
// rateLimiter.ts
export interface RateLimiter {
  allow(key: string): boolean;
}

export function createRateLimiter(opts: { limit: number; windowMs: number }): RateLimiter {
  const buckets = new Map<string, { count: number; resetAt: number }>();
  return {
    allow(key) {
      const now = Date.now();
      const b = buckets.get(key);
      if (!b || b.resetAt <= now) {
        buckets.set(key, { count: 1, resetAt: now + opts.windowMs });
        return true;
      }
      if (b.count >= opts.limit) return false;
      b.count++;
      return true;
    },
  };
}
```

**Why good:** a single small interface (`{ allow(key): boolean }`) hides bucket allocation, time tracking, expiry, and reset logic. A caller never thinks about windows or buckets. The implementation could be replaced with Redis-backed or token-bucket variants without touching callers — a real seam.

---

## 2. Honest boundary vs leaky abstraction

### Bad — leaky

```ts
class HttpClient {
  async get(url: string): Promise<unknown> {
    try {
      const res = await fetch(url);
      return await res.json();
    } catch (e) {
      return null;        // any failure becomes null
    }
  }
}
```

**Why bad:** the abstraction promises "give me a URL, get back JSON or null." It silently hides:

- Network failure vs 404 vs 500 vs malformed JSON — all collapse to `null`.
- Timeout? Same `null`.
- Partial response? `null`.

Callers cannot distinguish "no resource" from "your code is broken." The abstraction is leaky because every meaningful failure mode bleeds through eventually — the caller will need to know which kind of `null` they got, but cannot.

### Good — honest

```ts
type FetchResult<T> =
  | { ok: true; data: T }
  | { ok: false; kind: "not_found" }
  | { ok: false; kind: "network_error"; cause: unknown }
  | { ok: false; kind: "parse_error"; cause: unknown }
  | { ok: false; kind: "server_error"; status: number };

async function fetchJson<T>(url: string, parse: (raw: unknown) => T): Promise<FetchResult<T>> {
  let res: Response;
  try {
    res = await fetch(url);
  } catch (cause) {
    return { ok: false, kind: "network_error", cause };
  }
  if (res.status === 404) return { ok: false, kind: "not_found" };
  if (res.status >= 500)  return { ok: false, kind: "server_error", status: res.status };
  let raw: unknown;
  try {
    raw = await res.json();
  } catch (cause) {
    return { ok: false, kind: "parse_error", cause };
  }
  return { ok: true, data: parse(raw) };
}
```

**Why good:** every failure mode is an explicit case. Caller pattern-matches and decides. The `parse` callback enforces parse-don't-validate at the boundary. The abstraction does not promise more than it can deliver.

---

## 3. Right interface vs `any` / `Function`

### Bad — too broad

```ts
function pipe(value: any, ...fns: Function[]): any {
  return fns.reduce((acc, fn) => fn(acc), value);
}
```

**Why bad:** `any` and `Function` provide no compile-time help. Any sequence of arguments compiles. A typo (calling a function with wrong arity, or chaining incompatible types) shows up at runtime.

### Good — typed and honest

```ts
function pipe<A, B>(a: A, f1: (a: A) => B): B;
function pipe<A, B, C>(a: A, f1: (a: A) => B, f2: (b: B) => C): C;
function pipe<A, B, C, D>(a: A, f1: (a: A) => B, f2: (b: B) => C, f3: (c: C) => D): D;
function pipe(a: unknown, ...fns: Array<(x: unknown) => unknown>): unknown {
  return fns.reduce((acc, fn) => fn(acc), a);
}
```

**Why good:** call sites get type checking; the implementation falls back to `unknown` (not `any`). Common arities are typed; rarer ones use the fallback. The interface is honest about what it can and cannot type.

---

## 4. Parameterization vs pre-generalization

### Bad — generalized for needs that don't exist

```ts
class FormValidator<T> {
  constructor(
    private rules: Map<keyof T, Array<(value: any, ctx: T) => string | null>>,
    private errorFormatter?: (errors: Map<keyof T, string[]>) => unknown,
    private locale?: string,
    private severity?: "warn" | "error" | "info",
  ) {}
  // …200 lines that handle a dozen imagined cases…
}
```

Used in exactly one place to validate a sign-up form.

**Why bad:** every constructor parameter solves a problem nobody has. The class is impossible to read because every reader must hold "what does `severity` do?" in working memory. When a real new requirement arrives, it almost certainly does not fit the imagined shape.

### Good — concrete

```ts
type SignUpInput = { email: string; password: string; age: number };
type SignUpErrors = Partial<Record<keyof SignUpInput, string>>;

function validateSignUp(input: SignUpInput): SignUpErrors {
  const errors: SignUpErrors = {};
  if (!isEmail(input.email))     errors.email = "invalid email";
  if (input.password.length < 8) errors.password = "password too short";
  if (input.age < 13)            errors.age = "must be 13+";
  return errors;
}
```

**Why good:** does exactly what the one user needs. Reads in one screen. When the second form arrives, write a second function. After the third, look for shared concepts — and only if they truly share concepts.

---

## 5. State machine as discriminated union vs boolean flags

### Bad — booleans

```ts
type Job = {
  id: string;
  isStarted?: boolean;
  isCompleted?: boolean;
  isFailed?: boolean;
  result?: string;
  error?: string;
  startedAt?: Date;
  completedAt?: Date;
};

if (job.isCompleted && job.result) { use(job.result); }     // the && is the bug
```

**Why bad:** illegal states are representable. A `Job` with `isStarted=false` and `isCompleted=true` compiles. Every consumer must defensively check combinations. The `result` field's existence is implicit.

### Good — discriminated union

```ts
type Job =
  | { id: string; status: "pending" }
  | { id: string; status: "running"; startedAt: Date }
  | { id: string; status: "succeeded"; startedAt: Date; completedAt: Date; result: string }
  | { id: string; status: "failed"; startedAt: Date; failedAt: Date; error: string };

if (job.status === "succeeded") { use(job.result); }   // safe; no &&; result is required
```

**Why good:** illegal states are not representable. `result` exists exactly when `status === "succeeded"`. TypeScript's exhaustiveness checking ensures every case is handled. Readers see the entire state machine in the type.

---

## 6. Single-impl interface deleted vs kept (with rationale)

### Case A — delete

```ts
// Before
interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: OrderId): Promise<Order | null>;
}
class SqlOrderRepository implements OrderRepository { /* … */ }

// After
class OrderRepository { /* … */ }   // interface inlined; one class
```

**Why delete:** there is one implementation, and tests use a real database (test container). The interface added typing surface and a layer to navigate, with no payback.

### Case B — keep

```ts
interface PaymentGateway {
  charge(amount: Cents, source: PaymentSource): Promise<Charge>;
  refund(chargeId: string, amount: Cents): Promise<Refund>;
}
class StripeGateway implements PaymentGateway { /* … */ }
class FakePaymentGateway implements PaymentGateway { /* used in unit tests */ }
```

**Why keep:** there is a real second implementation (the test fake), and unit tests need a fast, deterministic in-memory substitute. The interface is the seam that makes tests fast. Even with one production implementation, the interface earns its keep.

**The rule:** an interface needs either (a) two real implementations, or (b) a concrete test seam that simpler mechanisms would not satisfy. Otherwise: delete.

---

## 7. Branded type vs unbranded

### Bad — strings everywhere

```ts
function transfer(from: string, to: string, amount: number) { /* … */ }

const orderId = "ord_123";
const userId = "usr_456";
transfer(orderId, userId, 100);   // compiles. Catastrophic.
```

**Why bad:** the type system sees three strings and a number; the *meaning* of each string is invisible. A whole class of catastrophic bugs is unguarded.

### Good — branded

```ts
type UserId  = string & { readonly __brand: "UserId" };
type OrderId = string & { readonly __brand: "OrderId" };

function transfer(from: UserId, to: UserId, amount: Cents) { /* … */ }

transfer(orderId, userId, 100);   // ✗ compile error
```

**Why good:** zero runtime cost. The compiler distinguishes user IDs from order IDs by intent, not just shape. The bug class is eliminated by construction.

---

## 8. Locality of behavior — React component example

### Bad — scattered

```tsx
// components/SubmitButton.tsx
import { onSubmitClick } from "../handlers/submitHandler";
import { submitButtonStyles } from "../styles/submitStyles";

export const SubmitButton = ({ formId }: { formId: string }) => (
  <button className={submitButtonStyles} onClick={() => onSubmitClick(formId)}>Submit</button>
);

// handlers/submitHandler.ts
import { dispatch } from "../store";
import { logEvent } from "../analytics";

export function onSubmitClick(formId: string) {
  dispatch({ type: "FORM_SUBMIT", formId });
  logEvent("submit_click", { formId });
}

// styles/submitStyles.ts
export const submitButtonStyles = "...";
```

To understand what the button does, the reader opens **three files**. Renaming or removing the button requires touching all three.

### Good — colocated

```tsx
// components/SubmitButton.tsx
import { dispatch } from "../store";
import { logEvent } from "../analytics";

const styles = "px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700";

export function SubmitButton({ formId }: { formId: string }) {
  function handleClick() {
    dispatch({ type: "FORM_SUBMIT", formId });
    logEvent("submit_click", { formId });
  }
  return <button className={styles} onClick={handleClick}>Submit</button>;
}
```

**Why good:** behavior, structure, and styling all visible in one place. Renaming or deleting the component requires touching one file. Carson Gross's Locality of Behavior principle.

**Caveat:** if `onSubmitClick` were used by other components, then a shared module is appropriate (real DRY). But for one-use glue code, locality wins.

---

## 9. Tell, don't ask vs query-then-modify

### Bad — query then modify externally

```ts
const account = repository.find(accountId);
if (account.balance >= amount) {
  account.balance -= amount;
  account.transactions.push({ type: "withdraw", amount, at: now() });
  repository.save(account);
} else {
  throw new InsufficientFundsError();
}
```

**Why bad:** the caller pulls the account's internals out, manipulates them, pushes them back. Every caller doing a withdraw must remember the same five-step dance. Invariants (balance never negative, transaction always recorded) are enforced by convention, not construction.

### Good — tell

```ts
class Account {
  // … fields …
  withdraw(amount: Cents): void {
    if (this.balance < amount) throw new InsufficientFundsError();
    this.balance -= amount;
    this.transactions.push({ type: "withdraw", amount, at: now() });
  }
}

// caller
const account = repository.find(accountId);
account.withdraw(amount);
repository.save(account);
```

**Why good:** the operation is a single intent (`withdraw`); the invariants are enforced by the object that owns the state. No caller can accidentally update balance without recording a transaction.

**Caveat:** this is appropriate when behavior and state are genuinely coupled. If `Account` is a DTO crossing a wire boundary, attaching methods is wrong — keep it data, do operations in a dedicated function. The choice is whether the data has *behavior* coupled to it (use methods) or is *transported* (keep it data).

---

## 10. Single function vs Strategy pattern with one strategy

### Bad — pattern for the sake of pattern

```ts
interface PricingStrategy {
  computePrice(item: Item): Cents;
}

class StandardPricingStrategy implements PricingStrategy {
  computePrice(item: Item): Cents { return item.basePrice; }
}

class PricingService {
  constructor(private strategy: PricingStrategy) {}
  computePrice(item: Item): Cents { return this.strategy.computePrice(item); }
}

const service = new PricingService(new StandardPricingStrategy());
```

**Why bad:** there is one strategy. The interface, the class, and the service exist for nothing. Any future second strategy will probably not fit this shape anyway — its real shape is unknown.

### Good — a function

```ts
function computePrice(item: Item): Cents {
  return item.basePrice;
}
```

**When to introduce the Strategy pattern:** when a *real* second strategy exists (loyalty pricing, regional pricing) AND the strategy must be selected at runtime per call. Even then, often a `switch` or a `Map<PricingMode, (item: Item) => Cents>` is enough — the full pattern is heavyweight for most cases.

---

## The pattern across all ten

A good abstraction:

- **Hides more than it exposes** (depth).
- **Has a name from the problem domain** (no `Manager`/`Helper`/`Wrapper`).
- **Is honest about what leaks** (errors, timing, ownership all explicit).
- **Removes possible-but-illegal states** rather than checking for them at runtime.
- **Pays for the interface tax with substantial implementation hidden behind it.**

A bad abstraction:

- Wraps a one-liner.
- Has a generic name and a generic type signature (`<T>` / `any` / `Function`).
- Promises more than it delivers.
- Adds parameters faster than callers add use cases.
- Could be inlined with no loss.

When evaluating any abstraction in code review, hold both lists in mind. If the abstraction passes the good list, it earns its keep. If it matches any of the bad list, propose the inline / split / rename.
