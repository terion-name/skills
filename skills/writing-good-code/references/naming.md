# Naming

Names are the cheapest, highest-leverage design tool. A good name creates a precise mental picture; a bad name forces the reader to simulate the implementation to recover the concept. **Naming is a design diagnostic**: when a clean name is hard to find, the abstraction is usually wrong — not the vocabulary.

## Core rules

### 1. Name things in the domain, not in the framework

Prefer nouns and verbs from the problem domain.

| Good | Bad |
|---|---|
| `InvoiceLine`, `RetryPolicy`, `AppointmentSlot` | `InvoiceManager`, `RetryHelper`, `AppointmentData` |
| `schedule(appointment)` | `processAppointment(data)` |
| `rejected`, `pending`, `settled` | `status1`, `flag`, `state` |

Framework vocabulary is acceptable at framework boundaries (e.g., `Request`, `Response`, `Middleware`) — not inside business logic.

### 2. Length scales with scope

| Scope | Style | Example |
|---|---|---|
| Loop index (≤ 3 lines) | 1 letter | `i`, `k`, `x` |
| Function local | 1 word | `count`, `offset`, `head` |
| Module-level binding | 2–3 words | `currentUserId`, `activeSessions` |
| Public function | precise multi-word | `resolveCurrentUserFromRequest` |
| Public type | precise noun | `AuthenticatedRequest`, `RefundPolicy` |

A module-level `x` is a crime. A loop-local `resolvedCurrentUserFromRequestIndex` is equally bad.

### 3. Avoid noise suffixes

The following are *diagnostics*, not absolute bans — but each requires justification.

| Suffix | Usually means | Preferred instead |
|---|---|---|
| `*Manager` | "I could not find a concept" | Name what it manages (`SessionPool`) |
| `*Helper` | "Grab bag of unrelated functions" | Co-locate with its concept, or give the concept a name |
| `*Handler` | Fine in event/UI/HTTP contexts | Elsewhere, name the action (`AuthorizePayment`) |
| `*Processor` | Usually too vague | Name what it produces (`InvoiceRenderer`) |
| `*Util` | "Random utilities" | Delete; move each function to its domain |
| `*Wrapper` | Often a thin layer hiding nothing | Use the wrapped type, or name what the wrapper adds |
| `*Info` / `*Data` | Meaningless distinction from the thing itself | Use the thing's name |
| `*Base` / `Abstract*` | Inheritance you probably do not need | Prefer composition; name the concept |
| `*Impl` | .NET/Java habit with no semantic value | Give the concrete class a real name |
| `*Context` | Fine when domain has a "context" | Name the data it carries |

### 4. Avoid Hungarian and type prefixes

- `strName`, `iCount`, `m_foo`, `pNode` — redundant with types or leaking implementation.
- `I` before interfaces — only retain where the language community uses it (C#/.NET). Avoid in TypeScript, Python, Go, Rust.

### 5. Searchable names

- `MAX_RETRIES = 3` over a bare `3`.
- `event` instead of `e` at non-trivial scope.
- Single-letter names are OK at tight scope only.

### 6. Pronounceable names

If a pair programmer could not say it out loud, rename. `genymdhms` → `generatedTimestamp`.

### 7. Consistent vocabulary across the codebase

Pick one of `fetch`, `get`, `load`, `retrieve` for an operation and use it consistently. Mixing costs the reader a slot per switch:

- `get*` — in-memory retrieval, no side effects, cheap.
- `fetch*` — network or IPC, may fail.
- `load*` — disk or DB, potentially expensive.
- `resolve*` — derive from context (e.g., current user).

Same for `create` / `make` / `new` / `build`, or `delete` / `remove` / `destroy`. Pick one pair per semantic, document it, stick with it.

### 8. Distinguish meaningful differences

`Product`, `ProductInfo`, `ProductData`, `ProductDetail`, `ProductRecord` — the reader has no way to tell which is which. Pick one. If there are genuinely multiple concepts, name them by their distinction, not by a noise suffix:

- `Product` — the domain entity
- `ProductRow` — a database row
- `ProductDTO` — a wire format
- `ProductSummary` — a projection

Each of those names earns its keep.

### 9. Boolean names read as predicates

`isReady`, `hasChildren`, `canEdit`, `shouldRetry`. Not `ready` (ambiguous noun/adjective), not `flag` (confession of laziness).

### 10. Functions named for intent, not mechanics

- `sortByDateDesc(users)` over `sort(users, dateComparatorDesc)`.
- `authorizePayment(order)` over `checkAndProcessAndLog(order)`.
- If a function's name contains "and," it is two functions.

## Naming as a diagnostic: the test

When naming feels hard, *do not* force a name. Feel the resistance as information. Two possibilities:

1. **The concept is not yet real.** You are naming a random slice of logic. Stop. Keep the code inline; maybe the concept will surface after the third caller.
2. **Two concepts are fused.** You keep reaching for "and" or "or" in the name. Split into two functions.

Rule: if you reach for `Helper`, `Manager`, `Util`, or "and/or" in a name, inline the code and try again later.

## When "Manager / Helper / Handler" is OK

Keep a short mental allow-list:

- **Framework conventions the community uses**: `EventHandler` (UI), `HttpHandler` (server), `AuthenticationManager` (Spring).
- **Domain terms your users actually say**: an HR system may legitimately have `BenefitsManager` if HR calls it that.
- **Everything else**: keep trying until the concept reveals itself, or leave the code inline.

## Good → Better → Bad

| Bad | Better | Good |
|---|---|---|
| `process(data)` | `parseOrder(raw)` | `parseOrder(raw: string): Order` |
| `DataHelper` | `OrderSerializer` | `OrderCodec` (if "codec" is the term the team uses) |
| `doStuff()` | `migrateLegacyUsers()` | `migrateLegacyUsersToMultiTenant()` |
| `tmp`, `data`, `info` | `pendingInvoices` | `pendingInvoicesForCurrentTenant` |
| `IUserService` + `UserService` (one impl) | `UserService` only | `UserService`; introduce `Users` interface when a second impl exists |
| `handle(e)` | `onOrderPlaced(event)` | `notifyWarehouseOfOrder(order)` |
| `utils.ts` with 40 exports | `orderFormatting.ts`, `currency.ts` | move each function next to its caller/domain module |

## File and module names

- A file's name should predict what a reader will find in it. `billing/invoices.ts` tells you both the domain and the concept.
- Avoid `index.ts` / `__init__.py` as the only home of logic; they are for re-exports. Logic deserves a specific file.
- Folder names express the domain (`patients/`, `billing/`), not the layer (`models/`, `services/`).
- Test files sit next to source: `invoices.ts` + `invoices.test.ts`.

## One more time

**If naming is hard, the problem is probably in the abstraction, not the vocabulary.**
