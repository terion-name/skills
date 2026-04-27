# C# idioms

Modern C# (.NET 8+). Target the language as it is in the mid-2020s, not as it was in 2012. Resist the "Enterprise Java" patterns that accreted in the 2000s.

## Enable nullable reference types everywhere

```xml
<PropertyGroup>
  <Nullable>enable</Nullable>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  <WarningsAsErrors>nullable</WarningsAsErrors>
</PropertyGroup>
```

Nullable annotations are the single most valuable language feature added in the last decade. Every type is either `Foo` (non-null) or `Foo?` (nullable), and the compiler checks flow. This prevents a huge category of NREs.

## Records for value types

```csharp
public record UserId(Guid Value);
public record Invoice(InvoiceId Id, int AmountCents, DateOnly IssuedAt);
```

Records give you value equality, deconstruction, `with`-expressions for non-destructive update, and a concise syntax. Use records for:

- DTOs crossing boundaries.
- Value objects (`Money`, `EmailAddress`, identifiers).
- Immutable domain data.

Use classes when you need reference identity or mutable state.

## Pattern matching and switch expressions

```csharp
string Describe(Request r) => r switch {
    { Status: "pending" } => "waiting",
    { Status: "succeeded", Response: var resp } => $"got {resp}",
    { Status: "failed", Error: var e, RetryAfter: var t } => $"error {e}, retry {t}",
    _ => throw new ArgumentException(nameof(r)),
};
```

Prefer switch expressions for mapping. Use pattern matching to deconstruct:

```csharp
if (user is { IsActive: true, Role: "admin" }) { /* … */ }
```

## File-scoped namespaces

```csharp
namespace Acme.Billing;     // no braces

public class Invoice { /* … */ }
```

Less indentation, less visual noise. Use everywhere.

## Primary constructors (C# 12) — use with care

Primary constructors on `record` types are excellent. On plain `class` types, they have a subtle trap: parameters become captured fields, but they are mutable and not visible as properties. This can lead to surprising closures and confuses readers used to traditional constructors.

**Rule of thumb:** use primary constructors on records freely. On classes, use them mainly for DI-injected dependencies that you want to keep private; do not use them for data that needs to be exposed as a property.

```csharp
// Records — primary constructor is idiomatic
public record User(UserId Id, string Email);

// Classes — fine for DI
public class OrderService(IOrderRepository repository, ILogger<OrderService> log)
{
    public async Task<Order> PlaceAsync(PlaceOrder cmd, CancellationToken ct)
    {
        // use `repository` and `log` directly
    }
}
```

## Target-typed `new`

```csharp
List<User> users = new();                          // instead of `new List<User>()`
Dictionary<string, int> counts = new() { ["a"] = 1 };
```

Cleans up verbose generic instantiations.

## Collection expressions (C# 12)

```csharp
int[] nums = [1, 2, 3];
List<string> names = ["alice", "bob"];
int[] combined = [..left, 0, ..right];
```

## Raw string literals

```csharp
var sql = """
    select id, email
    from users
    where tenant_id = @TenantId
    order by created_at desc
    """;
```

No escape tax; interpolation available with `$"""`.

## Async all the way

```csharp
public async Task<User?> GetUserAsync(UserId id, CancellationToken ct)
{
    return await repository.FindAsync(id, ct);
}
```

Rules:

- **Never `async void`** except for event handlers.
- **Never `.Result` or `.Wait()`** on a Task. They deadlock and hide errors.
- **Accept `CancellationToken`** on every public async method and propagate it.
- **Use `ConfigureAwait(false)`** in library code (class libraries, NuGet packages). In ASP.NET Core and most modern app code there is no sync context, so it is a no-op — but it is still correct.
- **`ValueTask`** for hot paths where the work usually completes synchronously (e.g., a cache hit). Otherwise `Task`.

## LINQ — clear over clever

```csharp
var activeAdmins = users
    .Where(u => u.IsActive)
    .Where(u => u.Role == "admin")
    .Select(u => u.Id)
    .ToList();
```

- Materialize (`ToList`, `ToArray`) at the right moment. Chained deferred queries that re-execute are a common performance bug.
- Do not write LINQ where a `foreach` is clearer.
- Avoid projecting to anonymous types that escape the method.

## Dependency injection — with restraint

Use constructor injection. Register what actually has multiple implementations or genuine test seams. Do not register every class — the DI container becomes a distributed global variable.

```csharp
builder.Services
    .AddScoped<IOrderRepository, SqlOrderRepository>()
    .AddSingleton<IClock, SystemClock>()
    .AddHttpClient<StripeGateway>();
```

- **Constructor injection only.** Avoid property injection and service locator.
- **Scoped** for request-bound state; **Singleton** for stateless services; **Transient** rarely.
- Prefer **factories over factory interfaces** — a `Func<T>` injected is often enough.
- **No `IFoo` per `Foo`** (see below).

## Interfaces — only when they pay their keep

Create an interface when:

- Two or more real implementations exist.
- A genuine test seam is needed and other mechanisms (a test subclass, a wrapper, a fake) would not work.
- A public API needs abstraction over a third-party type.

