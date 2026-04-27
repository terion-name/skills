# Worked examples (TypeScript)

Each example shows a **bad version**, a **diagnosis**, and a **better version**. All in TypeScript with strict mode; the principles translate directly to Python, C#, and Go.

---

## 1. Shallow → deep module

### Before (shallow)

```ts
// user-repository.ts
export class UserRepository {
  getById(id: string) {
    return db.query("select * from users where id = ?", [id]);
  }
}

// user-service.ts
export class UserService {
  constructor(private repo: UserRepository) {}
  getUser(id: string) { return this.repo.getById(id); }
}

// user-controller.ts
export class UserController {
  constructor(private svc: UserService) {}
  handle(req: Request) { return this.svc.getUser(req.params.id); }
}
```

**Diagnosis.** Three classes, three files, three indirections. Each layer exposes exactly one method that forwards to the next. Interface-to-implementation ratio ≈ 1 at every level — three shallow modules. No secrets hidden. Pass-through everything. Every change to the query shape touches all three.

### After (deep)

```ts
// users.ts — one file, one concept, one public function
export async function getUser(id: UserId): Promise<User | null> {
  const row = await db.query<UserRow>(
    "select id, name, email, created_at from users where id = $1",
    [id],
  );
  return row ? toDomain(row) : null;
}

function toDomain(r: UserRow): User { /* …mapping… */ }
```

One function, clearly named. The database is hidden inside. If a second caller needs a different query shape, add a second function (`getUserByEmail`) with its own name. The layered version offered no seam we actually needed; we reclaimed simplicity at no behavioral cost.

**When the shallow version is right:** if your team actually swaps database implementations, or actually runs UserRepository under several unrelated `UserService` variants, then the interfaces pay back. That is rarely the case.

---

## 2. Wrong abstraction → duplication → right abstraction

### Before (wrong)

```ts
function send(user: User, opts: {
  channel: "email" | "sms" | "push";
  template: string;
  compact?: boolean;
  includeUnsubscribe?: boolean;
  scheduled?: Date;
}) {
  if (opts.channel === "email") {
    const body = renderEmail(opts.template, user, opts.compact);
    if (opts.includeUnsubscribe) appendUnsubscribe(body);
    return scheduleOr(sendEmail, user.email, body, opts.scheduled);
  } else if (opts.channel === "sms") {
    const body = renderSms(opts.template, user);
    return scheduleOr(sendSms, user.phone, body, opts.scheduled);
  } else {
    return pushClient.send(user.deviceToken, opts.template);
  }
}
```

**Diagnosis.** Three unrelated protocols fused by a flag parameter (`channel`). Parameters mean different things per branch: `compact` and `includeUnsubscribe` only matter for email. A caller can write `send(user, { channel: "sms", includeUnsubscribe: true })` — meaningless — and the compiler cannot help. Over time each branch has grown its own flags, each useless to the other branches. This is the Wrong Abstraction with flag-parameter decay (Metz).

### Interim (duplication)

Go back first. Inline `send` into each call site, keeping only that caller's fields:

```ts
// place 1
const body = renderEmail(tpl, user, true);
appendUnsubscribe(body);
await sendEmail(user.email, body);

// place 2
const body = renderSms(tpl, user);
await sendSms(user.phone, body);

// place 3
await pushClient.send(user.deviceToken, tpl);
```

Read the three side by side. They are not the same concept. They barely overlap. There is nothing useful to DRY.

### After (honest — three functions)

```ts
export async function sendEmail(
  to: Email,
  template: EmailTemplate,
  opts?: { compact?: boolean; unsubscribe?: boolean; scheduled?: Date },
) { /* … */ }

export async function sendSms(
  to: Phone,
  template: SmsTemplate,
  opts?: { scheduled?: Date },
) { /* … */ }

export async function sendPush(
  to: DeviceToken,
  template: PushTemplate,
) { /* … */ }
```

If later a notification orchestrator needs to send across channels, *that* orchestrator holds the dispatch logic, usually with a discriminated union over the message type. The three functions stay honest.

---

## 3. Clever → clear

### Before

```ts
const result = users.filter(u => u.orders.some(o => o.items.every(i =>
  i.tags.includes("promo") && i.price > 0))).map(u => u.id);
```

