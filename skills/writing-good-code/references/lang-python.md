# Python idioms

Modern, pragmatic Python (3.11+). The language rewards simplicity more than most; fight the urge to bring enterprise patterns in.

## PEP 8 and PEP 20

PEP 8 (style) and PEP 20 (Zen) are load-bearing. The Zen — especially "Flat is better than nested," "Sparse is better than dense," "Readability counts" — is not decoration. It is the community's aesthetic, and code that violates it feels wrong to every reviewer.

Run `python -m this` if you want to see the Zen. Internalize: *There should be one — and preferably only one — obvious way to do it.* Prefer that one way.

## Typing at boundaries

Type hints are a design tool, not a religion. Annotate:

- Public functions and methods.
- Module-level constants and exported types.
- Anything crossing a module boundary.

Skip annotations for short internal helpers and obvious locals. The goal is communication, not ceremony.

Use modern syntax (3.10+):

```python
# Good
def resolve_user(id: str) -> User | None: ...
def all_ids(users: list[User]) -> set[str]: ...

# Old-style (avoid in new code)
from typing import Optional, List, Set
def resolve_user(id: str) -> Optional[User]: ...
def all_ids(users: List[User]) -> Set[str]: ...
```

Run `pyright` (or `mypy --strict`) in CI. Pyright is generally faster and has better inference; `mypy` has a larger plugin ecosystem (e.g., for SQLAlchemy).

## Protocol vs ABC

Prefer **Protocols** (structural typing) for dependency inversion. Prefer **ABCs** only when you need runtime `isinstance` checks or shared base behavior.

```python
from typing import Protocol

class SupportsWrite(Protocol):
    def write(self, data: bytes) -> int: ...

def dump(file: SupportsWrite, payload: bytes) -> None:
    file.write(payload)
```

Any object with a matching `write` method satisfies `SupportsWrite` — no explicit inheritance. This is duck typing with a type checker.

## Data classes

Choose based on need:

- **`@dataclass` (stdlib):** default choice for simple data containers.
- **`@dataclass(frozen=True)`:** immutable value objects.
- **`attrs`:** if you want more features (validators, converters, `__slots__` by default) without a runtime dependency cost at instantiation.
- **`pydantic`:** when you need parse-from-dict validation at a boundary (HTTP, config, messages). Do not use Pydantic for pure in-memory objects — it has validation overhead on construction.
- **`msgspec.Struct`:** when performance matters and you want fast JSON/msgpack parsing with validation.

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class Invoice:
    id: str
    amount_cents: int
    issued_at: datetime
```

`slots=True` (3.10+) makes attribute access faster and memory smaller.

## Parse, don't validate (Python)

For external input (HTTP, messages, config files), use Pydantic or msgspec at the boundary:

```python
from pydantic import BaseModel, Field

class CreateOrder(BaseModel):
    user_id: str = Field(pattern=r"^[0-9a-f-]{36}$")
    items: list["OrderItem"]

class OrderItem(BaseModel):
    sku: str = Field(min_length=1)
    qty: int = Field(ge=1)

def create_order(raw: dict) -> Order:
    dto = CreateOrder.model_validate(raw)
    return insert_order(dto.user_id, dto.items)
```

One parse at the boundary; downstream code operates on the typed DTO.

## EAFP > LBYL

Easier to Ask Forgiveness than Permission. Prefer catching exceptions over pre-checking when the pre-check would duplicate the operation:

```python
# Bad — LBYL, race condition between check and use
if key in d:
    value = d[key]

# Good — EAFP
try:
    value = d[key]
except KeyError:
    value = default
```

Exception: when the check is *cheap* and the failure is a *hot path*, LBYL wins. Use judgment. Membership checks in sets (`x in s`) are O(1) and clean.

## Context managers

Any resource with a lifecycle is a context manager:

```python
with open(path) as f: data = f.read()
with lock: mutate()
with engine.begin() as conn: conn.execute(...)
```

Write your own with `contextlib`:

```python
from contextlib import contextmanager

@contextmanager
def temp_dir():
    path = mkdtemp()
    try:
        yield path
    finally:
        rmtree(path)
```

## Comprehensions vs loops

Comprehensions for pure transformations and filters:

```python
squared = [x * x for x in xs]
adults = [u for u in users if u.age >= 18]
by_id = {u.id: u for u in users}
```

Loops for side effects or multi-step processing:

```python
for u in users:
    send_email(u)
    log.info("notified", user=u.id)
```

Nested comprehensions are a smell. More than one `for` clause, or a complex `if`, belongs in a loop with a name.

## Generators and iterators

For large or streaming data, generators keep memory flat:

```python
def lines_of(path):
    with open(path) as f:
        for line in f:
            yield line.rstrip()
```

Use `yield from` for delegation. Use `itertools` (`chain`, `groupby`, `islice`, `takewhile`, `pairwise`) instead of writing the same patterns by hand.

## f-strings

Always. Never `%` formatting or `.format()` in new code.

```python
log.info(f"user {user.id} created {n_orders} orders")
```

For structured logging, pass values as kwargs to the logger, not via f-strings — the logger can serialize them richly:

```python
log.info("user created orders", user_id=user.id, count=n_orders)
```

## pathlib over os.path

```python
from pathlib import Path

