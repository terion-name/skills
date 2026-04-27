# Worked refactors (TypeScript)

Each refactor is shown as a **commit sequence**, not just before/after. The point is to internalize the discipline: tiny, reversible steps; each step keeps tests green; structure and behavior never mix.

---

## Refactor 1 — Layered shallow monolith → colocated deep module

### Starting state

```
src/
  controllers/UserController.ts   // forwards HTTP to UserService
  services/UserService.ts          // forwards to UserRepository
  repositories/UserRepository.ts   // forwards to db
  mappers/UserMapper.ts            // db row → domain
  dtos/UserDTO.ts                  // wire → domain
```

Five files, four layers, every layer is pass-through. Reader hops four files to follow a single request.

### Goal

Collapse to a single colocated module. Preserve all behavior.

### Commit sequence

**Commit 1 — Add tests at HTTP boundary.** Before any structural change, write a characterization test that hits the route and asserts on the response. Run; commit.

**Commit 2 — Inline `UserMapper` into `UserRepository`.** It is one function called from one place. Inline; tests still pass.

**Commit 3 — Inline `UserDTO` mapping into `UserController`.** Same justification.

**Commit 4 — Inline `UserRepository` into `UserService`.** No real seam was being hidden; the abstraction had no second implementation and no test boundary.

**Commit 5 — Inline `UserService` into `UserController`.** Same reasoning. Now the controller contains the full request flow.

**Commit 6 — Move and rename: `controllers/UserController.ts` → `users/users.api.ts`.** Folder reorganization.

**Commit 7 — Split `users.api.ts` into `users.ts` (domain types + queries) and `users.api.ts` (HTTP).** Now the split matches a real boundary: HTTP vs domain.

### Final state

```
src/users/
  users.ts        // domain type + getUser, listUsers, etc.
  users.api.ts    // route handlers
  users.test.ts   // colocated
```

Two files, one folder, zero pass-throughs. Each module hides a real concern.

### Reader benefit

Following a request now means opening one file. The HTTP layer does HTTP; the domain layer does domain. The previous structure pretended to do this, but each layer hid nothing.

---

## Refactor 2 — Wrong abstraction (flag parameters) → duplication → right abstraction

### Starting state

```ts
// notifications.ts — grew over 18 months
function send(user: User, opts: {
  channel: "email" | "sms" | "push";
  template: string;
  compact?: boolean;
  includeUnsubscribe?: boolean;
  scheduled?: Date;
  legacyMode?: boolean;
  audit?: boolean;
}) {
  if (opts.audit) auditLog.write({ user: user.id, channel: opts.channel });
  if (opts.channel === "email") {
    let body = renderEmail(opts.template, user, opts.compact);
    if (opts.legacyMode) body = wrapForLegacyClient(body);
    if (opts.includeUnsubscribe) appendUnsubscribe(body);
    return scheduleOr(sendEmail, user.email, body, opts.scheduled);
  } else if (opts.channel === "sms") {
    if (opts.compact) throw new Error("compact not supported for sms");  // dead branch?
    const body = renderSms(opts.template, user);
    return scheduleOr(sendSms, user.phone, body, opts.scheduled);
  } else {
    if (opts.includeUnsubscribe || opts.compact) {
      throw new Error("unsupported");                                     // dead branch?
    }
    return pushClient.send(user.deviceToken, opts.template);
  }
}
```

Seven flags, three channels, several branches that may be dead. Caller code looks like `send(user, { channel: "sms", includeUnsubscribe: true })` — meaningless combinations compile.

### Goal

Replace with three honest functions. Re-derive any genuine sharing only after reading callers.

### Commit sequence

**Commit 1 — Characterize.** Find every call site (~15 of them). Write a test per call site asserting current behavior. Run; commit.

**Commit 2 — Inline `send` at each call site, one site per commit.** Use IDE inline. Each commit reduces by one caller; tests remain green.

```ts
// Was: send(u, { channel: "email", template: "welcome", includeUnsubscribe: true })
// Becomes:
const body = renderEmail("welcome", u, undefined);
appendUnsubscribe(body);
await sendEmail(u.email, body);
```

After 15 commits, `send` is unused; delete it.

**Commit 3 — Read the inlined call sites side by side.** They fall into three groups:

- ~8 sites that send email with various combinations of `compact` / `unsubscribe` flags.
- ~5 sites that send SMS with at most a `scheduled` date.
- ~2 sites that send push, with no flags ever set.

The "compact for SMS" and "unsubscribe for push" branches were unreachable. Audit was always set together with email — and only with email. Several branches were dead code preserved by fear.

**Commit 4 — Extract `sendEmailNotification`, `sendSmsNotification`, `sendPushNotification`** as three functions, each with the parameters its callers actually pass.