**Diagnosis.** Five nested predicates. The reader must trace four collection levels and two conjunctions in a single expression. Debugging requires rewriting the expression to inspect intermediates.

### After

```ts
function hasAllPromoItems(order: Order): boolean {
  return order.items.every(i => i.tags.includes("promo") && i.price > 0);
}
function hasQualifyingOrder(user: User): boolean {
  return user.orders.some(hasAllPromoItems);
}
const qualifyingUserIds = users.filter(hasQualifyingOrder).map(u => u.id);
```

Same behavior. Each level named. A reader asking "what counts as qualifying?" jumps to one place. Debuggable with ordinary breakpoints. Testable at each level.

---

## 4. Parse, don't validate

### Before

```ts
function createOrder(input: any) {
  if (!input.userId || typeof input.userId !== "string") throw new Error("bad userId");
  if (!Array.isArray(input.items) || input.items.length === 0) throw new Error("no items");
  for (const it of input.items) {
    if (typeof it.sku !== "string") throw new Error("bad sku");
    if (typeof it.qty !== "number" || it.qty < 1) throw new Error("bad qty");
  }
  return db.insertOrder(input.userId, input.items);
}
```

**Diagnosis.** `any` everywhere. Validation and use interleaved (shotgun parsing). Downstream code must re-check the same properties defensively. Error messages ad hoc; no single source of truth for the shape.

