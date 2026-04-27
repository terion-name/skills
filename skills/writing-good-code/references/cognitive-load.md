# Cognitive load — mechanical proxies for human confusion

You, as an agent, do not feel confusion. Human readers do, and their confusion is the root of most bugs, stalled PRs, and hostile ownership transitions. This reference gives you **observable properties** of code that correlate with high cognitive load, so you can keep it low.

## Why this matters

Humans hold roughly 4 items in working memory at once (Cowan, 2001, updating Miller's classic 7±2). When a code unit requires tracking more than 4 simultaneously relevant facts — variables, preconditions, branches, side effects — comprehension collapses, and with it goes the ability to change the code safely. Every rule below exists to keep a reading under that ceiling.

Two kinds of load matter (Sweller's cognitive load theory, applied to code by Artem Zakirullin):

- **Intrinsic load** — inherent to the problem. Irreducible. A genuinely complex business rule is genuinely complex.
- **Extraneous load** — imposed by *how* you wrote it. Reducible, and your job.

Familiarity is not simplicity. Code feels simple to its author because the author built state incrementally; the reader arrives at it all at once.

## Mechanical proxies, in order of leverage

Apply top-down. Earlier ones are cheaper to fix and produce larger readability gains.

### 1. Nesting depth

- **Threshold:** max indentation in a function ≤ 3.
- **Why:** each level adds a context the reader must hold ("I am inside the `if authorized`, inside the `for each item`, inside the `try`…"). By level 4 you have exceeded working memory.
- **Remedy:** guard clauses for preconditions; early returns; extract the deepest block into a named function; replace nested ternaries with an explicit `switch` or lookup.

### 2. Boolean operand count in a single decision

- **Threshold:** subexpressions joined by `&&` / `||` ≤ 3. `!` counts toward complexity.
- **Remedy:** extract named intermediate booleans:
  ```ts
  // Before
  if (user && user.active && !user.suspended && (user.role === "admin" || hasOverride))
  // After
  const isLoggedIn = user && user.active && !user.suspended;
  const canAct = user?.role === "admin" || hasOverride;
  if (isLoggedIn && canAct)
  ```

### 3. Function length (with a caveat)

- **Soft ceiling:** ~40 lines for typical code.
- **Caveat:** Ousterhout and Carmack both argue against mechanical splitting. A long function can be fine *if* it stays at one abstraction level and reads top-to-bottom like a recipe. **Short + shallow is worse than long + cohesive.** The actual smell is *mixed abstraction levels*, not length.
- **Remedy:** split by abstraction level, not by line count. If within a function you find yourself writing both `sendEmail(user)` and `socket.write(b"\r\n")`, split.

### 4. Parameter count

- **Threshold:** ≤ 4.
- **Remedy:** introduce a parameter object; preserve a whole object (pass `user` instead of `user.id, user.name, user.email`); split the function if the parameters fall into two unrelated groups.

### 5. Flag parameters

- **Target:** 0.
- **Why:** each boolean flag is strong evidence of two concepts fused into one function. The caller reads `render(user, true, false, true)` and has no idea what it does.
- **Remedy:** split into differently named functions (`renderCompact`, `renderFull`), or accept an options object with named keys when truly optional configuration. See `anti-patterns.md` for the full wrong-abstraction story.

### 6. Inheritance chain depth

- **Threshold:** ≤ 2.
- **Why:** method resolution becomes a research project; changes in a base class ripple silently.
- **Remedy:** composition. Depend on interfaces/protocols at the consumer, inject concrete types.

### 7. Interface-to-implementation ratio

- **Metric:** public signature count ÷ non-trivial implementation lines.
- **High ratio (close to 1)** ⇒ shallow module.
- **Remedy:** merge, inline, or redesign so the interface hides more.

### 8. File-hops per unit of behavior

- **Target:** 0–1 file. 2 is acceptable. 3+ is a Locality of Behavior violation.
- **Why:** every hop forces a reader to swap working-memory contents. Three hops and the thread is lost.
- **Remedy:** colocate. Put the handler next to the route, the styles next to the component, the query next to the use site, unless there is true knowledge duplication to prevent.

### 9. Abstraction layers per request path

- **Warning:** Controller → Service → UseCase → Repository → Gateway, with each layer being a thin pass-through.
- **Test:** each layer must hide a real secret (a design decision likely to change). If `UserRepository.getById` only calls `db.query("select * from users where id=?")`, the repository hides nothing.
- **Remedy:** collapse pass-through layers; introduce a layer when a real secret appears.

### 10. Stack-trace depth to user code

- **Warning:** if an exception from your code routes through >10 framework frames before reaching your code, the framework owns too much of your logic. You will debug every problem through the framework's internals.
- **Remedy:** thinner framework surface; favor libraries (you call them) over frameworks (they call you) when it's marginal.

### 11. Distinct project-specific vocabulary

- **Metric:** count the domain-specific, DSL, DDD-aggregate, or in-house-pattern terms a new reader must learn before editing.
- **Why:** each term is extraneous load imposed on readers who just want to change a button's copy. DDD rituals (aggregate roots, domain events, application services) applied outside their sweet spot often net-increase cognitive load.
- **Remedy:** use ceremony only where it pays back; use plain language otherwise.

### 12. Services per engineer

- **Warning:** more microservices than engineers on the team ⇒ probably a distributed monolith. Every cross-cutting change becomes a multi-service release dance.
- **Remedy:** merge services that always change together.

### 13. Suspect-suffix hit rate

- **Metric:** grep for `Manager|Helper|Handler|Util|Processor|Wrapper|Info|Data|Base|Abstract`.
- **Threshold:** every hit should justify itself with a domain term or framework convention; otherwise flag.
- **Remedy:** see `naming.md`.

### 14. Parameter-keyed conditionals inside a helper

- **Warning:** growing over time.
- **Why:** Metz decay — a shared helper accumulating per-caller branches is becoming the Wrong Abstraction.
- **Remedy:** inline back, delete dead branches per caller, re-derive. See `abstraction-quality`.

### 15. Status-code / error-code smuggling

- **Warning:** HTTP `401` meaning "token expired" and `403` meaning "role lacks permission" when the spec does not imply that split; overloading numeric codes with business meaning.
- **Why:** forces every client to memorize your interpretation. Each is a working-memory slot.
- **Remedy:** self-describing error objects in the response body (`{"code": "TOKEN_EXPIRED", "retryable": true}`).

## Readability rules with cognitive backing

- **Line-of-sight.** Happy path at the baseline indent. Preconditions fail fast and return.
- **Single Level of Abstraction per function (SLAP).** Do not mix `sendEmail(user)` and `socket.write(b"\r\n")` in the same function. Granularity must not shift mid-read.
- **Scope-length correlation for names.** Tight scope: `i`. Function local: `count`. Module level: `activeUserCount`. Public API: precise multi-word name.
- **Consistency > local optimality.** Matching the codebase's dominant pattern is almost always correct unless you have a concrete technical reason. Each deviation costs a working-memory slot.
- **Least astonishment.** `get_*` should not write. `is_*` should return bool, not throw. Iteration should not mutate its input. Operations should preserve the semantic expectations of their receiver type.

## Don't outsmart the reader

Kernighan: *"Debugging is twice as hard as writing the code, so if you write as cleverly as possible, you are, by definition, not smart enough to debug it."*

When a clever and a plain version are equally correct, the plain version is more correct in total — it saves the reader's working memory for the actually-intrinsic parts of the problem. Clever saves lines, not time. Plain saves time, which is what the team is spending.

## A quick self-check

Before finishing a function or module:

- [ ] Maximum indent ≤ 3?
- [ ] Every `if`/`while` has ≤ 3 boolean operands?
- [ ] ≤ 4 parameters, 0 flag parameters?
- [ ] One-sentence description has no "and"?
- [ ] A reader could understand this without opening another file 3 levels deep?
- [ ] Names are domain nouns/verbs, not suffix-boats?
- [ ] If I inlined this one step up, would it read worse? If not, inline it.
