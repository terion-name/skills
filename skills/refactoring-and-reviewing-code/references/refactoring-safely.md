# Refactoring safely — seams, characterization tests, and tiny steps

Refactoring without tests is editing without a safety net. Most code in the wild has no tests for the part you are about to change — Michael Feathers's working definition: **legacy code is code without tests**. This reference gives you the techniques to refactor legacy code without breaking it.

## The legacy code dilemma

To safely change code you need tests. To write tests you usually need to change the code so it can be tested. The way out is to find a **seam**: a point where you can alter behavior without editing at that place.

## Seams (Feathers)

A seam is anywhere program behavior can be substituted without modifying the surrounding code. There are three kinds, listed from easiest to hardest:

### Object seam (most common in OO languages)

A method call resolves through polymorphism. You can substitute by passing a different object.

```ts
class OrderService {
  constructor(private gateway: PaymentGateway) {}    // ← object seam
  charge(order: Order) { return this.gateway.charge(order.amount); }
}

// In tests, pass a fake gateway. No edits to OrderService.
const fakeGateway = { charge: async () => ({ ok: true }) };
const svc = new OrderService(fakeGateway);
```

If `OrderService` were instantiating `PaymentGateway` itself, you could not substitute — extract the dependency to the constructor first (preparatory refactor; see "Sprout/Wrap" below).

### Link seam

The thing being called is resolved at link/import time, not class-construction time. Test by linking a different implementation.

- **Python:** monkey-patch a module attribute, or use `unittest.mock.patch`.
- **Go:** package-level function variable that tests can reassign:
  ```go
  var now = time.Now    // production
  // in test: now = func() time.Time { return fixed }
  ```
- **TypeScript / JS:** depends on bundler; module mocking via `jest.mock` / `vi.mock`.
- **C#:** harder — usually requires extract-interface first.

Link seams are powerful but globally scoped — restore them in test teardown.

### Preprocessing seam (rare; C/C++)

`#define` or build-time substitution. Not relevant in most modern languages.

## Characterization tests

Before changing legacy code, **pin its current behavior**, including bugs. The goal is not to test what the code *should* do — it is to test what it *currently* does, so any behavior change you make is detected.

### How to write one

1. Call the function with concrete inputs.
2. Assert against whatever it returns / outputs / mutates.
3. If the output is wrong (the code has bugs), test the wrong output anyway. Add a `// TODO: this is buggy, see ticket #123` comment.
4. Lock in the current behavior; fix the bugs in a separate commit *after* the refactor.

```ts
test("calculateTax characterization — current behavior, bugs included", () => {
  // current code returns 0 for amounts < 100, even though it shouldn't
  expect(calculateTax({ amount: 50, region: "US" })).toBe(0);
  // and treats US-CA the same as US — separately tracked bug
  expect(calculateTax({ amount: 1000, region: "US" })).toBe(100);
  expect(calculateTax({ amount: 1000, region: "US-CA" })).toBe(100);
});
```

### Approval / snapshot tests

For functions with complex output (HTML, JSON, log lines), use snapshot testing:

```ts
test("renderInvoice — current output", () => {
  const out = renderInvoice(sampleInvoice);
  expect(out).toMatchSnapshot();
});
```

Run once, inspect the snapshot, commit. Subsequent runs alert you to any change.

### Higher-level characterization

If the unit you want to refactor has no usable seam, write a test at a higher boundary:

- HTTP-level: hit the endpoint, assert on the JSON response.
- Process-level: run the binary with input, snapshot stdout.
- Log-level: capture log output, snapshot the sequence.

You may not be able to carve unit tests around bad code. A characterization test at the integration level is much better than no test.

## Sprout method / Sprout class

Add new functionality as a *new* method or class, called from the legacy code in a single, minimal place. Leave the legacy code alone.

```ts
// Legacy function — long, untested, you need to add a discount calculation
function processOrder(order: Order) {
  // 200 lines of legacy logic
  const total = computeTotal(order);
  const discounted = applyNewDiscountPolicy(order, total);   // ← sprouted
  // 50 more lines
}

// New function — fully tested in isolation
export function applyNewDiscountPolicy(order: Order, total: number): number {
  // …new logic, with tests
}
```

The sprouted function has tests; the legacy code is touched in one place. You contained the change.