```ts
export function sendEmailNotification(
  to: Email,
  template: EmailTemplate,
  opts?: { compact?: boolean; unsubscribe?: boolean; scheduled?: Date; audit?: boolean },
) { /* … */ }

export function sendSmsNotification(
  to: Phone,
  template: SmsTemplate,
  opts?: { scheduled?: Date },
) { /* … */ }

export function sendPushNotification(
  to: DeviceToken,
  template: PushTemplate,
) { /* … */ }
```

**Commit 5 — Replace inlined call sites with the new functions, one site per commit.**

**Commit 6 — Delete dead-branch handling that originally existed for invalid combinations.** Now invalid combinations are compile errors.

### Result

Three honest functions. No flag parameter sprawl. Compiler prevents nonsense calls. The ~15 call sites read clearly. **The fastest way forward was back.**

---

## Refactor 3 — Pyramid of doom → guard clauses

### Before

```ts
function processWebhook(req: Request) {
  if (req.headers["content-type"] === "application/json") {
    if (req.body && typeof req.body === "object") {
      if ("event" in req.body) {
        if (req.body.event === "order.placed") {
          if (req.body.order && req.body.order.id) {
            handleOrderPlaced(req.body.order);
            return { ok: true };
          } else {
            return { error: "missing order" };
          }
        } else {
          return { error: "unknown event" };
        }
      } else {
        return { error: "no event field" };
      }
    } else {
      return { error: "invalid body" };
    }
  } else {
    return { error: "invalid content type" };
  }
}
```

### Commit sequence

**Commit 1 — Add tests** for each error path and the happy path. Snapshot the responses.

**Commit 2 — Invert the outermost condition (Guard Clauses tidying).**

```ts
function processWebhook(req: Request) {
  if (req.headers["content-type"] !== "application/json") {
    return { error: "invalid content type" };
  }
  // …rest, with one less indent
}
```

**Commit 3 — Repeat for each subsequent condition.** One commit per inversion.

**Commit 4 — Final state:**

```ts
function processWebhook(req: Request) {
  if (req.headers["content-type"] !== "application/json") return { error: "invalid content type" };
  if (!req.body || typeof req.body !== "object")          return { error: "invalid body" };
  if (!("event" in req.body))                             return { error: "no event field" };
  if (req.body.event !== "order.placed")                  return { error: "unknown event" };
  if (!req.body.order?.id)                                return { error: "missing order" };

  handleOrderPlaced(req.body.order);
  return { ok: true };
}
```

**Commit 5 (separate, behavior-affecting commit) — Replace the manual guards with a Zod parse at the boundary.** Now a single commit changes behavior (richer error messages, exhaustive validation).

```ts
const Webhook = z.object({
  event: z.literal("order.placed"),
  order: z.object({ id: z.string() }).passthrough(),
});

function processWebhook(req: Request) {
  if (req.headers["content-type"] !== "application/json") return { error: "invalid content type" };
  const parsed = Webhook.safeParse(req.body);
  if (!parsed.success) return { error: parsed.error.message };
  handleOrderPlaced(parsed.data.order);
  return { ok: true };
}
```

The structural cleanup (commits 2-4) shipped first, separately from the behavior change (commit 5).

---

## Refactor 4 — Validate-scattered → parse-once

### Before

```ts
function createOrder(input: any) {
  if (!input.userId) throw new Error("missing userId");
  if (typeof input.userId !== "string") throw new Error("bad userId");
  if (!Array.isArray(input.items)) throw new Error("missing items");
  if (input.items.length === 0) throw new Error("no items");

  const totalCents = computeTotal(input.items);
  if (totalCents <= 0) throw new Error("invalid total");                 // re-validates items

  return db.insertOrder({
    userId: input.userId,
    items: input.items.map((it: any) => ({
      sku: String(it.sku),                                                // re-coerces
      qty: Math.max(1, Math.floor(Number(it.qty))),                       // re-checks qty
    })),
    totalCents,
  });
}

function computeTotal(items: any[]) {
  let total = 0;
  for (const it of items) {
    if (typeof it.sku !== "string") throw new Error("bad item");           // re-validates
    if (typeof it.qty !== "number" || it.qty < 1) throw new Error("bad qty");
    total += it.qty * priceFor(it.sku);
  }
  return total;
}
```

Validation is sprinkled across two functions; coercion appears in the middle of work. `any` everywhere.

### Commit sequence

**Commit 1 — Tests.** Every error path; the happy path; one tricky edge case (e.g. `qty: 1.7` — what does the current code do?).

**Commit 2 — Introduce schema, parse at boundary.**

```ts
const OrderInput = z.object({
  userId: z.string().uuid(),
  items: z.array(z.object({
    sku: z.string().min(1),
    qty: z.number().int().min(1),
  })).nonempty(),
});
type OrderInput = z.infer<typeof OrderInput>;

function createOrder(raw: unknown) {
  const input = OrderInput.parse(raw);
  // existing body still does its old checks
}
```

