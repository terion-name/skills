# TypeScript idioms

Idiomatic, production-grade TypeScript for the 2020s. Principles over rules; pragmatism over purity.

## tsconfig: start strict

```jsonc
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "skipLibCheck": true
  }
}
```

`noUncheckedIndexedAccess` is the single biggest bug-prevention flag after `strict`. It forces you to handle the case where `arr[i]` is `undefined`. Leave it on.

`exactOptionalPropertyTypes` distinguishes "key missing" from "key set to undefined" — matters for JSON round-trips.

## `any` vs `unknown`

- `any` disables type-checking locally and everywhere the value flows. **Do not use it.**
- `unknown` is the type-safe "I don't know yet." Anything flowing in must be narrowed before use. This is the right type for "raw input from outside."

```ts
// Wrong
function parse(input: any) { return input.foo.bar; }

// Right
function parse(input: unknown) {
  if (typeof input !== "object" || input === null) throw new TypeError();
  // …narrow further or use a schema library
}
```

Set `@typescript-eslint/no-explicit-any` to error.

## Annotate boundaries, infer internals

```ts
// Public function — annotate everything
export function resolveUser(id: UserId): Promise<User | null> { /* … */ }

// Internal helper — let inference do the work
const normalized = users.map(u => ({ ...u, email: u.email.toLowerCase() }));
```

Over-annotating hurts readability; under-annotating at boundaries lets bad types leak across module edges. Public API = explicit; internals = inferred.

## Discriminated unions + exhaustiveness

Model states as unions with a literal tag, and use the `never` trick for exhaustiveness:

```ts
type Request =
  | { status: "pending" }
  | { status: "succeeded"; response: string }
  | { status: "failed"; error: string };

function describe(r: Request): string {
  switch (r.status) {
    case "pending":   return "waiting";
    case "succeeded": return r.response;
    case "failed":    return `error: ${r.error}`;
    default: {
      const _exhaustive: never = r;   // compile error if a case is missed
      return _exhaustive;
    }
  }
}
```

Adding a new variant anywhere in the codebase produces a compile error at every switch, pointing out exactly where to update.

## Branded types

```ts
type UserId  = string & { readonly __brand: "UserId" };
type OrderId = string & { readonly __brand: "OrderId" };

function asUserId(s: string): UserId { /* validate */ return s as UserId; }
```

Zero runtime cost, compile-time separation. Prevents the "passed an order id where a user id was expected" bug class.

## `as const` and `satisfies`

```ts
// `as const` — preserve literal types
const LEVELS = ["debug", "info", "warn", "error"] as const;
type Level = (typeof LEVELS)[number]; // "debug" | "info" | "warn" | "error"

// `satisfies` — check conformance without widening
const config = {
  host: "localhost",
  port: 5432,
  ssl: true,
} satisfies Config;

// config.host retains type "localhost" — useful for downstream inference
```

Prefer `satisfies` over type annotation when you want to both check conformance *and* keep narrow literal types.

## `type` vs `interface`

- **Default to `type`.** It is more flexible — supports unions, intersections, mapped types.
- Use `interface` when you specifically need declaration merging (library authors extending global types) or when defining class-like object shapes in OOP-heavy code.
- Never mix: do not define the same name as both `type` and `interface` in a codebase.

## `readonly` by default

```ts
function sum(xs: readonly number[]): number { /* … */ }
type Config = { readonly port: number; readonly host: string };
```

Makes mutation at the boundary a compile error. `readonly` signals intent; combined with functional helpers it prevents entire bug classes (shared-state mutation, aliased arguments changed under your feet).

## Avoid `enum`

TypeScript's `enum` has quirks (unexpected runtime code, reverse mappings for numeric enums, inconsistent with JS). Prefer a union of string literals:

```ts
// Instead of
enum Role { Admin = "admin", User = "user" }

// Use
const ROLE = ["admin", "user"] as const;
type Role = (typeof ROLE)[number];
```

Exception: `const enum` is fine for pure numeric flags where you want the constants inlined — but even there, string unions usually win on clarity.

## Avoid `namespace`

A relic from pre-module TypeScript. Use ES modules (`import`/`export`). `namespace` blocks should only appear when augmenting an external library's types.

## Narrowing taxonomy

```ts
// Typeof
if (typeof x === "string") { /* x: string */ }

// Instanceof
if (e instanceof Error) { /* e: Error */ }

// `in` operator
if ("length" in x) { /* x has length */ }

// Discriminated union
if (r.status === "failed") { /* r is the failure variant */ }

// User-defined type guard
function isUser(x: unknown): x is User { /* … */ }

// Assertion function
function assertIsUser(x: unknown): asserts x is User { /* … */ }
```

Assertion functions are especially useful at parse boundaries.

## Parse, don't validate — with Zod