Do not create an `IOrderService` + `OrderService` when there is one implementation. This is the single most common over-engineering pattern in C# codebases. When the second implementation materializes, extract the interface then.

## Exceptions — not for flow

- Exceptions signal exceptional conditions (programmer error, IO failure, preconditions).
- The happy path should not throw.
- Catch at boundaries (HTTP middleware, message handler, CLI main) and map to responses.
- `throw new InvalidOperationException("message")` is the default for "you called me wrong." Custom exception types when callers need to discriminate (`OrderNotFoundException` vs `DbUnavailableException`).
- For expected failures the caller must handle, prefer a result type.

## Result types (when you want them)

C# does not ship with a `Result<T, E>`. Popular options:

- **`OneOf` (library):** `OneOf<User, NotFound, DbError>`. Pattern-match on return.
- **`ErrorOr` (library):** `ErrorOr<Order>` with a list of `Error` objects.
- **Roll your own:** simple discriminated-union-style record hierarchy.

```csharp
public abstract record Result<T>;
public sealed record Ok<T>(T Value) : Result<T>;
public sealed record Err<T>(string Reason) : Result<T>;
```

Use results for domain-expected failures; use exceptions for unexpected failures.

## Collections — `IReadOnlyList<T>` at boundaries

```csharp
public IReadOnlyList<Order> GetOpenOrders() { /* … */ }
```

Expose `IReadOnlyList`, `IReadOnlyDictionary`, `IReadOnlyCollection` to callers. Return concrete types only when the caller genuinely needs the mutations.

## Value types that aren't records

- `struct` for small, immutable, heap-pressure-sensitive data. Know the costs (copy on pass, boxing when assigned to `object`).
- `readonly struct` to enforce immutability.
- `record struct` for value-equality + value-type semantics.

Default to records (reference) unless you have a measured reason for struct.

## Files, folders, projects

- **One public type per file**, filename = typename.
- **Folders map to namespaces**.
- **Project per bounded context**, not per layer. `Acme.Billing`, `Acme.Ordering` — not `Acme.Models`, `Acme.Services`.
- **Tests project per production project:** `Acme.Billing.Tests`.

## Naming conventions

Follow Microsoft's Framework Design Guidelines:

- `PascalCase` for types, methods, properties, events.
- `camelCase` for local variables and parameters.
- `_camelCase` for private fields (underscore prefix is established .NET convention).
- `PascalCase` for constants.
- No Hungarian notation.
- **Interfaces prefixed with `I`** — this is the .NET exception to the "no type prefix" rule; every .NET developer expects it, and consistency wins.
- `Async` suffix on async methods.
- Avoid `Manager`, `Helper`, `Util` — same rules as elsewhere. Exception: names that are framework-accepted (`SessionManager` in ASP.NET Core, `AuthenticationHandler`).

## Anti-patterns

### Service Locator

```csharp
// Bad
public class OrderService {
    public void Place(Order o) {
        var repo = ServiceLocator.Get<IOrderRepository>();
        repo.Save(o);
    }
}
```

Hides dependencies. Makes tests harder. Use constructor injection.

### Static `*Helper` / `*Util` classes with 20 methods

Usually a grab bag. Split into cohesive, named modules.

### Enterprise Java factories

`IFactoryProvider<T>`, `AbstractFactoryBuilder<T>`, `FactoryRegistry` — delete.

### Over-use of reflection

Reflection is a debugging and performance hazard. Use source generators or the `System.Text.Json` source-generated contexts when serialization needs drive you toward reflection.

### Blocking on async

`Task.Run(() => …).Result` — don't. Make the call chain async from top to bottom.

### Swallowed exceptions

```csharp
try { … } catch { }   // no.
```

At minimum log; ideally handle or re-throw with context.

### `async void`

Causes unhandled exceptions to crash the process. Reserve for event handlers; in every other case use `async Task`.

### Regions

`#region` blocks mostly hide large classes that should be split. Treat a region as a smell.

## Tooling

- **Analyzers:** enable `Microsoft.CodeAnalysis.NetAnalyzers`, `StyleCop.Analyzers`, and **Meziantou.Analyzer** (excellent catch-all).
- **Formatter:** `dotnet format`. Run in CI.
- **EditorConfig:** check in a repo-wide `.editorconfig` with style + analyzer rules.
- **Testing:** xUnit (most common), `FluentAssertions` for readable asserts, `NSubstitute` for mocking (less magic than Moq).

## Quick idiom cheatsheet

- `var` when the type is obvious from the right-hand side; explicit type when it clarifies intent.
- `sealed` on classes by default; unseal when extension is part of the design.
- `internal` for anything not explicitly part of the public API.
- `?.` and `??` to replace null guards.
- Range/index operators: `xs[^1]` for last element, `xs[1..^1]` for middle.
- `using var file = …;` for disposables in method scope.
- `await using` for `IAsyncDisposable`.
- `ConfigureAwait(false)` in library code; irrelevant in ASP.NET Core.
- Prefer `IAsyncEnumerable<T>` + `await foreach` to streaming via callbacks.
- `static` local functions when a helper does not need to close over captures.