Tests still pass; the parse is a strict superset of the current ad-hoc checks.

**Commit 3 — Remove the now-redundant runtime checks.**

```ts
function createOrder(raw: unknown) {
  const input = OrderInput.parse(raw);
  const totalCents = computeTotal(input.items);
  return db.insertOrder({ userId: input.userId, items: input.items, totalCents });
}

function computeTotal(items: OrderInput["items"]): number {
  return items.reduce((sum, it) => sum + it.qty * priceFor(it.sku), 0);
}
```

`computeTotal` no longer validates — `items` is typed.

**Commit 4 (behavior change, separate) — Improve error message format.** Now that errors come from a schema, replace the bare string with a structured response. Tests for error paths update; commit by itself.

---

## Refactor 5 — Util grab bag → domain modules

### Before

```
src/
  utils.ts        // 800 lines — date formatting, currency, string helpers,
                  // database connection helpers, encryption, retry logic, http,
                  // permission checks, …
```

A reader who imports from `utils` cannot guess what is there.

### Commit sequence

**Commit 1 — Categorize.** Open `utils.ts`, group functions by concept. List the categories that emerge:

- date formatting (5 functions)
- currency / money (4)
- encryption / hashing (3)
- retry / backoff (2)
- http helpers (4)
- permission checks (6)
- string casing (3)
- DB helpers (5)
- one-offs that don't fit (≈10)

**Commit 2 — Move date functions to `dates.ts`.** Update imports across the codebase (IDE-driven). Tests pass. Commit.

**Commit 3 — `currency.ts`.** Same pattern.

**Commit 4 — `encryption.ts`.** Same.

…and so on. One category per commit, each commit is a pure move + import update.

**Commit 12 — The leftovers.** Look at the remaining ≈10 one-off functions. For each:

- Is it called from one place? Inline it; delete from utils.
- Is it called from the domain it conceptually belongs to? Move it next to its caller.
- Is it actually generic but with no good home? Create a specific module (e.g. `text.ts`, `paging.ts`).

Delete `utils.ts` at the end. **A `utils.ts` is a confession; killing it is therapy.**

---

## Refactor 6 — Characterization test before untangling legacy `calculateTax`

### Before

```ts
// 200 lines, no tests, called from 30+ places, mixed concerns
export function calculateTax(input: any): number {
  // db lookups, hardcoded rates, regional rules, currency conversion,
  // logging, audit writes
}
```

You need to add a new tax rule for a new region.

### Commit sequence

**Commit 1 — Capture 20 representative orders from production logs.** Save as fixtures.

**Commit 2 — Write a characterization test:**

```ts
test("calculateTax — characterization (current behavior, bugs included)", () => {
  for (const sample of samples) {
    expect(calculateTax(sample.input)).toBe(sample.expectedTax);
  }
});
```

Run; some assertions fail because the function has bugs. **Update the expected values to match current output**, with comments noting the bugs:

```ts
// TODO bug #1234: US-CA charged same rate as US (should be higher)
{ input: { region: "US-CA", amount: 1000 }, expectedTax: 100 },
```

Commit. Now you have a safety net.

**Commit 3 — Sprout the new region's logic** as a separate function with its own unit tests. Call it from a single location in `calculateTax`. Run characterization tests; they pass; commit.

**Commit 4+ — Refactor `calculateTax` itself**, one extraction at a time:

- Extract regional rules into `taxRulesByRegion: Map<Region, RuleFn>`.
- Push the database lookup out to a parameter (object seam: `calculateTax(input, rateProvider)`).
- Separate logging from calculation.
- Replace `any` with a parsed `TaxInput` type.

Each extraction commits separately. Characterization tests stay green.

**Commit N — Replace characterization tests with focused unit tests** on each extracted piece. Retire the integration-level test once unit coverage exists. The bug-preserving asserts can now be split: keep the test; mark it `xtest` (skip); fix the underlying bug in a separate behavior-changing commit; un-skip.

### Result

A codebase where adding a new tax rule means writing one new function and one test, not editing a 200-line monolith. Each refactor was tiny, reversible, and demonstrably behavior-preserving.

---

## The pattern across all six refactors

1. **Tests first** — characterize current behavior at whatever level admits a test.
2. **Tiny commits** — each one a single mechanical change, green between each.
3. **Structure and behavior never mix in one commit.**
4. **Delete with confidence only after evidence** — characterization tests give you the evidence.
5. **Going back is fast** — when you find duplication that turned out to be coincidence, inlining is cheap; re-deriving is honest.

Refactoring is not a one-shot redesign. It is a discipline of small steps — and the small steps are what make it safe to do at all.
