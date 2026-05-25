# Policy: Go

Read alongside `web-and-api.md`. Go is memory-safe outside `unsafe`/cgo, so focus on injection, authz,
crypto, and concurrency.

## Command / SQL injection

- **Command:** `exec.Command("sh", "-c", userInput)` reintroduces a shell — pass argv directly
  (`exec.Command(bin, arg1, arg2)`), and guard argument injection. Never build the command string from input.
- **SQL:** `fmt.Sprintf` into a query then `db.Query(q)` → use placeholders (`db.Query("... WHERE id=$1", id)`
  / `?`). `database/sql` parameterizes; string-built queries don't.
- **Template:** `text/template` does **not** escape — for HTML always use `html/template`. Rendering a
  template parsed from user input is SSTI.

## SSRF / path / file

User-controlled URLs into `http.Get`/`http.Client.Do` (allowlist + block internal ranges, control
redirects via `CheckRedirect`). `filepath.Join(base, userInput)` + `os.Open`/`http.ServeFile` → traversal;
canonicalize with `filepath.Clean` and verify the result is under base (`strings.HasPrefix` after
`filepath.Abs`). `archive/zip`/`tar` extraction → Zip Slip: validate each entry path.

## Crypto & randomness

`math/rand` for tokens/keys (predictable, even with seeding) → `crypto/rand`. Weak hashes (`crypto/md5`,
`crypto/sha1`) for passwords → `golang.org/x/crypto/bcrypt`/`argon2`/`scrypt`. Non-constant-time secret
comparison → `crypto/subtle.ConstantTimeCompare`. `tls.Config{InsecureSkipVerify: true}` disables verification.
ECB / static IV / hardcoded keys.

## Concurrency

Data races (run `go test -race`; the race detector is authoritative evidence): shared maps without a
mutex (concurrent map write → crash/DoS), racy struct fields, closures capturing loop variables (pre-1.22).
Unbounded goroutine creation per request → DoS. Missing `context` cancellation → resource exhaustion.

## Error handling & input

- **Ignored errors:** `_ =` on security-relevant calls (auth checks, signature verification, `Close` on
  writers that flush). A swallowed verification error can mean "treated as valid".
- **Integer/slice bounds:** conversions (`int` from a parsed length), slice reslicing with input indices →
  panic/DoS or logic bug; validate before indexing.
- **`unsafe` / cgo:** apply `memory-safety.md` at the boundary — pointer arithmetic, `unsafe.Pointer`
  casts, C string lengths.

## Web specifics

Missing auth middleware on a route group; `net/http` servers without timeouts (`ReadTimeout`/`WriteTimeout`/
`IdleTimeout`) → slowloris DoS; request body without `http.MaxBytesReader` → memory DoS; permissive CORS;
JWT libs not verifying `alg`. Returning whole structs as JSON (mass exposure) — use response DTOs / `json:"-"`
on sensitive fields.

## Tools

`govulncheck ./...` (reachability-aware CVE detection — low false positives, trust it), `gosec -fmt sarif`,
`go vet`, `go test -race`, `staticcheck`. Confirm hits against code.
