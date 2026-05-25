# Policy: web & API security

Surface-level rules independent of language. For each class: the rule, the dangerous patterns / sinks to
grep for, and the fix. Trace **untrusted input → sink**; a sink is only a finding if attacker-controlled
data reaches it without adequate neutralization for that sink's context.

## Injection (SQL / NoSQL / command / LDAP / XPath / header)

**Rule:** never build an interpreter string by concatenating untrusted input. Use parameterization /
prepared statements / safe APIs. Allowlist where structure (table names, sort columns) can't be parameterized.

- **SQL:** grep for string-built queries — `f"SELECT ... {x}"`, `"... " + x`, `query(`...`+...)`,
  template literals in SQL, `.raw(`, `sequelize.query`, `knex.raw`, `executemany` with format strings.
  Sink: any DB driver `execute`/`query`. Fix: bound parameters (`?`, `$1`, named params), ORM query
  builders, never interpolate. Watch `ORDER BY`/`LIMIT`/identifiers (not parameterizable → allowlist).
- **NoSQL:** Mongo `$where`, `$regex`, operator injection via JSON bodies (`{"$gt":""}` as a password),
  `mapReduce`/`eval`. Fix: validate types, reject objects where scalars are expected, disable server-side JS.
- **OS command:** `system`, `exec`, `popen`, `subprocess(..., shell=True)`, `child_process.exec`,
  backticks, `os/exec` with a shell, `Runtime.exec(String)`. Fix: pass argv arrays, never a shell string;
  if a shell is unavoidable, allowlist + escape. Beware argument injection (`--option`) even without a shell.
- **LDAP / XPath / SMTP header / log injection:** same shape — escape per the target grammar; for log
  injection strip CR/LF so attackers can't forge log lines.

## Cross-site scripting (XSS)

**Rule:** encode output for its HTML context (body/attr/JS/URL/CSS), or use a framework that
auto-escapes and don't defeat it.

- **Reflected/stored:** untrusted data rendered into HTML without encoding. Grep: `innerHTML`,
  `outerHTML`, `document.write`, `dangerouslySetInnerHTML`, `v-html`, `|safe`/`{% autoescape false %}`
  (Jinja), `mark_safe`, `Html.Raw`, `bypassSecurityTrustHtml`, string-built `<script>`/templates.
- **DOM XSS:** sink (`innerHTML`, `eval`, `setTimeout(str)`, `location`, `jQuery.html`) fed from
  `location`/`document.referrer`/`postMessage`/URL params. Fix: contextual encoding; `textContent` not
  `innerHTML`; DOMPurify for must-render-HTML; a strict CSP as defense-in-depth (not a substitute).
- **SVG/markdown/rich-text** uploads and renderers are XSS vectors — sanitize server-side.

## Server-side request forgery (SSRF)

**Rule:** never let untrusted input choose the destination of a server-side request without an allowlist.

Grep: HTTP clients (`requests.get`, `fetch`, `axios`, `http.Get`, `URL.openConnection`, `curl`) whose
URL/host comes from user input; webhook URLs; "fetch image/PDF from URL"; URL preview/oEmbed; PDF/SSR
renderers. Fix: allowlist hosts/schemes; resolve DNS and block private/link-local/metadata ranges
(`169.254.169.254`, `127.0.0.0/8`, `10/8`, `172.16/12`, `192.168/16`, `::1`, `fd00::/8`); block redirects
to internal targets; no `file://`/`gopher://`/`dict://`. SSRF → cloud metadata → credential theft is a
classic critical chain — flag it.

## Broken access control (IDOR / authz / path)

**Rule:** authorize **every** request against the authenticated principal on the server; never trust
client-supplied identity, role, or object ownership.

- **IDOR:** object accessed by a user-supplied id (`/orders/{id}`, `?user_id=`) without an ownership
  check. Grep: route handlers that load by id and return it without `where owner = current_user`.
- **Missing function-level authz:** admin/privileged endpoints lacking a role check; relying on the UI
  hiding a button. Grep for routes without an auth decorator/middleware in an otherwise-guarded set.