config = Path.home() / ".config" / "app" / "config.yaml"
if config.exists():
    content = config.read_text()
```

Clean, cross-platform, composable. `os.path` strings are a legacy style.

## Pattern matching (3.10+)

Great for discriminating on structured data:

```python
match event:
    case {"type": "order_placed", "order_id": oid}:
        handle_order_placed(oid)
    case {"type": "order_cancelled", "order_id": oid, "reason": reason}:
        handle_cancellation(oid, reason)
    case _:
        log.warning("unknown event", event=event)
```

Better than long `if/elif/else` chains on `event["type"]`. Exhaustiveness is not compiler-checked (unlike TypeScript's discriminated unions), so pair with explicit type hints and mypy/pyright.

## Classes — sparingly

Python is multi-paradigm. Use classes when:

- State and behavior are genuinely coupled (maintained invariants between method calls).
- You need an identity-bearing object.
- A framework requires it (e.g., Django models, Flask class-based views).

Otherwise: functions + modules. A module *is* a singleton. A class with only `@staticmethod` decorators is a module in disguise — convert it.

Avoid deep inheritance. Prefer composition. Mixins are acceptable for true orthogonal concerns but become confusing fast.

## Typing tricks worth knowing

```python
from typing import NewType, Literal, TypeAlias, Self, overload

UserId = NewType("UserId", str)          # branded type
Status = Literal["pending", "ok", "err"] # literal union
RequestId: TypeAlias = str               # explicit alias

class Builder:
    def step(self) -> Self: ...          # 3.11+, returns the concrete subtype
```

`TypedDict` for dict-shaped data crossing boundaries (prefer dataclasses inside the boundary):

```python
from typing import TypedDict

class OrderRow(TypedDict):
    id: str
    amount_cents: int
```

## Anti-patterns

### Mutable default arguments

```python
# Bug — same list shared across all calls
def add(item, bag=[]):
    bag.append(item)
    return bag
```

Use `None` and initialize inside:

```python
def add(item, bag=None):
    bag = bag or []
    bag.append(item)
    return bag
```

### `import *`

Pollutes namespace, hides origins. Import what you use.

### `type(x) == Foo`

Use `isinstance(x, Foo)` — handles subclasses; raises on bad types.

### Global mutable state

Module-level variables that functions mutate are a test-isolation nightmare. Prefer passing state explicitly or using dependency-injected objects.

### Metaclass abuse

If a decorator works, use a decorator. If a base class works, use a base class. Metaclasses are powerful and opaque — reserve for library authors with a clear need (ORMs, validators).

### Deep inheritance

More than two levels of inheritance is usually wrong. Composition, protocols, and plain functions handle most cases.

### Catching broad exceptions

```python
# Bad
try:
    risky()
except:
    pass

# Better
try:
    risky()
except SomeError as e:
    log.warning("known failure", error=str(e))
    # handle or re-raise
```

Bare `except:` catches even `KeyboardInterrupt` and `SystemExit`. Always narrow.

### Over-class-ified functions

A class with one method and a constructor is a function:

```python
# Convert this
class OrderProcessor:
    def __init__(self, db): self.db = db
    def process(self, order): ...

# To this
def process_order(order, db): ...
```

Or, if the dependency is cross-cutting, use a partial / closure:

```python
from functools import partial

process = partial(process_order, db=db)
```

## Tooling (2024-2026)

- **Package manager:** `uv` (Astral). Fast. Handles venvs, project config, and tool install. Replaces `pip`, `pip-tools`, `virtualenv`, `pyenv` for most workflows.
- **Linter / formatter:** `ruff` (Astral). One tool for both, replacing `flake8`, `isort`, `pyupgrade`, `pydocstyle`, `black`. Very fast.
- **Type checker:** `pyright` (Microsoft) or `mypy` (community). Pyright is generally faster and has better inference; mypy has broader plugin ecosystem.
- **Testing:** `pytest`. Always `pytest`. Fixtures over `setUp`/`tearDown`. Parametrize for table-driven tests.
- **Async:** `asyncio`. `httpx` for HTTP. `asyncpg` / `psycopg3` for PostgreSQL.

## Quick idiom cheatsheet

- `list(x)` / `dict(x)` / `set(x)` for copies; `copy.deepcopy(x)` only when shallow is not enough.
- `enumerate(xs)` over manual index counters.
- `zip(xs, ys)` over parallel loops.
- `any(...)` / `all(...)` over boolean accumulator loops.
- `sorted(xs, key=...)` over custom comparator.
- `collections.Counter` for frequency tables.
- `collections.defaultdict` for grouping.
- `functools.cache` for memoization.
- `itertools.chain.from_iterable` for flattening one level.
- `_` for unused variables; `__` for double-underscore-private to avoid mangling only when you mean it.
