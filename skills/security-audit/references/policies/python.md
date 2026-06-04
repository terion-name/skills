# Policy: Python

Read alongside `web-and-api.md`. This covers Python-specific dangerous APIs and idioms.

## Code/command execution sinks

**Rule:** no untrusted input into evaluators or shells.

Grep: `eval`, `exec`, `compile`, `__import__(userInput)`, `subprocess.*(..., shell=True)`, `os.system`,
`os.popen`, `commands.*`, `pty.spawn`. Fix: remove dynamic eval; `subprocess.run([...], shell=False)` with
an argv list; validate/allowlist any program name or argument that comes from input (guard argument injection too).

## Insecure deserialization

**Rule:** never unpickle / unsafely-load untrusted bytes.

Grep: `pickle.loads`/`pickle.load`, `cPickle`, `marshal.loads`, `shelve`, `dill`, `joblib.load`,
`yaml.load` **without** `Loader=SafeLoader` (use `yaml.safe_load`), `jsonpickle`. All are RCE gadgets on
attacker bytes. Fix: JSON/`safe_load`; if you must accept serialized objects, sign+verify them.

## Injection

- **SQL:** never `cursor.execute("... %s" % x)` or f-strings/`.format` in SQL; use parameter binding
  (`execute(sql, params)`). Django: avoid `.raw()`/`.extra()` with interpolation; SQLAlchemy: use bound
  params / `text()` with params, not string concat.
- **Template (SSTI):** Jinja `render_template_string(userInput)` or `Template(userInput)` → RCE; `|safe`
  / `{% autoescape false %}` / `mark_safe` → XSS. Render fixed templates; pass data as context only.
- **Server-side `format`:** `userInput.format(...)` / `%`-format on attacker strings can leak attributes
  (`{0.__class__}`); don't format with user-controlled format strings.

## SSRF / file / path

`requests`/`urllib`/`httpx` with user URLs (allowlist + block internal ranges); `open(userPath)`,
`os.path.join(base, user)`, `send_file`, `tarfile.extractall`/`zipfile.extractall` (traversal/Zip Slip —
validate members, use `filter='data'` on 3.12+). `xml.etree`/`lxml` with external entities → XXE
(use `defusedxml`).

## Crypto & randomness

`random` module for tokens/keys/passwords (predictable) → use `secrets` / `os.urandom`. Weak hashes
(`hashlib.md5`/`sha1`) for passwords → `argon2`/`bcrypt`/`scrypt`/`pbkdf2`. `hashlib` comparisons for
secrets → `hmac.compare_digest` (timing). Hardcoded keys/IVs; ECB mode; static/predictable IVs.

## Web frameworks

- **Django:** `DEBUG=True` in prod (info leak), `ALLOWED_HOSTS=['*']`, `SECRET_KEY` committed, CSRF
  exemptions (`@csrf_exempt`), `mark_safe`/`|safe`, `eval`/`pickle` in views, missing `@login_required`/
  permission checks (IDOR), `extra()`/`raw()` SQL.
- **Flask/FastAPI:** `app.run(debug=True)` exposing the Werkzeug console (RCE), `SECRET_KEY` hardcoded,
  `render_template_string`, missing auth dependencies on routes, over-broad CORS, returning whole ORM
  objects (mass exposure).
- **Mass assignment:** `Model(**request.json)` / `setattr` loops → allowlist fields.

## Other

- **`assert` for security checks:** stripped under `python -O` — never gate authz/validation on `assert`.
- **Temp files:** `tempfile.mktemp` (race) → `mkstemp`/`NamedTemporaryFile`; predictable `/tmp` paths
  (world-writable race, like the example finding's class).
- **`requests(..., verify=False)`** disables TLS verification.
- **Logging secrets:** tokens/passwords in log statements.

## Tools

`bandit -r <pkg> -f sarif`, `pip-audit` / `safety` (CVE deps), `semgrep --config p/python`. Confirm hits against code.
