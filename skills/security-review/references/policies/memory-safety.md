# Policy: memory safety (C / C++ / unsafe Rust / FFI / cgo)

Applies to native code and to `unsafe`/FFI boundaries in otherwise-safe languages. Memory-safety bugs are
frequently exploitable for RCE, so default to high severity when an attacker controls the input that
reaches the unsafe operation. Validate with sanitizers (`-fsanitize=address,undefined`) and, for parsers,
a short fuzzing run — a sanitizer crash on attacker-controlled input is strong evidence.

## Buffer / stack / heap overflow (out-of-bounds write/read)

**Rule:** every buffer write must be bounded by the destination size, not the source length.

Grep: `strcpy`, `strcat`, `sprintf`, `gets`, `scanf("%s")`, `memcpy`/`memmove` with a length derived from
input, `alloca` with an input-sized argument, array indexing with an unchecked index, pointer arithmetic
on attacker-influenced offsets. Fix: bounded variants (`strncpy`/`snprintf` with correct sizes,
`strlcpy`/`strlcat`), explicit length checks, container types (`std::vector`/`std::string`,
`std::span` for bounds). In Rust, OOB is normally impossible in safe code — scrutinize `get_unchecked`,
raw-pointer deref, and `slice::from_raw_parts` with computed lengths.

## Integer overflow / truncation → undersized allocation

**Rule:** validate arithmetic that feeds an allocation size or a loop/index bound.

Grep: `malloc(n * size)` / `new T[n]` where `n` is input; `size_t`↔`int` casts; subtraction that can wrap
(`len - header_len`); `length` fields read from a file/packet. An overflowed size → small allocation →
subsequent write overflows the heap. Fix: checked arithmetic (`__builtin_*_overflow`, `checked_mul` /
`checked_add` in Rust), reject implausible sizes, use types wide enough for the domain.

## Use-after-free / double-free / dangling pointers

**Rule:** ownership and lifetime must be unambiguous; never use a pointer after `free`/`delete`/move.

Grep: `free(p)` followed by any use of `p`; returning addresses of locals; storing raw pointers into
long-lived structures; manual `delete` mixed with smart pointers; iterator invalidation after container
mutation; callback/closure capturing a freed object. Fix: RAII + smart pointers (`unique_ptr`/`shared_ptr`),
null after free, ownership discipline; in Rust trust the borrow checker but audit `unsafe` lifetime
extensions and `transmute`. UAF is a top RCE primitive — rate accordingly when attacker-triggerable.

## Format-string vulnerabilities

**Rule:** the format string is always a literal; user data is an argument.

Grep: `printf(userInput)`, `fprintf(f, userInput)`, `syslog(prio, userInput)`, `*.Sprintf` patterns where
the format comes from input. `%n` enables arbitrary write. Fix: `printf("%s", userInput)`.

## Off-by-one, OOB read, info leak

Loop bounds (`<=` vs `<`), null-terminator space, reading past a length field. OOB reads leak memory
(keys, ASLR-defeating pointers) — see Heartbleed. Validate lengths against the actual buffer, not the
claimed length.

## Type confusion / uninitialized memory / unchecked casts

Unions and `reinterpret_cast`/`transmute` interpreting bytes as the wrong type; reading uninitialized
stack/heap; C `void*` round-trips; deserializing into a type without validating a tag. Fix: tagged unions,
zero-initialize, validate discriminators before casting.

## Concurrency memory bugs

Data races on shared memory (TOCTOU on buffers, racy `len`/`ptr` updates) can corrupt memory. Run under
TSan. In Rust, audit `Send`/`Sync` impls and `unsafe` shared-state code.

## FFI / cgo / boundary issues

At any managed↔native boundary: validate that lengths/pointers passed across are correct and that the
native side can't write past what the managed side allocated; check string null-termination assumptions;
ensure errors don't leave half-initialized memory exposed. Treat the boundary as a trust seam.

## Validation notes

- Build with `-fsanitize=address,undefined` (and `-fsanitize=thread` for races); reproduce the crash on a
  PoC input; capture the ASan/UBSan report as evidence (the offending op, the access size, the stack).
- If you can't compile (no toolchain), validate by code review tracing the input-to-write path, and record
  the missing-dynamic-repro blindspot.
- Mitigations like ASLR/stack canaries/NX reduce exploitability but don't make the bug not-a-bug; note them
  when calibrating likelihood, not when deciding whether to report.
