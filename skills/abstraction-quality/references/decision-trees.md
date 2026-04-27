# Decision trees for abstraction decisions

Four flowcharts. Each is a procedure for one specific recurring question. Run the procedure top-to-bottom; do not skip steps. A "no" anywhere means the abstraction is not yet justified.

---

## Tree 1 — Should I extract this abstraction?

```
                         start
                           │
                           ▼
       ┌───────────────────────────────────────┐
       │ Q1. Can I name it with a domain noun  │
       │ or verb (NOT Manager/Helper/Util/     │
       │ Wrapper/Handler/Processor/Base/Impl)? │
       └───────┬───────────────────────┬───────┘
               yes                     no
               │                       │
               ▼                       ▼
       ┌──────────────┐        DO NOT EXTRACT
       │ Q2. Are there│        The concept is not real yet.
       │ ≥3 call sites│        Duplicate; tag with a comment.
       │ that share   │
       │ this concept │
       │ (Rule of 3)? │
       └──┬───────┬───┘
          yes     no
          │       └────► DO NOT EXTRACT (Rule of Three)
          ▼
       ┌────────────────────────────┐
       │ Q3. Do all callers need    │
       │ the same behavior          │
       │ (no per-caller flags or    │
       │ new parameters)?           │
       └──┬─────────────────────┬───┘
          yes                   no
          │                     └────► DO NOT EXTRACT
          ▼                            Wrong seam — would create the
       ┌──────────────────────┐        Wrong Abstraction with flag
       │ Q4. Is the interface │        parameters from day one.
       │ substantially smaller│
       │ than the impl        │
       │ (depth ≥ 3:1 ratio)? │
       └──┬───────────────┬───┘
          yes             no
          │               └────► DO NOT EXTRACT
          ▼                      You'd create a shallow module —
       ┌────────────────┐         pure interface tax for no benefit.
       │ Q5. Would      │
       │ inlining       │
       │ produce        │
       │ clearly worse  │
       │ code?          │
       └──┬─────────┬───┘
          yes       no
          │         └────► PREFER INLINE
          ▼                If inline is no worse, it's better.
       ┌─────────────────┐
       │ Q6. Is the      │
       │ domain stable   │
       │ enough that the │
       │ shape won't     │
       │ shift soon?     │
       └──┬──────────┬───┘
          yes        no
          │          └────► DO NOT EXTRACT YET
          ▼                  Learn more first. Premature
       EXTRACT.              abstraction in an unstable domain
                             is the most expensive abstraction.
```

Apply ruthlessly. Extracting too early is worse than not extracting.

---

## Tree 2 — Should I add this abstraction layer?

```
                         start
                           │
                           ▼
       ┌──────────────────────────────────────┐
       │ Q1. What design decision does this   │
       │ layer hide? (the Parnas secret)      │
       │ State it in one sentence.            │
       └──┬───────────────────────┬───────────┘
          can name it             can't name it
          │                       └────► DO NOT ADD
          ▼                              No secret = no module.
       ┌─────────────────────────┐
       │ Q2. Does that decision  │
       │ change often enough to  │
       │ pay back the layer?     │
       │ (Has it changed at      │
       │ least once historically │
       │ or are 2+ variations    │
       │ already real?)          │
       └──┬───────────────────┬──┘
          yes                 no
          │                   └────► DO NOT ADD (YAGNI)
          ▼                          Speculative generality.
       ┌─────────────────────────┐
       │ Q3. Does this layer     │
       │ introduce a new         │
       │ abstraction (different  │
       │ from its neighbors),    │
       │ NOT a pass-through?     │
       └──┬───────────────────┬──┘
          yes                 no
          │                   └────► DO NOT ADD
          ▼                          Pass-through layers are pure cost.
       ┌─────────────────────────┐
       │ Q4. Does the layer's    │
       │ interface have ≤ ~5     │
       │ methods, each carrying  │
       │ real semantics?         │
       └──┬───────────────────┬──┘
          yes                 no
          │                   └────► RESHAPE OR DON'T ADD
          ▼                          Big interfaces = weak abstractions.
       ADD THE LAYER.
```

A layer pays its keep when it hides a real, changing decision behind a small, semantically loaded interface.

---

## Tree 3 — Is this class/function doing too much?