- **Mass assignment / over-posting:** binding request bodies straight to models (`Model(**body)`,
  `Object.assign(entity, body)`, `update_attributes(params)`) lets attackers set `is_admin`. Fix: explicit
  allowlists / DTOs.
- **Path traversal:** user input in a filesystem path (`../`, absolute paths, null bytes, encoded `%2e`).
  Grep: `open(`, `readFile`, `sendFile`, `path.join(base, userInput)`, archive extraction (`unzip`/`untar`
  → **Zip Slip**). Fix: canonicalize then verify the resolved path stays under the intended base;
  allowlist names; reject `..`.

## CSRF

**Rule:** state-changing requests need an anti-CSRF defense. Fix: SameSite=Lax/Strict cookies +
synchronizer/double-submit tokens, or require a custom header for JSON APIs. Grep: cookie-auth POST/PUT/
DELETE routes with no CSRF token and `SameSite=None`. (Token-in-header bearer auth is generally immune.)

## Server-side template injection (SSTI)

**Rule:** never render a template whose *source* is user-controlled. Grep: `render_template_string`,
`Template(userInput)`, Jinja/Twig/Freemarker/Velocity/Handlebars fed user input. SSTI → RCE in most
engines. Fix: render fixed templates, pass user data only as context variables.

## Insecure deserialization

**Rule:** never deserialize untrusted bytes into rich objects. Grep: `pickle.loads`, `yaml.load`
(non-safe), `marshal`, Java `ObjectInputStream`/`readObject`, .NET `BinaryFormatter`/`JavaScriptSerializer`
with type info, PHP `unserialize`, Ruby `Marshal.load`, Node `node-serialize`/unsafe `eval`-based parsers.
These are frequent RCE gadgets. Fix: use data-only formats (JSON with a schema), `yaml.safe_load`,
allowlist types, sign+verify any serialized state that must round-trip through a client.

## Authentication & session

**Rule:** strong credential storage, safe session handling, no secrets in tokens.

Check: passwords hashed with a slow KDF (`bcrypt`/`scrypt`/`argon2`, never MD5/SHA-1/unsalted SHA-256);
constant-time comparison for secrets/tokens/MACs; session cookies `HttpOnly` + `Secure` + `SameSite`;
session rotation on login (fixation); JWT — algorithm pinned (reject `alg:none`, reject HS/RS confusion),
signature verified, `exp`/`aud`/`iss` checked, no sensitive data in the (unencrypted) payload; password
reset tokens random + single-use + expiring; lockout/throttling on auth endpoints; MFA flows not bypassable.

## Transport, CORS, headers, redirects

- **TLS:** no disabled cert verification (`verify=False`, `rejectUnauthorized:false`, `InsecureSkipVerify:true`);
  no plaintext transmission of credentials/tokens.
- **CORS:** never reflect arbitrary `Origin` with `Allow-Credentials: true`; allowlist origins; never `*` with credentials.
- **Open redirect:** user-controlled redirect targets (`?next=`, `?url=`) → allowlist relative paths / known hosts.
- **Security headers** (defense-in-depth): CSP, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, HSTS.
- **Rate limiting / resource limits:** auth, expensive, and unbounded endpoints; request-size and
  pagination caps; protect against ReDoS (catastrophic-backtracking regexes on user input) and zip bombs.

## File upload & content handling

Validate type by content (magic bytes) not extension; store outside webroot; randomize names; cap size;
never execute uploads; scan archives for traversal/bombs; set correct `Content-Disposition`/`Content-Type`
on download to prevent content sniffing → XSS.

## API-specific

- **GraphQL:** depth/complexity limits (query-bomb DoS), field-level authz, disable introspection in prod,
  no batching abuse.
- **Mass data exposure:** endpoints returning whole objects (passwords, internal flags) — allowlist response fields.
- **SSRF/IDOR/authz** apply equally to REST/gRPC — the rules above are protocol-independent.