```ts
import { z } from "zod";

const User = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  role: z.enum(["admin", "user"]),
});
type User = z.infer<typeof User>;

export function loadUser(raw: unknown): User {
  return User.parse(raw);
}
```

Schema is the single source of truth. Downstream code receives a refined type; no re-validation.

## Result types vs exceptions

For expected failures where callers must decide:

```ts
type Result<T, E> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function findUser(id: UserId): Promise<Result<User, "not_found" | "db_down">> { /* … */ }
```

For programmer errors, preconditions, and unrecoverable failures: throw. Let them propagate to a boundary that maps to HTTP/log output.

Libraries like `neverthrow` encode this pattern with chainable combinators; a hand-rolled discriminated union is also fine and has zero dependency cost.

## Classes — sparingly

TypeScript does not require OOP. Default to functions and plain objects; use classes when:

- You have genuine state *behaviour* coupling (methods that operate on internal state, invariants maintained between calls).
- A framework requires classes (Angular components, some testing libraries).
- You need identity-based equality.

A "class" with no internal state is just a namespace of functions — convert it.

Do not create an `IFoo` for every `Foo`. Introduce an interface when a second implementation exists.

## Module organization

- **One concept per file.** File named after the concept.
- **Co-locate tests.** `orders.ts` + `orders.test.ts`.
- **Avoid deep barrel files.** `index.ts` files that re-export dozens of symbols cause:
  - Circular imports (hard to debug).
  - Slow builds (tree-shaking fights with barrels).
  - Loss of locality (readers can no longer find where a symbol lives).
  Prefer importing from the specific file: `import { createOrder } from "./orders/orders"` over `import { createOrder } from "./orders"`.
- **Folder = domain.** `orders/`, `billing/`, `patients/`. Not `services/`, `controllers/`.

## Async/await

- Prefer `async/await` over `.then` chains.
- Always `await` or explicitly return promises; dangling promises are a bug.
- Use `Promise.all` for concurrent independent work; do not serialize by default.
- Use `AbortSignal` for cancellation.
- `for await (const x of stream)` for async iterables.

```ts
// Bad — serial
const user   = await findUser(id);
const orders = await findOrdersForUser(id);

// Good — concurrent
const [user, orders] = await Promise.all([findUser(id), findOrdersForUser(id)]);
```

## Utility types: useful in moderation

`Pick`, `Omit`, `Partial`, `Required`, `ReturnType`, `Parameters`, `Awaited`, `NonNullable`, `Record` are worth knowing. `Exclude`, `Extract`, `InstanceType` for edge cases.

Do not build a 10-layer conditional type when a plain interface would do. If a type needs a comment to explain what it produces, consider whether the underlying design is clear.

## Avoid

- `!` non-null assertion in production code. Each use is a bet you can lose. Narrow or refactor.
- `as` casts without `unknown` bridge. `x as Foo` is unsafe; `x as unknown as Foo` is at least visible.
- `Function`, `Object`, `{}` as types — too broad. Use `(...args: never[]) => unknown`, `Record<string, unknown>`, `object`.
- `any[]` / `any{}`.
- Over-generic signatures. If you cannot name what the generic parameter represents, it is probably the wrong abstraction.
- Overload-first design. TypeScript's function overloads are for interop with JS patterns (e.g., `addEventListener` with many event names). For new code, use union types or separate functions.
- Side effects at module top level.
- `require()` / CommonJS in new code.

## Tooling (2024-2026)

- **Type checker:** `tsc --noEmit` in CI.
- **Linter:** `typescript-eslint` (flat config) or **Biome** (fast all-in-one). Biome is catching up fast; eslint remains the most configurable.
- **Formatter:** Prettier or Biome.
- **Runner:** `tsx` for scripts; `tsc --build` for monorepos; `vitest` for tests.
- **Bundler:** only when shipping to the browser. For Node services, `tsx` or `tsc` is enough.

Recommended `typescript-eslint` rules to raise from warn to error:

- `no-explicit-any`
- `no-floating-promises`
- `no-misused-promises`
- `no-non-null-assertion`
- `consistent-type-imports`
- `switch-exhaustiveness-check`
- `no-unnecessary-condition`

## Quick idiom cheatsheet

- `const` everywhere until mutation is proven necessary, then `let`.
- Arrow functions for callbacks and short helpers; named `function` declarations for exported top-level functions (cleaner stack traces, supports hoisting).
- Early return over nested `if`/`else`.
- `??` (nullish coalescing) over `||` for defaults when `0` / `""` / `false` are valid values.
- `?.` (optional chaining) to replace manual null-guards.
- Template literals over `+` for string building.
- `Map` and `Set` over `{}` and `[]` when the semantic is a map or set.
- `structuredClone` over `JSON.parse(JSON.stringify(x))` for deep copies.
- `Array.from({ length: n }, (_, i) => …)` over empty-array-push loops.