```
                         start
                           │
                           ▼
       ┌──────────────────────────────────────┐
       │ Q1. Can I describe its purpose in    │
       │ ONE sentence WITHOUT using "and"?    │
       └──┬─────────────────────────┬─────────┘
          yes                       no (need "and")
          │                         └────► SPLIT
          ▼                                 Two concepts wearing a trench coat.
       ┌────────────────────────────────┐    Extract Class along the "and".
       │ Q2. Do the fields/parameters   │
       │ used by different methods form │
       │ disjoint subsets?              │
       └──┬─────────────────────────┬───┘
          no                        yes
          │                         └────► SPLIT
          ▼                                Methods that share no state
       ┌────────────────────────────────┐  belong in different modules.
       │ Q3. Does the module suffer     │
       │ Divergent Change (gets edited  │
       │ for many unrelated reasons)?   │
       └──┬─────────────────────────┬───┘
          no                        yes
          │                         └────► SPLIT (along axis of change)
          ▼                                One reason to change per module.
       ┌────────────────────────────────┐
       │ Q4. Is it >200 lines AND       │
       │ uncohesive (not all the same   │
       │ abstraction level)?            │
       └──┬─────────────────────────┬───┘
          no                        yes
          │                         └────► CONSIDER Extract Class
          ▼                                Only if a real concept emerges.
       ┌────────────────────────────────┐    Otherwise leave alone.
       │ Q5. >200 lines BUT cohesive,   │
       │ linear, same abstraction level │
       │ (a long recipe)?               │
       └──┬─────────────────────────┬───┘
          no                        yes
          │                         └────► KEEP
          ▼                                Length alone is not the smell.
       NO ACTION NEEDED                   Carmack-style coherent functions
                                          are fine.
```

The smell is mixed concerns or divergent change — not raw line count.

---

## Tree 4 — Is this the right seam?

```
                         start
                           │
                           ▼
       ┌──────────────────────────────────────┐
       │ Q1. Can I replace this boundary with │
       │ a test double or alternate impl      │
       │ WITHOUT editing the code on either   │
       │ side?                                │
       └──┬─────────────────────────┬─────────┘
          yes                       no
          │                         └────► NOT YET A SEAM
          ▼                                Refactor first to introduce a seam.
       ┌────────────────────────────────┐
       │ Q2. Would the two sides evolve │
       │ for different reasons (i.e. is │
       │ there real evolutionary        │
       │ independence)?                 │
       └──┬─────────────────────────┬───┘
          yes                       no
          │                         └────► ARTIFICIAL SEAM
          ▼                                The boundary doesn't match
       ┌────────────────────────────────┐  the real change axis. Reconsider.
       │ Q3. Does the interface have    │
       │ ≤ ~5 methods, each carrying    │
       │ real semantics?                │
       └──┬─────────────────────────┬───┘
          yes                       no
          │                         └────► NARROW IT
          ▼                                Big interfaces = weak abstractions.
       ┌────────────────────────────────┐  Push back, reshape.
       │ Q4. Are the leaks (timing,     │
       │ error semantics, resource      │
       │ ownership) DOCUMENTED and      │
       │ predictable?                   │
       └──┬─────────────────────────┬───┘
          yes                       no
          │                         └────► DOCUMENT THEM FIRST
          ▼                                Hidden leaks bite later.
       GOOD SEAM.
```

A real seam: replaceable, narrow, evolutionarily independent, with documented leaks.

---

## Tree 5 — Should I generalize this (add a parameter / type parameter)?

```
                         start
                           │
                           ▼
       ┌──────────────────────────────────────┐
       │ Q1. Do I have THREE concrete uses    │
       │ that all want this parameter set     │
       │ differently?                         │
       └──┬─────────────────────────┬─────────┘
          yes                       no (1 or 2 uses)
          │                         └────► HARDCODE
          ▼                                Until the third use appears,
       ┌────────────────────────────────┐  the variation is imaginary.
       │ Q2. Are the three uses really  │
       │ on the same axis, or are they  │
       │ accidental coincidences in     │
       │ shape?                         │
       └──┬─────────────────────────┬───┘
          same axis                 coincidence
          │                         └────► KEEP SEPARATE
          ▼                                "Same shape" ≠ "same concept".
       ┌────────────────────────────────┐
       │ Q3. Does the generalization    │
       │ make the code easier to read,  │
       │ or just shorter?               │
       └──┬─────────────────────────┬───┘
          easier to read            just shorter
          │                         └────► HARDCODE
          ▼                                Brevity isn't readability.
       GENERALIZE.
```

---

## Meta-rule

The defaults all point one way: **don't extract, don't add the layer, don't generalize, don't widen the seam, don't fuse modules** — until the evidence is overwhelming. The asymmetry is real: the cost of leaving things concrete is small and easily reversed; the cost of premature abstraction is permanent and viral.

When in doubt, **stay concrete**. Wait for the third caller. Wait for the second implementation. Wait for the divergent change. Then act, with high confidence, on real signal — not on the imagined needs of a hypothetical future.