## Wrap method / Wrap class

Rename the legacy method, then create a new method with the old name that delegates to the renamed one and adds the new behavior.

```ts
// Before
class OrderService {
  placeOrder(order: Order) { /* legacy */ }
}

// After (wrap)
class OrderService {
  private placeOrderLegacy(order: Order) { /* legacy, untouched */ }

  placeOrder(order: Order) {
    this.placeOrderLegacy(order);
    this.notifyAnalytics(order);     // new behavior
  }

  private notifyAnalytics(order: Order) { /* tested in isolation */ }
}
```

Used when you cannot easily call new code from inside legacy code.

## The legacy code change loop

Feathers's algorithm:

1. **Identify change points.** Where do you actually need to modify behavior?
2. **Find test points.** Where can you assert on the current behavior?
3. **Break dependencies.** Find seams; extract dependencies to constructor parameters; introduce link seams. Use safe automated refactorings (rename, extract method) — these are mechanical and unlikely to break behavior.
4. **Write characterization tests.** Pin current behavior at the test point.
5. **Make changes.** Now you can refactor and add behavior with confidence.
6. **Refactor for cleanliness.** Once tests are in place, the rest of the cleanup is normal refactoring.

## Safe automated refactorings

These are almost always safe to perform via IDE refactoring tools, even without tests:

- **Rename** (variable, function, class, file) — IDE updates all references.
- **Extract method** (with no shared mutable state in the extracted body).
- **Extract variable**.
- **Inline variable** (not always — careful with side-effecting expressions).
- **Move method/file** within a module — IDE updates imports.

Use these to **break dependencies** before you have tests. They are how you create seams.

## Unsafe-without-tests refactorings

Do not perform these without tests:

- Anything that changes call order.
- Anything that combines or splits state.
- Anything that changes error handling.
- Inlining a method that is called from many places (unless you can read every caller).
- Changing a public method's signature.

## Language-specific seams

### TypeScript

- Constructor injection (object seam).
- Module-level function exports + `vi.mock` / `jest.mock` (link seam).
- Default parameters that accept a callable: `function f(now = Date.now) { … }`.

### Python

- Constructor injection.
- Module-level functions + `monkeypatch.setattr` in pytest.
- `unittest.mock.patch` decorator.
- `Protocol` types let you accept any structurally-matching object.

### C#

- Constructor injection (the dominant pattern; usually requires extracting an interface first).
- Virtual methods (override in test subclass).
- `internal` types + `InternalsVisibleTo("Tests")`.

### Go

- Accept an interface where you currently use a concrete type.
- Package-level function variable for things like `time.Now` you want to override in tests.

## A worked example: untangling `calculateTax`

You have:

```ts
// 200 lines of code, no tests, mixed concerns, called from many places
export function calculateTax(order: any): number {
  // database lookups, hardcoded rates, regional rules, currency conversion,
  // logging, audit writes — all in one function
}
```

You need to add a new tax rule. The right path:

1. **Capture current behavior at the integration level.** Pick 10 representative orders from production logs; run them through the function; snapshot the outputs.
   ```ts
   test("calculateTax characterization", () => {
     for (const sample of samples) {
       expect(calculateTax(sample.input)).toBe(sample.expectedTax);
     }
   });
   ```
2. **Sprout the new rule** as a separate function with its own unit tests.
3. **Call the sprouted function** from `calculateTax` in one place.
4. Re-run the characterization test. If it passes, the change preserved behavior on the captured samples.
5. Now, with tests in place, refactor `calculateTax` itself: extract regional rules into named functions, push the database lookups out, separate concerns. Each refactor commits separately, all keep characterization tests green.
6. Eventually, the original function is decomposed and the characterization tests are replaced with focused unit tests on the extracted pieces. Then the characterization tests can be retired.

This is the slow, safe path. It is much faster than the alternative — making a change, breaking production, debugging the regression, re-shipping.

## Quick checklist before any refactor

- [ ] Are there tests for the code I am about to change?
- [ ] If not, can I find a seam to write tests through?
- [ ] If not, can I write a higher-level characterization test?
- [ ] Have I committed the test on its own (separate from the refactor)?
- [ ] Will my refactor be a sequence of small commits, each green?
- [ ] Have I separated structure from behavior?
