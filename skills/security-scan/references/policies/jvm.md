# Policy: JVM (Java / Kotlin / Scala)

Read alongside `web-and-api.md`. The JVM's historical hotspots are deserialization, XXE, and reflection/
expression-language injection — all RCE-grade.

## Insecure deserialization (top JVM RCE)

**Rule:** never deserialize untrusted bytes with native Java serialization.

Grep: `ObjectInputStream.readObject`, `XMLDecoder`, `readUnshared`, frameworks that auto-deserialize
(unsafe Jackson `enableDefaultTyping`/`@JsonTypeInfo` with polymorphic types, `XStream`, `Kryo`, `SnakeYAML`
`Yaml().load` without a safe constructor, Apache Commons-Collections gadgets). Fix: don't accept serialized
objects from clients; JSON with disabled polymorphic typing; SnakeYAML `SafeConstructor`; serialization
filters (`ObjectInputFilter`) if unavoidable.

## XXE (XML external entities)

**Rule:** disable DTDs and external entities on every XML parser.

Grep: `DocumentBuilderFactory`, `SAXParserFactory`, `XMLInputFactory`, `TransformerFactory`, `SAXReader`,
`Unmarshaller` without hardening. Fix: `setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)`
(and disable external general/parameter entities); set `XMLConstants.FEATURE_SECURE_PROCESSING`. XXE →
file read / SSRF / DoS (billion-laughs).

## Expression-language / template / reflection injection

`Runtime.exec`/`ProcessBuilder` with a shell string; EL/OGNL/SpEL/MVEL evaluating user input (the Struts/
Spring RCE class) — `SpelExpressionParser().parseExpression(userInput)`; reflection driven by user input
(`Class.forName(userInput)`, `Method.invoke`); ScriptEngine (`eval`) on user input; Velocity/Freemarker/
Thymeleaf templates from user source (SSTI).

## Injection & web

- **SQL:** string-built JDBC/JPQL/HQL → `PreparedStatement` with bound params / criteria API; `@Query`
  with concatenation in Spring Data → parameterized.
- **Path traversal / Zip Slip:** `new File(base, userInput)`, `Files.newInputStream`, `ZipEntry.getName()`
  extraction → canonicalize and verify containment.
- **SSRF:** `URL.openConnection`/`HttpClient`/`RestTemplate`/`WebClient` with user URLs.
- **Spring specifics:** missing method security (`@PreAuthorize`), `permitAll` on sensitive routes,
  Actuator endpoints exposed (`/env`, `/heapdump`, `/jolokia` → RCE), mass binding via `@ModelAttribute`
  without `@InitBinder` allowlist, `@CrossOrigin("*")`, disabled CSRF on cookie-auth flows.

## Crypto & randomness

`java.util.Random`/`Math.random` for tokens → `SecureRandom`. `MessageDigest` MD5/SHA-1 for passwords →
`BCrypt`/`Argon2`/PBKDF2. `Cipher.getInstance("AES")` defaults to ECB → use AES/GCM with a random IV/nonce.
Non-constant-time comparison (`String.equals`/`Arrays.equals`) for MACs → `MessageDigest.isEqual`.
`TrustManager` that accepts all certs / `HostnameVerifier` returning true → TLS bypass. Hardcoded keys.

## Other

`assert` for security (disabled unless `-ea`); secrets in logs / exceptions / stack traces returned to
clients; `System.getenv`/property secrets logged; unbounded request/upload sizes (DoS); ReDoS in
`Pattern`. Kotlin: `!!` masking nullability bugs; runtime validation still required on external input.

## Tools

OWASP Dependency-Check (`mvn ... dependency-check` / `gradle dependencyCheckAnalyze`) or `osv-scanner` for
CVE deps; `semgrep --config p/java`; SpotBugs + FindSecBugs if the project builds. Confirm hits against code.