### After

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
  const input = OrderInput.parse(raw);               // boundary — once
  return db.insertOrder(input.userId, input.items);  // typed, trusted
}
```

One parse at the boundary; downstream code is statically guaranteed. New rules go into the schema, not through the call tree. The schema is documentation.

---

## 5. Pyramid of doom → guard clauses

### Before

```ts
function process(req: Request) {
  if (req.user) {
    if (req.user.isActive) {
      if (req.payload) {
        if (req.payload.amount > 0) {
          return charge(req.user, req.payload.amount);
        } else {
          return { error: "amount" };
        }
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
```

### After

```ts
function process(req: Request) {
  if (!req.user)               return { error: "no user" };
  if (!req.user.isActive)      return { error: "inactive" };
  if (!req.payload)            return { error: "payload" };
  if (req.payload.amount <= 0) return { error: "amount" };
  return charge(req.user, req.payload.amount);
}
```

Happy path at the left margin; each precondition fails fast; nesting depth 1. Adding a new precondition is a single line, not a new level.

---

## 6. Branded types prevent a bug class

### Before

```ts
function transfer(from: string, to: string, amount: number) { /* … */ }
transfer(orderId, userId, 100); // compiles. Catastrophic.
```

### After

```ts
type UserId  = string & { readonly __brand: "UserId"  };
type OrderId = string & { readonly __brand: "OrderId" };

function transfer(from: UserId, to: UserId, amount: number) { /* … */ }

transfer(orderId, userId, 100); // ✗ compile error
```

Zero runtime cost. A class of catastrophic bugs (passing the wrong kind of id to `transfer`) becomes impossible.

---

## 7. Discriminated union replaces flag + optional fields

### Before

```ts
type Request = {
  status: string;              // "pending" | "succeeded" | "failed"
  response?: string;
  error?: string;
  retryAfter?: number;
};

if (req.status === "succeeded") console.log(req.response!); // the ! is a red flag
```

### After

```ts
type Request =
  | { status: "pending" }
  | { status: "succeeded"; response: string }
  | { status: "failed"; error: string; retryAfter: number };

if (req.status === "succeeded") console.log(req.response); // no `!`, safe
```

No more non-null assertions. TypeScript exhaustiveness checks force you to handle every state:

```ts
function describe(req: Request): string {
  switch (req.status) {
    case "pending":   return "waiting";
    case "succeeded": return `got ${req.response}`;
    case "failed":    return `error ${req.error}, retry in ${req.retryAfter}`;
    // a new status added to the union gives a compile error here
  }
}
```

---

## 8. Options object vs flag-parameter sprawl

### Before

```ts
function fetchUser(id: string, includeOrders: boolean, includePrefs: boolean, withDeleted: boolean) { /* … */ }
fetchUser("u1", true, false, true);
```

**Diagnosis.** Four positional flags. Call sites are unreadable.

### After

```ts
function fetchUser(id: UserId, opts: { includeOrders?: boolean; includePrefs?: boolean; withDeleted?: boolean } = {}) { /* … */ }
fetchUser(userId, { includeOrders: true, withDeleted: true });
```

Or, if the flags actually correspond to three distinct use cases, **split into three named functions**:

```ts
fetchUser(id);
fetchUserWithOrders(id);
fetchUserIncludingDeleted(id);
```

Prefer split when the call sites each consistently pass the same flag combination — that reveals the flag is not a toggle but a different concept.

---

## 9. Define the error away

### Before

```ts
function removeTag(post: Post, tag: string) {
  const i = post.tags.indexOf(tag);
  if (i < 0) throw new Error("tag not present");
  post.tags.splice(i, 1);
}
```

Callers end up with:

```ts
try { removeTag(post, "promo"); } catch { /* ignore */ }
```

**Diagnosis.** The caller's intent is "ensure 'promo' is not in the tag list." The function models "precisely remove this one element." The mismatch forces every caller to swallow an exception.

### After

```ts
function removeTag(post: Post, tag: string) {
  post.tags = post.tags.filter(t => t !== tag);
}
```

The error disappeared. No caller needs a `try/catch`. The no-op case is the correct behavior.

---

## 10. Colocation beats layered dispersion

### Before (file tree)

```
src/
  controllers/OrderController.ts
  services/OrderService.ts
  repositories/OrderRepository.ts
  mappers/OrderMapper.ts
  dtos/OrderDTO.ts
  validators/OrderValidator.ts
  types/Order.ts
```

A reader who wants to understand how an order is created opens **seven files**.

### After

```
src/
  orders/
    orders.ts          // domain type + core operations
    orders.api.ts      // HTTP route handlers
    orders.db.ts       // persistence
    orders.test.ts     // tests
    orders.schema.ts   // input/output schemas (Zod)
```

Same separation of concerns, but grouped by domain. One folder, predictable filenames, one reader hop to any piece. When orders change, one folder changes.

**When the old structure is right:** in a very large codebase with multiple teams owning horizontal layers (e.g., a DB team, an API team, a domain team), the layered structure may match organizational reality (Conway's Law). For most teams under 50 engineers, domain colocation wins.

---

## 11. Inheritance → composition

### Before

```ts
abstract class Notifier {
  abstract send(user: User, message: string): Promise<void>;
  log(user: User, message: string) { /* shared */ }
}
class EmailNotifier extends Notifier { send(user, message) { /* … */ } }
class SmsNotifier   extends Notifier { send(user, message) { /* … */ } }
class PushNotifier  extends Notifier { send(user, message) { /* … */ } }
```

**Diagnosis.** The three notifiers have almost nothing in common except the name `send`. The shared `log` is one line. The abstract class imposes a hierarchy for a trivial gain, and new notifier types must now participate in that hierarchy.

### After

```ts
type Notify = (user: User, message: string) => Promise<void>;

const sendEmail: Notify = async (user, message) => { /* … */ };
const sendSms:   Notify = async (user, message) => { /* … */ };
const sendPush:  Notify = async (user, message) => { /* … */ };

function logged(notify: Notify): Notify {
  return async (user, message) => {
    await notify(user, message);
    console.log("notified", user.id);
  };
}

const emailLogged = logged(sendEmail);
```

Three plain functions. Logging is a separate, composable concern. No class hierarchy, no `abstract` method to remember to implement.

---

## 12. Options pattern vs default computation

### Before

```ts
function resize(img: Image, width: number, height: number, quality?: number, format?: string) {
  const q = quality ?? 85;
  const f = format ?? "jpeg";
  // ...
}
```

### After (push decisions down)

```ts
function resize(img: Image, dim: { width: number; height: number }) {
  const quality = chooseQualityFor(img, dim);    // hides the policy
  const format = chooseFormatFor(img);
  // ...
}
```

Callers stop needing to know about the defaults. The policy lives in the module where it belongs, with its own tests. If one caller genuinely needs to override, *that* caller gets an overload; the common path stays simple.

---

## Pattern behind every example

Each refactor has the same shape: a piece of complexity the *caller* had to carry (a deeply nested check, a misplaced validation, a hierarchy, a combinatorial flag mess) moves *into* the module that should carry it, or dissolves entirely. The interface shrinks. The reader's working memory gets smaller to hold the code in head. That is what "better" means.
