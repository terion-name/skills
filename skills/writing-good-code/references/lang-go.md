# Go idioms

Go has strong idioms. The community enforces them. Deviation makes code unidiomatic, which makes it harder to maintain, not original. When in doubt, follow the [Go Proverbs](https://go-proverbs.github.io/) and Effective Go.

## The proverbs that matter most

- **Don't communicate by sharing memory; share memory by communicating.**
- **Concurrency is not parallelism.**
- **Channels orchestrate; mutexes serialize.**
- **The bigger the interface, the weaker the abstraction.**
- **Make the zero value useful.**
- **`interface{}` says nothing.** (Now `any`, same meaning.)
- **Gofmt's style is no one's favorite, yet gofmt is everyone's favorite.**
- **A little copying is better than a little dependency.**
- **Clear is better than clever.**
- **Errors are values.**
- **Don't just check errors, handle them gracefully.**

Every rule below descends from these.

## Accept interfaces, return structs

Define interfaces at the **consumer** side, with the smallest set of methods needed. Return concrete types from constructors.

```go
// Good — interface at consumer, concrete return
package payments

type Charger interface {
    Charge(ctx context.Context, amount Cents) error
}

func Settle(ctx context.Context, c Charger, amt Cents) error { ... }

// …elsewhere…
package stripe

func New(apiKey string) *Client { ... }   // concrete, not an interface
```

This is the inverse of Java/C# conventions. Do not define `PaymentService` interfaces in a `payments` package with one implementation somewhere else. The interface belongs where it is used, sized to that use.

## Small interfaces

```go
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type Closer interface { Close() error }
```

`io.Reader` has one method. Dozens of concrete types satisfy it. That is the Go way. A 10-method interface is usually three interfaces glued together.

**Rule of thumb:** if your interface has more than 3-4 methods, ask whether you have two interfaces.

## Errors are values

```go
user, err := findUser(ctx, id)
if err != nil {
    return fmt.Errorf("finding user %s: %w", id, err)
}
```

- Wrap with `%w` to preserve the causal chain.
- Add context at each layer (what were you trying to do?).
- Use `errors.Is(err, ErrNotFound)` for sentinel errors, `errors.As(err, &target)` for typed errors.
- Name sentinel errors `ErrFoo` at package level.

```go
var ErrNotFound = errors.New("not found")

if errors.Is(err, payments.ErrNotFound) { ... }
```

Define custom error types when callers need structured information:

```go
type ValidationError struct {
    Field   string
    Message string
}
func (e *ValidationError) Error() string { return e.Field + ": " + e.Message }
```

## `context.Context` as the first parameter

Any function that does I/O, RPC, or long work takes `ctx context.Context` as its first argument:

```go
func GetUser(ctx context.Context, id UserID) (*User, error) { ... }
```

- Propagate `ctx` everywhere downstream.
- Cancel and timeout via `context.WithCancel` and `context.WithTimeout`.
- Do not store `ctx` in a struct (it is request-scoped).
- Do not pass `nil` ctx — use `context.Background()` or `context.TODO()`.

## Zero values

Make them useful. A `sync.Mutex{}`, a `bytes.Buffer{}`, a zero-value `http.Client{}` are all ready to use. Design your types the same way:

```go
type Counter struct {
    mu    sync.Mutex
    count int64
}

func (c *Counter) Inc() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}
```

No constructor needed; `var c Counter` works.

## Don't export by default

Start lowercase (package-private). Export a symbol only when a caller outside the package needs it. Every exported name is a public API commitment.

## Package design

- **Package names are short, lowercase, one word:** `users`, `billing`, `http`.
- **No `util` / `helpers` / `common` packages.** Move each function to its concept's package.
- **No `base` / `core` / `shared`.** Same reason.
- **Package name and directory name match.**
- **Package path expresses intent:** `github.com/acme/billing/invoices`.
- A package is imported using its last path segment — design names accordingly. `bytes.Buffer` reads well; `util.Buffer` does not.
- Circular imports mean your boundary is wrong. Split or move types.

## Don't reflex-create getters and setters

```go
type User struct {
    ID    UserID
    Email string
}

u.Email = "..."   // direct access is idiomatic
```

Expose fields directly. Introduce accessors only when you need invariants, lazy initialization, or validation.

If a getter exists, do not call it `GetEmail` — Go style is just `Email()`. Prefix `Get` only when there is a corresponding `Set`.

## Composition via embedding

```go
type Logger struct { /* ... */ }
func (l *Logger) Info(msg string) { ... }

type Server struct {
    Logger                       // embedding, not inheritance
    addr string
}

s := &Server{Logger: log, addr: ":8080"}
s.Info("started")                // inherited method
```

Embedding is composition with convenience, not inheritance. Do not use it to model "is-a"; use it to compose capabilities.

## Tests — table-driven

```go
func TestValidate(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        wantErr bool
    }{
        {"empty", "", true},
        {"too short", "ab", true},
        {"ok", "hello", false},
    }
    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            err := Validate(tc.input)
            if (err != nil) != tc.wantErr {
                t.Errorf("Validate(%q): got err=%v, want err=%v", tc.input, err, tc.wantErr)
            }
        })
    }
}
```

- `t.Run` for subtests — names must be unique and stable.
- `t.Helper()` in test helpers.
- `t.Cleanup()` over `defer` for test teardown.
- Use the standard `testing` package. Avoid heavy testing frameworks; the standard tools are good.
- Use `testify/assert` and `testify/require` if the team already does. Many projects avoid it to keep tests vanilla.

## Concurrency

- Goroutines are cheap but not free. Every `go f()` must have a clear lifetime.
- If you start a goroutine, you must know how it ends (channel close, context cancel, explicit done signal).
- **Never start a goroutine in a library without a way for the caller to stop it.**
- Prefer channels for hand-off between goroutines.
- Prefer `sync.Mutex` for protecting shared state.
- `sync.RWMutex` only when profiling shows reader contention; simple `Mutex` is usually faster for low contention.
- `sync/atomic` for counters and simple flags.
- `errgroup` from `golang.org/x/sync/errgroup` for concurrent tasks with error propagation.

```go
g, ctx := errgroup.WithContext(ctx)
for _, u := range urls {
    u := u
    g.Go(func() error { return fetch(ctx, u) })
}
if err := g.Wait(); err != nil { return err }
```

## Generics — sparingly

Go generics (1.18+) are for:

- **Containers** (`type Set[T comparable] map[T]struct{}`).
- **Algorithmic helpers on sequences** (`slices.Contains`, `maps.Keys`).
- **Pure type-parameter utilities** where `any` would lose information.

Not for:

- Rewriting interface-based APIs to "make them generic."
- Replacing `any` throughout a codebase.

Use the minimum constraint. Prefer `comparable` or a constraint from `constraints.Ordered` over `any` when possible.

## Anti-patterns

### `any` in public APIs

Exported functions and types should not accept or return `any` (or `interface{}`). If you need polymorphism, use an interface; if you don't, use concrete types.

### Large interfaces

A 20-method interface for a service is an inversion of the Go idiom. Split.

### `init()` with logic

`init()` runs at import time. Side effects in `init` are untestable and order-sensitive. Reserve for registering self-describing things (like a driver registering itself). Do not do I/O, read config, or start goroutines in `init`.

### Panic as flow control

Panics are for unrecoverable situations. Ordinary errors go through the error return value. Recovering from panic in production code is limited to: top-level HTTP/GRPC servers, to prevent a single-request panic from crashing the process.

### Naked returns in long functions

```go
// Bad — what is actually returned?
func (s *Server) process(ctx context.Context, r *Request) (user *User, orders []Order, err error) {
    // ... 50 lines ...
    return
}
```

Be explicit: `return user, orders, nil`. Naked returns are acceptable only in tiny functions.

### Mutex in an exported struct field

```go
// Bad
type Cache struct {
    Mu    sync.Mutex
    Items map[string]int
}
```

Callers might try to lock it themselves, or worse, copy the struct and break the mutex. Make it unexported:

```go
type Cache struct {
    mu    sync.Mutex
    items map[string]int
}
```

### Forgetting to close

`defer res.Body.Close()`, `defer rows.Close()`, `defer file.Close()`. Forgetting these leaks resources. Run `go vet` and use `errcheck` linter.

### Checking errors with `== nil` for typed errors

```go
// Bad — doesn't work with wrapped errors
if err == ErrNotFound { ... }

// Good
if errors.Is(err, ErrNotFound) { ... }
```

### Deep package trees

`github.com/acme/app/internal/services/billing/v2/handlers/http/routes/payments/...` is a smell. Flatten.

## Tooling

- **Format:** `gofmt` (not optional; integrate into editor save).
- **Imports:** `goimports` (adds/removes imports automatically).
- **Vet:** `go vet ./...` in CI.
- **Lint:** `golangci-lint` with a curated preset. Start with `govet`, `errcheck`, `staticcheck`, `revive`, `gosimple`, `unused`, `gosec`, `ineffassign`. Add more gradually.
- **Race detector:** `go test -race ./...` in CI.
- **Modules:** `go mod tidy` to clean up.

## Quick idiom cheatsheet

- `if err != nil { return err }` — most common line in Go.
- `defer` for cleanup, right after acquisition.
- Pre-allocate slices when size is known: `make([]Item, 0, n)`.
- `range` ignores the second value with `for _, x := range xs`.
- Capture loop variables: `for _, x := range xs { x := x; go f(x) }` (no longer needed in Go 1.22+, which scopes the loop var).
- Struct tags for serialization: `` `json:"email,omitempty"` ``.
- Enum-ish via `type X int` + `const ( A X = iota; B )`.
- Named return values when they document the return; otherwise prefer explicit returns.
- `nil` slice and `nil` map semantics: a nil slice is valid for `append` and `range`; a nil map is valid for reading (returns zero) but panics on write.
