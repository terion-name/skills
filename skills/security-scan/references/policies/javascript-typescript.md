# Policy: JavaScript / TypeScript (Node + browser)

Read alongside `web-and-api.md` (XSS, SSRF, injection, authz all apply). This covers JS/TS-specific
dangerous APIs and idioms.

## Code execution sinks

**Rule:** never feed untrusted input to a code evaluator.

Grep: `eval`, `new Function`, `setTimeout`/`setInterval` with a string arg, `vm.runIn*` /
`vm.runInNewContext` (the `vm` module is **not** a security sandbox), `require(userInput)` /
`import(userInput)`, `child_process.exec`/`execSync` (shell — use `execFile`/`spawn` with an argv array),
template engines compiled from user input (SSTI). Fix: remove dynamic eval; argv arrays for subprocess.

## Prototype pollution

**Rule:** never recursively merge / set-by-path with attacker-controlled keys without blocking
`__proto__`, `constructor`, `prototype`.

Grep: deep-merge/`extend`/`set(obj, path, val)` helpers, `Object.assign` from request bodies, query-string
parsers, old `lodash.merge`/`set`. Polluting `Object.prototype` can flip security flags app-wide and chain
to RCE via gadget. Fix: `Object.create(null)` maps, `Map`, key allowlists, reject the magic keys, freeze prototypes.

## Insecure deserialization / parsing

`node-serialize`, `funcster`, `eval`-based JSON, unsafe `js-yaml` `load` (use `safeLoad`/`DEFAULT_SCHEMA`),
`serialize-javascript` misuse. XML parsers: disable external entities (XXE) — see below.

## XXE (XML external entities)

`libxmljs`, `xmldom`, SAX parsers with entity expansion enabled → file read / SSRF / DoS. Fix: disable
DTD/external entity resolution; prefer JSON.

## Regular-expression DoS (ReDoS)

User input matched against a regex with catastrophic backtracking (nested quantifiers, `(a+)+`, overlapping
alternations). Grep user-facing `RegExp`/`.match`/`.test`. Fix: linear-time regex (RE2), input length caps,
anchored patterns, validate the regex isn't attacker-supplied.

## TypeScript-specific traps

- `as`/`as any`/`!` (non-null assertion) and `@ts-ignore` can mask an unchecked-input bug — TS types are
  erased at runtime and give **no** runtime validation. Validate external data (HTTP bodies, env, JSON) at
  the boundary with a runtime schema (zod/io-ts/valibot); a typed-but-unvalidated `req.body as User` is a lie.
- Don't trust `unknown`-narrowing that's actually a cast.

## Node platform

- **Path traversal / Zip Slip:** `path.join(base, userInput)`, archive extraction; canonicalize and verify
  containment (see `web-and-api.md`).
- **SSRF:** `fetch`/`axios`/`http.request` with user URLs; follow-redirect to internal hosts.
- **Secrets:** `.env` committed, secrets in `process.env` logged, secrets in client bundles (anything in a
  browser build is public — check Next.js `NEXT_PUBLIC_*`, Vite `import.meta.env`).
- **Insecure randomness:** `Math.random()` for tokens/ids/keys → use `crypto.randomUUID`/`crypto.randomBytes`.
- **`postMessage`:** verify `event.origin`; never `targetOrigin: "*"` with sensitive data.
- **CORS / cookies:** `cors({origin:true})` reflects any origin; set `httpOnly`+`secure`+`sameSite` on cookies.

## Dependencies & supply chain

`npm audit` / `pnpm audit`; lockfile committed and integrity-checked; beware `postinstall` scripts in
dependencies, dependency-confusion (private scope not claimed publicly), and typosquats. See
`secrets-and-supply-chain.md`.

## Tools

`semgrep --config p/javascript --config p/typescript --config p/owasp-top-ten`; `eslint` with
`eslint-plugin-security` if configured; `npm audit --json`. Confirm every hit against code.
