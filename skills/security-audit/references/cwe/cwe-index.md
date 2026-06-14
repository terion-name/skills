# CWE Reference Catalog

Generated for the security-audit skill. Use `cwe-catalog.jsonl` as the structured source of truth and `cwe-labels.json` for filename tags.

- Source: `https://cwe.mitre.org/data/xml/cwec_latest.xml.zip#cwec_v4.20.xml`
- Schema: `https://cwe.mitre.org/data/xsd/cwe_schema_latest.xsd`
- Catalog: CWE
- Version/date: 4.20 / 2026-04-30
- Generated: 2026-06-14T08:08:18Z
- Entries: 1391 (969 weaknesses, 422 categories)

## Report Usage

For every validated, likely, or unvalidated finding, choose the closest CWE weakness and include:

```
CWE: CWE-22 - Path Traversal
CWE description: Improper limitation of a pathname to a restricted directory allows traversal outside the intended root.
CWE mapping: primary; the source accepts a user-controlled path and the sink resolves it without a containment check.
Standards: CWE-22, <other mappings>
```

Use `filename_tag` for report filenames, e.g. `SEC-001-[HIGH]-[CWE-22-path-traversal]-arbitrary-file-read.md`.

## Index

| CWE | Kind | Abstraction | Short label | Name | Filename tag |
|-----|------|-------------|-------------|------|--------------|
| CWE-1 | category |  | DEPRECATED: Location | DEPRECATED: Location | CWE-1-deprecated-location |
| CWE-2 | category |  | 7PK - Environment | 7PK - Environment | CWE-2-7pk-environment |
| CWE-3 | category |  | DEPRECATED: Technology-specific Environment Issues | DEPRECATED: Technology-specific Environment Issues | CWE-3-deprecated-technology-specific-environment-issues |
| CWE-4 | category |  | DEPRECATED: J2EE Environment Issues | DEPRECATED: J2EE Environment Issues | CWE-4-deprecated-j2ee-environment-issues |
| CWE-5 | weakness | Variant | J2EE Misconfiguration: Insecure Transport | J2EE Misconfiguration: Data Transmission Without Encryption | CWE-5-j2ee-misconfiguration-insecure-transport |
| CWE-6 | weakness | Variant | J2EE Misconfiguration: Insufficient Session-ID Length | J2EE Misconfiguration: Insufficient Session-ID Length | CWE-6-j2ee-misconfiguration-insufficient-session-id-length |
| CWE-7 | weakness | Variant | J2EE Misconfiguration: Missing Error Handling | J2EE Misconfiguration: Missing Custom Error Page | CWE-7-j2ee-misconfiguration-missing-error-handling |
| CWE-8 | weakness | Variant | J2EE Misconfiguration: Unsafe Bean Declaration | J2EE Misconfiguration: Entity Bean Declared Remote | CWE-8-j2ee-misconfiguration-unsafe-bean-declaration |
| CWE-9 | weakness | Variant | J2EE Misconfiguration: Weak Access Permissions | J2EE Misconfiguration: Weak Access Permissions for EJB Methods | CWE-9-j2ee-misconfiguration-weak-access-permissions |
| CWE-10 | category |  | DEPRECATED: ASP.NET Environment Issues | DEPRECATED: ASP.NET Environment Issues | CWE-10-deprecated-asp-net-environment-issues |
| CWE-11 | weakness | Variant | ASP.NET Misconfiguration: Creating Debug Binary | ASP.NET Misconfiguration: Creating Debug Binary | CWE-11-asp-net-misconfiguration-creating-debug-binary |
| CWE-12 | weakness | Variant | ASP.NET Misconfiguration: Missing Custom Error Handling | ASP.NET Misconfiguration: Missing Custom Error Page | CWE-12-asp-net-misconfiguration-missing-custom-error-handling |
| CWE-13 | weakness | Variant | ASP.NET Misconfiguration: Password in Configuration File | ASP.NET Misconfiguration: Password in Configuration File | CWE-13-asp-net-misconfiguration-password-in-configuration-file |
| CWE-14 | weakness | Variant | Sensitive memory uncleared by compiler optimization | Compiler Removal of Code to Clear Buffers | CWE-14-sensitive-memory-uncleared-by-compiler-optimization |
| CWE-15 | weakness | Base | Setting Manipulation | External Control of System or Configuration Setting | CWE-15-setting-manipulation |
| CWE-16 | category |  | Server Misconfiguration | Configuration | CWE-16-server-misconfiguration |
| CWE-17 | category |  | DEPRECATED: Code | DEPRECATED: Code | CWE-17-deprecated-code |
| CWE-18 | category |  | DEPRECATED: Source Code | DEPRECATED: Source Code | CWE-18-deprecated-source-code |
| CWE-19 | category |  | Data Processing Errors | Data Processing Errors | CWE-19-data-processing-errors |
| CWE-20 | weakness | Class | Improper Input Handling | Improper Input Validation | CWE-20-improper-input-handling |
| CWE-21 | category |  | DEPRECATED: Pathname Traversal and Equivalence Errors | DEPRECATED: Pathname Traversal and Equivalence Errors | CWE-21-deprecated-pathname-traversal-and-equivalence-errors |
| CWE-22 | weakness | Base | Path Traversal | Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') | CWE-22-path-traversal |
| CWE-23 | weakness | Base | Relative Path Traversal | Relative Path Traversal | CWE-23-relative-path-traversal |
| CWE-24 | weakness | Variant | '../filedir | Path Traversal: '../filedir' | CWE-24-filedir |
| CWE-25 | weakness | Variant | '/../filedir | Path Traversal: '/../filedir' | CWE-25-filedir |
| CWE-26 | weakness | Variant | '/directory/../filename | Path Traversal: '/dir/../filename' | CWE-26-directory-filename |
| CWE-27 | weakness | Variant | 'directory/../../filename | Path Traversal: 'dir/../../filename' | CWE-27-directory-filename |
| CWE-28 | weakness | Variant | '..\filename' ('dot dot backslash') | Path Traversal: '..\filedir' | CWE-28-filename-dot-dot-backslash |
| CWE-29 | weakness | Variant | '\..\filename' ('leading dot dot backslash') | Path Traversal: '\..\filename' | CWE-29-filename-leading-dot-dot-backslash |
| CWE-30 | weakness | Variant | 7 - '\directory\..\filename | Path Traversal: '\dir\..\filename' | CWE-30-7-directory-filename |
| CWE-31 | weakness | Variant | 8 - 'directory\..\..\filename | Path Traversal: 'dir\..\..\filename' | CWE-31-8-directory-filename |
| CWE-32 | weakness | Variant | '...' (triple dot) | Path Traversal: '...' (Triple Dot) | CWE-32-triple-dot |
| CWE-33 | weakness | Variant | '....' (multiple dot) | Path Traversal: '....' (Multiple Dot) | CWE-33-multiple-dot |
| CWE-34 | weakness | Variant | '....//' (doubled dot dot slash) | Path Traversal: '....//' | CWE-34-doubled-dot-dot-slash |
| CWE-35 | weakness | Variant | '.../...//' | Path Traversal: '.../...//' | CWE-35-cwe |
| CWE-36 | weakness | Base | Absolute Path Traversal | Absolute Path Traversal | CWE-36-absolute-path-traversal |
| CWE-37 | weakness | Variant | /absolute/pathname/here | Path Traversal: '/absolute/pathname/here' | CWE-37-absolute-pathname-here |
| CWE-38 | weakness | Variant | \absolute\pathname\here ('backslash absolute path') | Path Traversal: '\absolute\pathname\here' | CWE-38-absolute-pathname-here-backslash-absolute-path |
| CWE-39 | weakness | Variant | 'C:dirname' or C: (Windows volume or 'drive letter') | Path Traversal: 'C:dirname' | CWE-39-c-dirname-c-windows-volume-drive-letter |
| CWE-40 | weakness | Variant | '\\UNC\share\name\' (Windows UNC share) | Path Traversal: '\\UNC\share\name\' (Windows UNC Share) | CWE-40-unc-share-name-windows-unc-share |
| CWE-41 | weakness | Base | Path Equivalence | Improper Resolution of Path Equivalence | CWE-41-path-equivalence |
| CWE-42 | weakness | Variant | Trailing Dot - 'filedir.' | Path Equivalence: 'filename.' (Trailing Dot) | CWE-42-trailing-dot-filedir |
| CWE-43 | weakness | Variant | Multiple Trailing Dot - 'filedir....' | Path Equivalence: 'filename....' (Multiple Trailing Dot) | CWE-43-multiple-trailing-dot-filedir |
| CWE-44 | weakness | Variant | Internal Dot - 'file.ordir' | Path Equivalence: 'file.name' (Internal Dot) | CWE-44-internal-dot-file-ordir |
| CWE-45 | weakness | Variant | Multiple Internal Dot - 'file...dir' | Path Equivalence: 'file...name' (Multiple Internal Dot) | CWE-45-multiple-internal-dot-file-dir |
| CWE-46 | weakness | Variant | Trailing Space - 'filedir ' | Path Equivalence: 'filename ' (Trailing Space) | CWE-46-trailing-space-filedir |
| CWE-47 | weakness | Variant | Leading Space - ' filedir' | Path Equivalence: ' filename' (Leading Space) | CWE-47-leading-space-filedir |
| CWE-48 | weakness | Variant | file(SPACE)name (internal space) | Path Equivalence: 'file name' (Internal Whitespace) | CWE-48-file-space-name-internal-space |
| CWE-49 | weakness | Variant | filedir/ (trailing slash, trailing /) | Path Equivalence: 'filename/' (Trailing Slash) | CWE-49-filedir-trailing-slash-trailing |
| CWE-50 | weakness | Variant | //multiple/leading/slash ('multiple leading slash') | Path Equivalence: '//multiple/leading/slash' | CWE-50-multiple-leading-slash-multiple-leading-slash |
| CWE-51 | weakness | Variant | /multiple//internal/slash ('multiple internal slash') | Path Equivalence: '/multiple//internal/slash' | CWE-51-multiple-internal-slash-multiple-internal-slash |
| CWE-52 | weakness | Variant | /multiple/trailing/slash// ('multiple trailing slash') | Path Equivalence: '/multiple/trailing/slash//' | CWE-52-multiple-trailing-slash-multiple-trailing-slash |
| CWE-53 | weakness | Variant | \multiple\\internal\backslash | Path Equivalence: '\multiple\\internal\backslash' | CWE-53-multiple-internal-backslash |
| CWE-54 | weakness | Variant | filedir\ (trailing backslash) | Path Equivalence: 'filedir\' (Trailing Backslash) | CWE-54-filedir-trailing-backslash |
| CWE-55 | weakness | Variant | /./ (single dot directory) | Path Equivalence: '/./' (Single Dot Directory) | CWE-55-single-dot-directory |
| CWE-56 | weakness | Variant | filedir* (asterisk / wildcard) | Path Equivalence: 'filedir*' (Wildcard) | CWE-56-filedir-asterisk-wildcard |
| CWE-57 | weakness | Variant | dirname/fakechild/../realchild/filename | Path Equivalence: 'fakedir/../realdir/filename' | CWE-57-dirname-fakechild-realchild-filename |
| CWE-58 | weakness | Variant | Windows 8.3 Filename | Path Equivalence: Windows 8.3 Filename | CWE-58-windows-8-3-filename |
| CWE-59 | weakness | Base | Link Following | Improper Link Resolution Before File Access ('Link Following') | CWE-59-link-following |
| CWE-60 | category |  | DEPRECATED: UNIX Path Link Problems | DEPRECATED: UNIX Path Link Problems | CWE-60-deprecated-unix-path-link-problems |
| CWE-61 | weakness | Compound | UNIX symbolic link following | UNIX Symbolic Link (Symlink) Following | CWE-61-unix-symbolic-link-following |
| CWE-62 | weakness | Variant | UNIX hard link | UNIX Hard Link | CWE-62-unix-hard-link |
| CWE-63 | category |  | DEPRECATED: Windows Path Link Problems | DEPRECATED: Windows Path Link Problems | CWE-63-deprecated-windows-path-link-problems |
| CWE-64 | weakness | Variant | Windows Shortcut Following (.LNK) | Windows Shortcut Following (.LNK) | CWE-64-windows-shortcut-following-lnk |
| CWE-65 | weakness | Variant | Windows hard link | Windows Hard Link | CWE-65-windows-hard-link |
| CWE-66 | weakness | Base | Virtual Files | Improper Handling of File Names that Identify Virtual Resources | CWE-66-virtual-files |
| CWE-67 | weakness | Variant | Windows MS-DOS device names | Improper Handling of Windows Device Names | CWE-67-windows-ms-dos-device-names |
| CWE-68 | category |  | DEPRECATED: Windows Virtual File Problems | DEPRECATED: Windows Virtual File Problems | CWE-68-deprecated-windows-virtual-file-problems |
| CWE-69 | weakness | Variant | Windows ::DATA alternate data stream | Improper Handling of Windows ::DATA Alternate Data Stream | CWE-69-windows-data-alternate-data-stream |
| CWE-70 | category |  | DEPRECATED: Mac Virtual File Problems | DEPRECATED: Mac Virtual File Problems | CWE-70-deprecated-mac-virtual-file-problems |
| CWE-71 | weakness | Variant | DEPRECATED: Apple '.DS_Store' | DEPRECATED: Apple '.DS_Store' | CWE-71-deprecated-apple-ds-store |
| CWE-72 | weakness | Variant | Improper Handling of Apple HFS+ Alternate Data Stream Path | Improper Handling of Apple HFS+ Alternate Data Stream Path | CWE-72-improper-handling-apple-hfs-alternate-data-stream-path |
| CWE-73 | weakness | Base | Path Manipulation | External Control of File Name or Path | CWE-73-path-manipulation |
| CWE-74 | weakness | Class | Injection problem ('data' used as something else) | Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') | CWE-74-injection-problem-data-used-as-something-else |
| CWE-75 | weakness | Class | Special Element Injection | Failure to Sanitize Special Elements into a Different Plane (Special Element Injection) | CWE-75-special-element-injection |
| CWE-76 | weakness | Base | Equivalent Special Element Injection | Improper Neutralization of Equivalent Special Elements | CWE-76-equivalent-special-element-injection |
| CWE-77 | weakness | Class | Command Injection | Improper Neutralization of Special Elements used in a Command ('Command Injection') | CWE-77-command-injection |
| CWE-78 | weakness | Base | OS Command Injection | Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') | CWE-78-os-command-injection |
| CWE-79 | weakness | Base | Cross-site scripting (XSS) | Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') | CWE-79-cross-site-scripting-xss |
| CWE-80 | weakness | Variant | Basic XSS | Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS) | CWE-80-basic-xss |
| CWE-81 | weakness | Variant | XSS in error pages | Improper Neutralization of Script in an Error Message Web Page | CWE-81-xss-in-error-pages |
| CWE-82 | weakness | Variant | Script in IMG tags | Improper Neutralization of Script in Attributes of IMG Tags in a Web Page | CWE-82-script-in-img-tags |
| CWE-83 | weakness | Variant | XSS using Script in Attributes | Improper Neutralization of Script in Attributes in a Web Page | CWE-83-xss-using-script-in-attributes |
| CWE-84 | weakness | Variant | XSS using Script Via Encoded URI Schemes | Improper Neutralization of Encoded URI Schemes in a Web Page | CWE-84-xss-using-script-via-encoded-uri-schemes |
| CWE-85 | weakness | Variant | DOUBLE - Doubled character XSS manipulations, e.g. "<script" | Doubled Character XSS Manipulations | CWE-85-double-doubled-character-xss-manipulations-e-g-script |
| CWE-86 | weakness | Variant | Invalid Characters in Identifiers | Improper Neutralization of Invalid Characters in Identifiers in Web Pages | CWE-86-invalid-characters-in-identifiers |
| CWE-87 | weakness | Variant | Alternate XSS syntax | Improper Neutralization of Alternate XSS Syntax | CWE-87-alternate-xss-syntax |
| CWE-88 | weakness | Base | Argument Injection or Modification | Improper Neutralization of Argument Delimiters in a Command ('Argument Injection') | CWE-88-argument-injection-or-modification |
| CWE-89 | weakness | Base | SQL injection | Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') | CWE-89-sql-injection |
| CWE-90 | weakness | Base | LDAP injection | Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection') | CWE-90-ldap-injection |
| CWE-91 | weakness | Base | XML injection (aka Blind Xpath injection) | XML Injection (aka Blind XPath Injection) | CWE-91-xml-injection-aka-blind-xpath-injection |
| CWE-92 | weakness | Base | DEPRECATED: Improper Sanitization of Custom Special Characters | DEPRECATED: Improper Sanitization of Custom Special Characters | CWE-92-deprecated-improper-sanitization-of-custom-special |
| CWE-93 | weakness | Base | CRLF Injection | Improper Neutralization of CRLF Sequences ('CRLF Injection') | CWE-93-crlf-injection |
| CWE-94 | weakness | Base | Code Evaluation and Injection | Improper Control of Generation of Code ('Code Injection') | CWE-94-code-evaluation-and-injection |
| CWE-95 | weakness | Variant | Direct Dynamic Code Evaluation ('Eval Injection') | Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection') | CWE-95-direct-dynamic-code-evaluation-eval-injection |
| CWE-96 | weakness | Base | Direct Static Code Injection | Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection') | CWE-96-direct-static-code-injection |
| CWE-97 | weakness | Variant | Server-Side Includes (SSI) Injection | Improper Neutralization of Server-Side Includes (SSI) Within a Web Page | CWE-97-server-side-includes-ssi-injection |
| CWE-98 | weakness | Variant | PHP File Include | Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') | CWE-98-php-file-include |
| CWE-99 | weakness | Class | Resource Injection | Improper Control of Resource Identifiers ('Resource Injection') | CWE-99-resource-injection |
| CWE-100 | category |  | DEPRECATED: Technology-Specific Input Validation Problems | DEPRECATED: Technology-Specific Input Validation Problems | CWE-100-deprecated-technology-specific-input-validation-problems |
| CWE-101 | category |  | DEPRECATED: Struts Validation Problems | DEPRECATED: Struts Validation Problems | CWE-101-deprecated-struts-validation-problems |
| CWE-102 | weakness | Variant | Struts: Duplicate Validation Forms | Struts: Duplicate Validation Forms | CWE-102-struts-duplicate-validation-forms |
| CWE-103 | weakness | Variant | Struts: Erroneous validate() Method | Struts: Incomplete validate() Method Definition | CWE-103-struts-erroneous-validate-method |
| CWE-104 | weakness | Variant | Struts: Form Bean Does Not Extend Validation Class | Struts: Form Bean Does Not Extend Validation Class | CWE-104-struts-form-bean-does-not-extend-validation-class |
| CWE-105 | weakness | Variant | Struts: Form Field Without Validator | Struts: Form Field Without Validator | CWE-105-struts-form-field-without-validator |
| CWE-106 | weakness | Variant | Struts: Plug-in Framework Not In Use | Struts: Plug-in Framework not in Use | CWE-106-struts-plug-in-framework-not-in-use |
| CWE-107 | weakness | Variant | Struts: Unused Validation Form | Struts: Unused Validation Form | CWE-107-struts-unused-validation-form |
| CWE-108 | weakness | Variant | Struts: Unvalidated Action Form | Struts: Unvalidated Action Form | CWE-108-struts-unvalidated-action-form |
| CWE-109 | weakness | Variant | Struts: Validator Turned Off | Struts: Validator Turned Off | CWE-109-struts-validator-turned-off |
| CWE-110 | weakness | Variant | Struts: Validator Without Form Field | Struts: Validator Without Form Field | CWE-110-struts-validator-without-form-field |
| CWE-111 | weakness | Variant | Unsafe JNI | Direct Use of Unsafe JNI | CWE-111-unsafe-jni |
| CWE-112 | weakness | Base | Missing XML Validation | Missing XML Validation | CWE-112-missing-xml-validation |
| CWE-113 | weakness | Variant | HTTP response splitting | Improper Neutralization of CRLF Sequences in HTTP Headers ('HTTP Request/Response Splitting') | CWE-113-http-response-splitting |
| CWE-114 | weakness | Class | Process Control | Process Control | CWE-114-process-control |
| CWE-115 | weakness | Base | Misinterpretation Error | Misinterpretation of Input | CWE-115-misinterpretation-error |
| CWE-116 | weakness | Class | Improper Output Handling | Improper Encoding or Escaping of Output | CWE-116-improper-output-handling |
| CWE-117 | weakness | Base | Log Forging | Improper Output Neutralization for Logs | CWE-117-log-forging |
| CWE-118 | weakness | Class | Range Error | Incorrect Access of Indexable Resource ('Range Error') | CWE-118-range-error |
| CWE-119 | weakness | Class | Buffer Overflow | Improper Restriction of Operations within the Bounds of a Memory Buffer | CWE-119-buffer-overflow |
| CWE-120 | weakness | Base | Unbounded Transfer ('classic overflow') | Buffer Copy without Checking Size of Input ('Classic Buffer Overflow') | CWE-120-unbounded-transfer-classic-overflow |
| CWE-121 | weakness | Variant | Stack overflow | Stack-based Buffer Overflow | CWE-121-stack-overflow |
| CWE-122 | weakness | Variant | Heap overflow | Heap-based Buffer Overflow | CWE-122-heap-overflow |
| CWE-123 | weakness | Base | Write-what-where condition | Write-what-where Condition | CWE-123-write-what-where-condition |
| CWE-124 | weakness | Base | UNDER - Boundary beginning violation ('buffer underflow'?) | Buffer Underwrite ('Buffer Underflow') | CWE-124-under-boundary-beginning-violation-buffer-underflow |
| CWE-125 | weakness | Base | Out-of-bounds Read | Out-of-bounds Read | CWE-125-out-of-bounds-read |
| CWE-126 | weakness | Variant | Buffer over-read | Buffer Over-read | CWE-126-buffer-over-read |
| CWE-127 | weakness | Variant | Buffer under-read | Buffer Under-read | CWE-127-buffer-under-read |
| CWE-128 | weakness | Base | Wrap-around error | Wrap-around Error | CWE-128-wrap-around-error |
| CWE-129 | weakness | Variant | INDEX - Array index overflow | Improper Validation of Array Index | CWE-129-index-array-index-overflow |
| CWE-130 | weakness | Base | Length Parameter Inconsistency | Improper Handling of Length Parameter Inconsistency | CWE-130-length-parameter-inconsistency |
| CWE-131 | weakness | Base | Other length calculation error | Incorrect Calculation of Buffer Size | CWE-131-other-length-calculation-error |
| CWE-132 | weakness | Base | DEPRECATED: Miscalculated Null Termination | DEPRECATED: Miscalculated Null Termination | CWE-132-deprecated-miscalculated-null-termination |
| CWE-133 | category |  | String Errors | String Errors | CWE-133-string-errors |
| CWE-134 | weakness | Base | Format string vulnerability | Use of Externally-Controlled Format String | CWE-134-format-string-vulnerability |
| CWE-135 | weakness | Base | Improper string length checking | Incorrect Calculation of Multi-Byte String Length | CWE-135-improper-string-length-checking |
| CWE-136 | category |  | Type Errors | Type Errors | CWE-136-type-errors |
| CWE-137 | category |  | Data Neutralization Issues | Data Neutralization Issues | CWE-137-data-neutralization-issues |
| CWE-138 | weakness | Class | Special Elements (Characters or Reserved Words) | Improper Neutralization of Special Elements | CWE-138-special-elements-characters-or-reserved-words |
| CWE-139 | category |  | DEPRECATED: General Special Element Problems | DEPRECATED: General Special Element Problems | CWE-139-deprecated-general-special-element-problems |
| CWE-140 | weakness | Base | Delimiter Problems | Improper Neutralization of Delimiters | CWE-140-delimiter-problems |
| CWE-141 | weakness | Variant | Parameter Delimiter | Improper Neutralization of Parameter/Argument Delimiters | CWE-141-parameter-delimiter |
| CWE-142 | weakness | Variant | Value Delimiter | Improper Neutralization of Value Delimiters | CWE-142-value-delimiter |
| CWE-143 | weakness | Variant | Record Delimiter | Improper Neutralization of Record Delimiters | CWE-143-record-delimiter |
| CWE-144 | weakness | Variant | Line Delimiter | Improper Neutralization of Line Delimiters | CWE-144-line-delimiter |
| CWE-145 | weakness | Variant | Section Delimiter | Improper Neutralization of Section Delimiters | CWE-145-section-delimiter |
| CWE-146 | weakness | Variant | Delimiter between Expressions or Commands | Improper Neutralization of Expression/Command Delimiters | CWE-146-delimiter-between-expressions-or-commands |
| CWE-147 | weakness | Variant | Input Terminator | Improper Neutralization of Input Terminators | CWE-147-input-terminator |
| CWE-148 | weakness | Variant | Input Leader | Improper Neutralization of Input Leaders | CWE-148-input-leader |
| CWE-149 | weakness | Variant | Quoting Element | Improper Neutralization of Quoting Syntax | CWE-149-quoting-element |
| CWE-150 | weakness | Variant | Escape, Meta, or Control Character / Sequence | Improper Neutralization of Escape, Meta, or Control Sequences | CWE-150-escape-meta-or-control-character-sequence |
| CWE-151 | weakness | Variant | Comment Element | Improper Neutralization of Comment Delimiters | CWE-151-comment-element |
| CWE-152 | weakness | Variant | Macro Symbol | Improper Neutralization of Macro Symbols | CWE-152-macro-symbol |
| CWE-153 | weakness | Variant | Substitution Character | Improper Neutralization of Substitution Characters | CWE-153-substitution-character |
| CWE-154 | weakness | Variant | Variable Name Delimiter | Improper Neutralization of Variable Name Delimiters | CWE-154-variable-name-delimiter |
| CWE-155 | weakness | Variant | Wildcard or Matching Element | Improper Neutralization of Wildcards or Matching Symbols | CWE-155-wildcard-or-matching-element |
| CWE-156 | weakness | Variant | Whitespace | Improper Neutralization of Whitespace | CWE-156-whitespace |
| CWE-157 | weakness | Variant | Grouping Element / Paired Delimiter | Failure to Sanitize Paired Delimiters | CWE-157-grouping-element-paired-delimiter |
| CWE-158 | weakness | Variant | Null Character / Null Byte | Improper Neutralization of Null Byte or NUL Character | CWE-158-null-character-null-byte |
| CWE-159 | weakness | Class | Common Special Element Manipulations | Improper Handling of Invalid Use of Special Elements | CWE-159-common-special-element-manipulations |
| CWE-160 | weakness | Variant | Leading Special Element | Improper Neutralization of Leading Special Elements | CWE-160-leading-special-element |
| CWE-161 | weakness | Variant | Multiple Leading Special Elements | Improper Neutralization of Multiple Leading Special Elements | CWE-161-multiple-leading-special-elements |
| CWE-162 | weakness | Variant | Trailing Special Element | Improper Neutralization of Trailing Special Elements | CWE-162-trailing-special-element |
| CWE-163 | weakness | Variant | Multiple Trailing Special Elements | Improper Neutralization of Multiple Trailing Special Elements | CWE-163-multiple-trailing-special-elements |
| CWE-164 | weakness | Variant | Internal Special Element | Improper Neutralization of Internal Special Elements | CWE-164-internal-special-element |
| CWE-165 | weakness | Variant | Multiple Internal Special Element | Improper Neutralization of Multiple Internal Special Elements | CWE-165-multiple-internal-special-element |
| CWE-166 | weakness | Base | Missing Special Element | Improper Handling of Missing Special Element | CWE-166-missing-special-element |
| CWE-167 | weakness | Base | Extra Special Element | Improper Handling of Additional Special Element | CWE-167-extra-special-element |
| CWE-168 | weakness | Base | Inconsistent Special Elements | Improper Handling of Inconsistent Special Elements | CWE-168-inconsistent-special-elements |
| CWE-169 | category |  | DEPRECATED: Technology-Specific Special Elements | DEPRECATED: Technology-Specific Special Elements | CWE-169-deprecated-technology-specific-special-elements |
| CWE-170 | weakness | Base | Improper Null Termination | Improper Null Termination | CWE-170-improper-null-termination |
| CWE-171 | category |  | DEPRECATED: Cleansing, Canonicalization, and Comparison Errors | DEPRECATED: Cleansing, Canonicalization, and Comparison Errors | CWE-171-deprecated-cleansing-canonicalization-and-comparison-errors |
| CWE-172 | weakness | Class | Encoding Error | Encoding Error | CWE-172-encoding-error |
| CWE-173 | weakness | Variant | Alternate Encoding | Improper Handling of Alternate Encoding | CWE-173-alternate-encoding |
| CWE-174 | weakness | Variant | Double Encoding | Double Decoding of the Same Data | CWE-174-double-encoding |
| CWE-175 | weakness | Variant | Mixed Encoding | Improper Handling of Mixed Encoding | CWE-175-mixed-encoding |
| CWE-176 | weakness | Variant | Unicode Encoding | Improper Handling of Unicode Encoding | CWE-176-unicode-encoding |
| CWE-177 | weakness | Variant | URL Encoding (Hex Encoding) | Improper Handling of URL Encoding (Hex Encoding) | CWE-177-url-encoding-hex-encoding |
| CWE-178 | weakness | Base | Case Sensitivity (lowercase, uppercase, mixed case) | Improper Handling of Case Sensitivity | CWE-178-case-sensitivity-lowercase-uppercase-mixed-case |
| CWE-179 | weakness | Base | Early Validation Errors | Incorrect Behavior Order: Early Validation | CWE-179-early-validation-errors |
| CWE-180 | weakness | Variant | Validate-Before-Canonicalize | Incorrect Behavior Order: Validate Before Canonicalize | CWE-180-validate-before-canonicalize |
| CWE-181 | weakness | Variant | Validate-Before-Filter | Incorrect Behavior Order: Validate Before Filter | CWE-181-validate-before-filter |
| CWE-182 | weakness | Base | Collapse of Data into Unsafe Value | Collapse of Data into Unsafe Value | CWE-182-collapse-of-data-into-unsafe-value |
| CWE-183 | weakness | Base | Permissive Whitelist | Permissive List of Allowed Inputs | CWE-183-permissive-whitelist |
| CWE-184 | weakness | Base | Incomplete Blacklist | Incomplete List of Disallowed Inputs | CWE-184-incomplete-blacklist |
| CWE-185 | weakness | Class | Regular Expression Error | Incorrect Regular Expression | CWE-185-regular-expression-error |
| CWE-186 | weakness | Base | Overly Restrictive Regular Expression | Overly Restrictive Regular Expression | CWE-186-overly-restrictive-regular-expression |
| CWE-187 | weakness | Variant | Partial Comparison | Partial String Comparison | CWE-187-partial-comparison |
| CWE-188 | weakness | Base | Reliance on data layout | Reliance on Data/Memory Layout | CWE-188-reliance-on-data-layout |
| CWE-189 | category |  | Numeric Errors | Numeric Errors | CWE-189-numeric-errors |
| CWE-190 | weakness | Base | Integer overflow (wrap or wraparound) | Integer Overflow or Wraparound | CWE-190-integer-overflow-wrap-or-wraparound |
| CWE-191 | weakness | Base | Integer underflow (wrap or wraparound) | Integer Underflow (Wrap or Wraparound) | CWE-191-integer-underflow-wrap-or-wraparound |
| CWE-192 | weakness | Variant | Integer coercion error | Integer Coercion Error | CWE-192-integer-coercion-error |
| CWE-193 | weakness | Base | Off-by-one Error | Off-by-one Error | CWE-193-off-by-one-error |
| CWE-194 | weakness | Variant | Sign extension error | Unexpected Sign Extension | CWE-194-sign-extension-error |
| CWE-195 | weakness | Variant | Signed to unsigned conversion error | Signed to Unsigned Conversion Error | CWE-195-signed-to-unsigned-conversion-error |
| CWE-196 | weakness | Variant | Unsigned to signed conversion error | Unsigned to Signed Conversion Error | CWE-196-unsigned-to-signed-conversion-error |
| CWE-197 | weakness | Base | Numeric truncation error | Numeric Truncation Error | CWE-197-numeric-truncation-error |
| CWE-198 | weakness | Variant | Numeric Byte Ordering Error | Use of Incorrect Byte Ordering | CWE-198-numeric-byte-ordering-error |
| CWE-199 | category |  | Information Management Errors | Information Management Errors | CWE-199-information-management-errors |
| CWE-200 | weakness | Class | Information Leak (information disclosure) | Exposure of Sensitive Information to an Unauthorized Actor | CWE-200-information-leak-information-disclosure |
| CWE-201 | weakness | Base | Accidental leaking of sensitive information through sent data | Insertion of Sensitive Information Into Sent Data | CWE-201-accidental-leaking-of-sensitive-information-through-sent |
| CWE-202 | weakness | Base | Accidental leaking of sensitive information through data queries | Exposure of Sensitive Information Through Data Queries | CWE-202-accidental-leaking-of-sensitive-information-through-data |
| CWE-203 | weakness | Base | Discrepancy Information Leaks | Observable Discrepancy | CWE-203-discrepancy-information-leaks |
| CWE-204 | weakness | Base | Response discrepancy infoleak | Observable Response Discrepancy | CWE-204-response-discrepancy-infoleak |
| CWE-205 | weakness | Base | Behavioral Discrepancy Infoleak | Observable Behavioral Discrepancy | CWE-205-behavioral-discrepancy-infoleak |
| CWE-206 | weakness | Variant | Internal behavioral inconsistency infoleak | Observable Internal Behavioral Discrepancy | CWE-206-internal-behavioral-inconsistency-infoleak |
| CWE-207 | weakness | Variant | External behavioral inconsistency infoleak | Observable Behavioral Discrepancy With Equivalent Products | CWE-207-external-behavioral-inconsistency-infoleak |
| CWE-208 | weakness | Base | Timing discrepancy infoleak | Observable Timing Discrepancy | CWE-208-timing-discrepancy-infoleak |
| CWE-209 | weakness | Base | Accidental leaking of sensitive information through error messages | Generation of Error Message Containing Sensitive Information | CWE-209-accidental-leaking-of-sensitive-information-through-error |
| CWE-210 | weakness | Base | Product-Generated Error Message Infoleak | Self-generated Error Message Containing Sensitive Information | CWE-210-product-generated-error-message-infoleak |
| CWE-211 | weakness | Base | Product-External Error Message Infoleak | Externally-Generated Error Message Containing Sensitive Information | CWE-211-product-external-error-message-infoleak |
| CWE-212 | weakness | Base | Cross-Boundary Cleansing Infoleak | Improper Removal of Sensitive Information Before Storage or Transfer | CWE-212-cross-boundary-cleansing-infoleak |
| CWE-213 | weakness | Base | Intended information leak | Exposure of Sensitive Information Due to Incompatible Policies | CWE-213-intended-information-leak |
| CWE-214 | weakness | Base | Process information infoleak to other processes | Invocation of Process Using Visible Sensitive Information | CWE-214-process-information-infoleak-to-other-processes |
| CWE-215 | weakness | Base | Infoleak Using Debug Information | Insertion of Sensitive Information Into Debugging Code | CWE-215-infoleak-using-debug-information |
| CWE-216 | weakness | Class | DEPRECATED: Containment Errors | DEPRECATED: Containment Errors (Container Errors) | CWE-216-deprecated-containment-errors |
| CWE-217 | weakness | Base | DEPRECATED: Failure to Protect Stored Data from Modification | DEPRECATED: Failure to Protect Stored Data from Modification | CWE-217-deprecated-failure-to-protect-stored-data-from-modification |
| CWE-218 | weakness | Base | DEPRECATED: Failure to provide confidentiality for stored data | DEPRECATED: Failure to provide confidentiality for stored data | CWE-218-deprecated-failure-to-provide-confidentiality-for-stored |
| CWE-219 | weakness | Variant | Sensitive Data Under Web Root | Storage of File with Sensitive Data Under Web Root | CWE-219-sensitive-data-under-web-root |
| CWE-220 | weakness | Variant | Sensitive Data Under FTP Root | Storage of File With Sensitive Data Under FTP Root | CWE-220-sensitive-data-under-ftp-root |
| CWE-221 | weakness | Class | Information loss or omission | Information Loss or Omission | CWE-221-information-loss-or-omission |
| CWE-222 | weakness | Base | Truncation of Security-relevant Information | Truncation of Security-relevant Information | CWE-222-truncation-of-security-relevant-information |
| CWE-223 | weakness | Base | Omission of Security-relevant Information | Omission of Security-relevant Information | CWE-223-omission-of-security-relevant-information |
| CWE-224 | weakness | Base | Obscured Security-relevant Information by Alternate Name | Obscured Security-relevant Information by Alternate Name | CWE-224-obscured-security-relevant-information-by-alternate-name |
| CWE-225 | weakness | Base | DEPRECATED: General Information Management Problems | DEPRECATED: General Information Management Problems | CWE-225-deprecated-general-information-management-problems |
| CWE-226 | weakness | Base | Sensitive Information Uncleared Before Use | Sensitive Information in Resource Not Removed Before Reuse | CWE-226-sensitive-information-uncleared-before-use |
| CWE-227 | category |  | 7PK - API Abuse | 7PK - API Abuse | CWE-227-7pk-api-abuse |
| CWE-228 | weakness | Class | Structure and Validity Problems | Improper Handling of Syntactically Invalid Structure | CWE-228-structure-and-validity-problems |
| CWE-229 | weakness | Base | Improper Handling of Values | Improper Handling of Values | CWE-229-improper-handling-of-values |
| CWE-230 | weakness | Variant | Missing Value Error | Improper Handling of Missing Values | CWE-230-missing-value-error |
| CWE-231 | weakness | Variant | Extra Value Error | Improper Handling of Extra Values | CWE-231-extra-value-error |
| CWE-232 | weakness | Variant | Undefined Value Error | Improper Handling of Undefined Values | CWE-232-undefined-value-error |
| CWE-233 | weakness | Base | Parameter Problems | Improper Handling of Parameters | CWE-233-parameter-problems |
| CWE-234 | weakness | Variant | Missing Parameter Error | Failure to Handle Missing Parameter | CWE-234-missing-parameter-error |
| CWE-235 | weakness | Variant | Extra Parameter Error | Improper Handling of Extra Parameters | CWE-235-extra-parameter-error |
| CWE-236 | weakness | Variant | Undefined Parameter Error | Improper Handling of Undefined Parameters | CWE-236-undefined-parameter-error |
| CWE-237 | weakness | Base | Element Problems | Improper Handling of Structural Elements | CWE-237-element-problems |
| CWE-238 | weakness | Variant | Missing Element Error | Improper Handling of Incomplete Structural Elements | CWE-238-missing-element-error |
| CWE-239 | weakness | Variant | Incomplete Element | Failure to Handle Incomplete Element | CWE-239-incomplete-element |
| CWE-240 | weakness | Base | Inconsistent Elements | Improper Handling of Inconsistent Structural Elements | CWE-240-inconsistent-elements |
| CWE-241 | weakness | Base | Wrong Data Type | Improper Handling of Unexpected Data Type | CWE-241-wrong-data-type |
| CWE-242 | weakness | Base | Dangerous Functions | Use of Inherently Dangerous Function | CWE-242-dangerous-functions |
| CWE-243 | weakness | Variant | Directory Restriction | Creation of chroot Jail Without Changing Working Directory | CWE-243-directory-restriction |
| CWE-244 | weakness | Variant | Heap Inspection | Improper Clearing of Heap Memory Before Release ('Heap Inspection') | CWE-244-heap-inspection |
| CWE-245 | weakness | Variant | J2EE Bad Practices: getConnection() | J2EE Bad Practices: Direct Management of Connections | CWE-245-j2ee-bad-practices-getconnection |
| CWE-246 | weakness | Variant | J2EE Bad Practices: Sockets | J2EE Bad Practices: Direct Use of Sockets | CWE-246-j2ee-bad-practices-sockets |
| CWE-247 | weakness | Base | DEPRECATED: Reliance on DNS Lookups in a Security Decision | DEPRECATED: Reliance on DNS Lookups in a Security Decision | CWE-247-deprecated-reliance-on-dns-lookups-security-decision |
| CWE-248 | weakness | Base | Often Misused: Exception Handling | Uncaught Exception | CWE-248-often-misused-exception-handling |
| CWE-249 | weakness | Variant | DEPRECATED: Often Misused: Path Manipulation | DEPRECATED: Often Misused: Path Manipulation | CWE-249-deprecated-often-misused-path-manipulation |
| CWE-250 | weakness | Base | Often Misused: Privilege Management | Execution with Unnecessary Privileges | CWE-250-often-misused-privilege-management |
| CWE-251 | category |  | Often Misused: Strings | Often Misused: String Management | CWE-251-often-misused-strings |
| CWE-252 | weakness | Base | Unchecked Return Value | Unchecked Return Value | CWE-252-unchecked-return-value |
| CWE-253 | weakness | Base | Misinterpreted function return value | Incorrect Check of Function Return Value | CWE-253-misinterpreted-function-return-value |
| CWE-254 | category |  | Security Features | 7PK - Security Features | CWE-254-security-features |
| CWE-255 | category |  | Broken Authentication and Session Management | Credentials Management Errors | CWE-255-broken-authentication-and-session-management |
| CWE-256 | weakness | Base | Password Management | Plaintext Storage of a Password | CWE-256-password-management |
| CWE-257 | weakness | Base | Storing passwords in a recoverable format | Storing Passwords in a Recoverable Format | CWE-257-storing-passwords-in-a-recoverable-format |
| CWE-258 | weakness | Variant | Password Management: Empty Password in Configuration File | Empty Password in Configuration File | CWE-258-password-management-empty-password-in-configuration-file |
| CWE-259 | weakness | Variant | Password Management: Hard-Coded Password | Use of Hard-coded Password | CWE-259-password-management-hard-coded-password |
| CWE-260 | weakness | Base | Password Management: Password in Configuration File | Password in Configuration File | CWE-260-password-management-password-in-configuration-file |
| CWE-261 | weakness | Base | Password Management: Weak Cryptography | Weak Encoding for Password | CWE-261-password-management-weak-cryptography |
| CWE-262 | weakness | Base | Not allowing password aging | Not Using Password Aging | CWE-262-not-allowing-password-aging |
| CWE-263 | weakness | Base | Allowing password aging | Password Aging with Long Expiration | CWE-263-allowing-password-aging |
| CWE-264 | category |  | Permissions, Privileges, and ACLs | Permissions, Privileges, and Access Controls | CWE-264-permissions-privileges-and-acls |
| CWE-265 | category |  | Privilege / sandbox errors | Privilege Issues | CWE-265-privilege-sandbox-errors |
| CWE-266 | weakness | Base | Incorrect Privilege Assignment | Incorrect Privilege Assignment | CWE-266-incorrect-privilege-assignment |
| CWE-267 | weakness | Base | Unsafe Privilege | Privilege Defined With Unsafe Actions | CWE-267-unsafe-privilege |
| CWE-268 | weakness | Base | Privilege Chaining | Privilege Chaining | CWE-268-privilege-chaining |
| CWE-269 | weakness | Class | Privilege Management Error | Improper Privilege Management | CWE-269-privilege-management-error |
| CWE-270 | weakness | Base | Privilege Context Switching Error | Privilege Context Switching Error | CWE-270-privilege-context-switching-error |
| CWE-271 | weakness | Class | Privilege Dropping / Lowering Errors | Privilege Dropping / Lowering Errors | CWE-271-privilege-dropping-lowering-errors |
| CWE-272 | weakness | Base | Least Privilege Violation | Least Privilege Violation | CWE-272-least-privilege-violation |
| CWE-273 | weakness | Base | Failure to check whether privileges were dropped successfully | Improper Check for Dropped Privileges | CWE-273-failure-to-check-whether-privileges-were-dropped |
| CWE-274 | weakness | Base | Insufficient privileges | Improper Handling of Insufficient Privileges | CWE-274-insufficient-privileges |
| CWE-275 | category |  | Permission errors | Permission Issues | CWE-275-permission-errors |
| CWE-276 | weakness | Base | Insecure Default Permissions | Incorrect Default Permissions | CWE-276-insecure-default-permissions |
| CWE-277 | weakness | Variant | Insecure inherited permissions | Insecure Inherited Permissions | CWE-277-insecure-inherited-permissions |
| CWE-278 | weakness | Variant | Insecure preserved inherited permissions | Insecure Preserved Inherited Permissions | CWE-278-insecure-preserved-inherited-permissions |
| CWE-279 | weakness | Variant | Insecure execution-assigned permissions | Incorrect Execution-Assigned Permissions | CWE-279-insecure-execution-assigned-permissions |
| CWE-280 | weakness | Base | Fails poorly due to insufficient permissions | Improper Handling of Insufficient Permissions or Privileges | CWE-280-fails-poorly-due-to-insufficient-permissions |
| CWE-281 | weakness | Base | Permission preservation failure | Improper Preservation of Permissions | CWE-281-permission-preservation-failure |
| CWE-282 | weakness | Class | Ownership errors | Improper Ownership Management | CWE-282-ownership-errors |
| CWE-283 | weakness | Base | Unverified Ownership | Unverified Ownership | CWE-283-unverified-ownership |
| CWE-284 | weakness | Pillar | Access Control List (ACL) errors | Improper Access Control | CWE-284-access-control-list-acl-errors |
| CWE-285 | weakness | Class | Missing Access Control | Improper Authorization | CWE-285-missing-access-control |
| CWE-286 | weakness | Class | User management errors | Incorrect User Management | CWE-286-user-management-errors |
| CWE-287 | weakness | Class | Authentication Error | Improper Authentication | CWE-287-authentication-error |
| CWE-288 | weakness | Base | Authentication Bypass by Alternate Path/Channel | Authentication Bypass Using an Alternate Path or Channel | CWE-288-authentication-bypass-by-alternate-path-channel |
| CWE-289 | weakness | Base | Authentication bypass by alternate name | Authentication Bypass by Alternate Name | CWE-289-authentication-bypass-by-alternate-name |
| CWE-290 | weakness | Base | Authentication bypass by spoofing | Authentication Bypass by Spoofing | CWE-290-authentication-bypass-by-spoofing |
| CWE-291 | weakness | Variant | Trusting self-reported IP address | Reliance on IP Address for Authentication | CWE-291-trusting-self-reported-ip-address |
| CWE-292 | weakness | Variant | DEPRECATED: Trusting Self-reported DNS Name | DEPRECATED: Trusting Self-reported DNS Name | CWE-292-deprecated-trusting-self-reported-dns-name |
| CWE-293 | weakness | Variant | Using referrer field for authentication | Using Referer Field for Authentication | CWE-293-using-referrer-field-for-authentication |
| CWE-294 | weakness | Base | Authentication bypass by replay | Authentication Bypass by Capture-replay | CWE-294-authentication-bypass-by-replay |
| CWE-295 | weakness | Base | Insecure Configuration Management | Improper Certificate Validation | CWE-295-insecure-configuration-management |
| CWE-296 | weakness | Base | Failure to follow chain of trust in certificate validation | Improper Following of a Certificate's Chain of Trust | CWE-296-failure-follow-chain-trust-certificate-validation |
| CWE-297 | weakness | Variant | Failure to validate host-specific certificate data | Improper Validation of Certificate with Host Mismatch | CWE-297-failure-to-validate-host-specific-certificate-data |
| CWE-298 | weakness | Variant | Failure to validate certificate expiration | Improper Validation of Certificate Expiration | CWE-298-failure-to-validate-certificate-expiration |
| CWE-299 | weakness | Base | Failure to check for certificate revocation | Improper Check for Certificate Revocation | CWE-299-failure-to-check-for-certificate-revocation |
| CWE-300 | weakness | Class | Man-in-the-middle (MITM) | Channel Accessible by Non-Endpoint | CWE-300-man-in-the-middle-mitm |
| CWE-301 | weakness | Base | Reflection attack in an auth protocol | Reflection Attack in an Authentication Protocol | CWE-301-reflection-attack-in-an-auth-protocol |
| CWE-302 | weakness | Base | Authentication Bypass via Assumed-Immutable Data | Authentication Bypass by Assumed-Immutable Data | CWE-302-authentication-bypass-via-assumed-immutable-data |
| CWE-303 | weakness | Base | Authentication Logic Error | Incorrect Implementation of Authentication Algorithm | CWE-303-authentication-logic-error |
| CWE-304 | weakness | Base | Missing Critical Step in Authentication | Missing Critical Step in Authentication | CWE-304-missing-critical-step-in-authentication |
| CWE-305 | weakness | Base | Authentication Bypass by Primary Weakness | Authentication Bypass by Primary Weakness | CWE-305-authentication-bypass-by-primary-weakness |
| CWE-306 | weakness | Base | No Authentication for Critical Function | Missing Authentication for Critical Function | CWE-306-no-authentication-for-critical-function |
| CWE-307 | weakness | Base | Multiple Failed Authentication Attempts not Prevented | Improper Restriction of Excessive Authentication Attempts | CWE-307-multiple-failed-authentication-attempts-not-prevented |
| CWE-308 | weakness | Base | Using single-factor authentication | Use of Single-factor Authentication | CWE-308-using-single-factor-authentication |
| CWE-309 | weakness | Base | Using password systems | Use of Password System for Primary Authentication | CWE-309-using-password-systems |
| CWE-310 | category |  | Cryptographic Issues | Cryptographic Issues | CWE-310-cryptographic-issues |
| CWE-311 | weakness | Class | Insufficient Transport Layer Protection | Missing Encryption of Sensitive Data | CWE-311-insufficient-transport-layer-protection |
| CWE-312 | weakness | Base | Plaintext Storage of Sensitive Information | Cleartext Storage of Sensitive Information | CWE-312-plaintext-storage-of-sensitive-information |
| CWE-313 | weakness | Variant | Plaintext Storage in File or on Disk | Cleartext Storage in a File or on Disk | CWE-313-plaintext-storage-in-file-or-on-disk |
| CWE-314 | weakness | Variant | Plaintext Storage in Registry | Cleartext Storage in the Registry | CWE-314-plaintext-storage-in-registry |
| CWE-315 | weakness | Variant | Plaintext Storage in Cookie | Cleartext Storage of Sensitive Information in a Cookie | CWE-315-plaintext-storage-in-cookie |
| CWE-316 | weakness | Variant | Plaintext Storage in Memory | Cleartext Storage of Sensitive Information in Memory | CWE-316-plaintext-storage-in-memory |
| CWE-317 | weakness | Variant | Plaintext Storage in GUI | Cleartext Storage of Sensitive Information in GUI | CWE-317-plaintext-storage-in-gui |
| CWE-318 | weakness | Variant | Plaintext Storage in Executable | Cleartext Storage of Sensitive Information in Executable | CWE-318-plaintext-storage-in-executable |
| CWE-319 | weakness | Base | Plaintext Transmission of Sensitive Information | Cleartext Transmission of Sensitive Information | CWE-319-plaintext-transmission-of-sensitive-information |
| CWE-320 | category |  | Key Management Errors | Key Management Errors | CWE-320-key-management-errors |
| CWE-321 | weakness | Variant | Use of hard-coded cryptographic key | Use of Hard-coded Cryptographic Key | CWE-321-use-of-hard-coded-cryptographic-key |
| CWE-322 | weakness | Base | Key exchange without entity authentication | Key Exchange without Entity Authentication | CWE-322-key-exchange-without-entity-authentication |
| CWE-323 | weakness | Base | Reusing a nonce, key pair in encryption | Reusing a Nonce, Key Pair in Encryption | CWE-323-reusing-a-nonce-key-pair-in-encryption |
| CWE-324 | weakness | Base | Using a key past its expiration date | Use of a Key Past its Expiration Date | CWE-324-using-a-key-past-its-expiration-date |
| CWE-325 | weakness | Base | Missing Required Cryptographic Step | Missing Cryptographic Step | CWE-325-missing-required-cryptographic-step |
| CWE-326 | weakness | Class | Weak Encryption | Inadequate Encryption Strength | CWE-326-weak-encryption |
| CWE-327 | weakness | Class | Using a broken or risky cryptographic algorithm | Use of a Broken or Risky Cryptographic Algorithm | CWE-327-using-a-broken-or-risky-cryptographic-algorithm |
| CWE-328 | weakness | Base | Reversible One-Way Hash | Use of Weak Hash | CWE-328-reversible-one-way-hash |
| CWE-329 | weakness | Variant | Not using a random IV with CBC mode | Generation of Predictable IV with CBC Mode | CWE-329-not-using-a-random-iv-with-cbc-mode |
| CWE-330 | weakness | Class | Randomness and Predictability | Use of Insufficiently Random Values | CWE-330-randomness-and-predictability |
| CWE-331 | weakness | Base | Insufficient Entropy | Insufficient Entropy | CWE-331-insufficient-entropy |
| CWE-332 | weakness | Variant | Insufficient entropy in PRNG | Insufficient Entropy in PRNG | CWE-332-insufficient-entropy-in-prng |
| CWE-333 | weakness | Variant | Failure of TRNG | Improper Handling of Insufficient Entropy in TRNG | CWE-333-failure-of-trng |
| CWE-334 | weakness | Base | Small Space of Random Values | Small Space of Random Values | CWE-334-small-space-of-random-values |
| CWE-335 | weakness | Base | PRNG Seed Error | Incorrect Usage of Seeds in Pseudo-Random Number Generator (PRNG) | CWE-335-prng-seed-error |
| CWE-336 | weakness | Variant | Same Seed in PRNG | Same Seed in Pseudo-Random Number Generator (PRNG) | CWE-336-same-seed-in-prng |
| CWE-337 | weakness | Variant | Predictable Seed in PRNG | Predictable Seed in Pseudo-Random Number Generator (PRNG) | CWE-337-predictable-seed-in-prng |
| CWE-338 | weakness | Base | Non-cryptographic PRNG | Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG) | CWE-338-non-cryptographic-prng |
| CWE-339 | weakness | Variant | Small Seed Space in PRNG | Small Seed Space in PRNG | CWE-339-small-seed-space-in-prng |
| CWE-340 | weakness | Class | Predictability problems | Generation of Predictable Numbers or Identifiers | CWE-340-predictability-problems |
| CWE-341 | weakness | Base | Predictable from Observable State | Predictable from Observable State | CWE-341-predictable-from-observable-state |
| CWE-342 | weakness | Base | Predictable Exact Value from Previous Values | Predictable Exact Value from Previous Values | CWE-342-predictable-exact-value-from-previous-values |
| CWE-343 | weakness | Base | Predictable Value Range from Previous Values | Predictable Value Range from Previous Values | CWE-343-predictable-value-range-from-previous-values |
| CWE-344 | weakness | Base | Static Value in Unpredictable Context | Use of Invariant Value in Dynamically Changing Context | CWE-344-static-value-in-unpredictable-context |
| CWE-345 | weakness | Class | Insufficient Verification of Data | Insufficient Verification of Data Authenticity | CWE-345-insufficient-verification-of-data |
| CWE-346 | weakness | Class | Origin Validation Error | Origin Validation Error | CWE-346-origin-validation-error |
| CWE-347 | weakness | Base | Improperly Verified Signature | Improper Verification of Cryptographic Signature | CWE-347-improperly-verified-signature |
| CWE-348 | weakness | Base | Use of Less Trusted Source | Use of Less Trusted Source | CWE-348-use-of-less-trusted-source |
| CWE-349 | weakness | Base | Untrusted Data Appended with Trusted Data | Acceptance of Extraneous Untrusted Data With Trusted Data | CWE-349-untrusted-data-appended-with-trusted-data |
| CWE-350 | weakness | Variant | Improperly Trusted Reverse DNS | Reliance on Reverse DNS Resolution for a Security-Critical Action | CWE-350-improperly-trusted-reverse-dns |
| CWE-351 | weakness | Base | Insufficient Type Distinction | Insufficient Type Distinction | CWE-351-insufficient-type-distinction |
| CWE-352 | weakness | Compound | Cross-Site Request Forgery (CSRF) | Cross-Site Request Forgery (CSRF) | CWE-352-cross-site-request-forgery-csrf |
| CWE-353 | weakness | Base | Failure to add integrity check value | Missing Support for Integrity Check | CWE-353-failure-to-add-integrity-check-value |
| CWE-354 | weakness | Base | Failure to check integrity check value | Improper Validation of Integrity Check Value | CWE-354-failure-to-check-integrity-check-value |
| CWE-355 | category |  | (UI) User Interface Errors | User Interface Security Issues | CWE-355-ui-user-interface-errors |
| CWE-356 | weakness | Base | Product UI does not warn user of unsafe actions | Product UI does not Warn User of Unsafe Actions | CWE-356-product-ui-does-not-warn-user-unsafe-actions |
| CWE-357 | weakness | Base | Insufficient UI warning of dangerous operations | Insufficient UI Warning of Dangerous Operations | CWE-357-insufficient-ui-warning-of-dangerous-operations |
| CWE-358 | weakness | Base | Improperly Implemented Security Check for Standard | Improperly Implemented Security Check for Standard | CWE-358-improperly-implemented-security-check-for-standard |
| CWE-359 | weakness | Base | Privacy Violation | Exposure of Private Personal Information to an Unauthorized Actor | CWE-359-privacy-violation |
| CWE-360 | weakness | Base | Trust of system event data | Trust of System Event Data | CWE-360-trust-of-system-event-data |
| CWE-361 | category |  | 7PK - Time and State | 7PK - Time and State | CWE-361-7pk-time-and-state |
| CWE-362 | weakness | Class | Race Conditions | Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition') | CWE-362-race-conditions |
| CWE-363 | weakness | Base | Race condition enabling link following | Race Condition Enabling Link Following | CWE-363-race-condition-enabling-link-following |
| CWE-364 | weakness | Base | Signal handler race condition | Signal Handler Race Condition | CWE-364-signal-handler-race-condition |
| CWE-365 | weakness | Base | DEPRECATED: Race Condition in Switch | DEPRECATED: Race Condition in Switch | CWE-365-deprecated-race-condition-in-switch |
| CWE-366 | weakness | Base | Race condition within a thread | Race Condition within a Thread | CWE-366-race-condition-within-a-thread |
| CWE-367 | weakness | Base | Time-of-check Time-of-use race condition | Time-of-check Time-of-use (TOCTOU) Race Condition | CWE-367-time-of-check-time-of-use-race-condition |
| CWE-368 | weakness | Base | Context Switching Race Condition | Context Switching Race Condition | CWE-368-context-switching-race-condition |
| CWE-369 | weakness | Base | Denial of Service | Divide By Zero | CWE-369-denial-of-service |
| CWE-370 | weakness | Variant | Race condition in checking for certificate revocation | Missing Check for Certificate Revocation after Initial Check | CWE-370-race-condition-in-checking-for-certificate-revocation |
| CWE-371 | category |  | State Issues | State Issues | CWE-371-state-issues |
| CWE-372 | weakness | Base | Incomplete Internal State Distinction | Incomplete Internal State Distinction | CWE-372-incomplete-internal-state-distinction |
| CWE-373 | weakness | Base | DEPRECATED: State Synchronization Error | DEPRECATED: State Synchronization Error | CWE-373-deprecated-state-synchronization-error |
| CWE-374 | weakness | Base | Passing mutable objects to an untrusted method | Passing Mutable Objects to an Untrusted Method | CWE-374-passing-mutable-objects-to-an-untrusted-method |
| CWE-375 | weakness | Base | Mutable object returned | Returning a Mutable Object to an Untrusted Caller | CWE-375-mutable-object-returned |
| CWE-376 | category |  | DEPRECATED: Temporary File Issues | DEPRECATED: Temporary File Issues | CWE-376-deprecated-temporary-file-issues |
| CWE-377 | weakness | Class | Insecure Temporary File | Insecure Temporary File | CWE-377-insecure-temporary-file |
| CWE-378 | weakness | Base | Improper temp file opening | Creation of Temporary File With Insecure Permissions | CWE-378-improper-temp-file-opening |
| CWE-379 | weakness | Base | Guessed or visible temporary file | Creation of Temporary File in Directory with Insecure Permissions | CWE-379-guessed-or-visible-temporary-file |
| CWE-380 | category |  | DEPRECATED: Technology-Specific Time and State Issues | DEPRECATED: Technology-Specific Time and State Issues | CWE-380-deprecated-technology-specific-time-and-state-issues |
| CWE-381 | category |  | DEPRECATED: J2EE Time and State Issues | DEPRECATED: J2EE Time and State Issues | CWE-381-deprecated-j2ee-time-and-state-issues |
| CWE-382 | weakness | Variant | J2EE Bad Practices: System.exit() | J2EE Bad Practices: Use of System.exit() | CWE-382-j2ee-bad-practices-system-exit |
| CWE-383 | weakness | Variant | J2EE Bad Practices: Threads | J2EE Bad Practices: Direct Use of Threads | CWE-383-j2ee-bad-practices-threads |
| CWE-384 | weakness | Compound | Session Fixation | Session Fixation | CWE-384-session-fixation |
| CWE-385 | weakness | Base | Covert Timing Channel | Covert Timing Channel | CWE-385-covert-timing-channel |
| CWE-386 | weakness | Base | Symbolic name not mapping to correct object | Symbolic Name not Mapping to Correct Object | CWE-386-symbolic-name-not-mapping-to-correct-object |
| CWE-387 | category |  | Signal Errors | Signal Errors | CWE-387-signal-errors |
| CWE-388 | category |  | 7PK - Errors | 7PK - Errors | CWE-388-7pk-errors |
| CWE-389 | category |  | Error Conditions, Return Values, Status Codes | Error Conditions, Return Values, Status Codes | CWE-389-error-conditions-return-values-status-codes |
| CWE-390 | weakness | Base | Improper error handling | Detection of Error Condition Without Action | CWE-390-improper-error-handling |
| CWE-391 | weakness | Base | Unchecked Return Value | Unchecked Error Condition | CWE-391-unchecked-return-value |
| CWE-392 | weakness | Base | Missing Error Status Code | Missing Report of Error Condition | CWE-392-missing-error-status-code |
| CWE-393 | weakness | Base | Wrong Status Code | Return of Wrong Status Code | CWE-393-wrong-status-code |
| CWE-394 | weakness | Base | Unexpected Status Code or Return Value | Unexpected Status Code or Return Value | CWE-394-unexpected-status-code-or-return-value |
| CWE-395 | weakness | Base | Catching NullPointerException | Use of NullPointerException Catch to Detect NULL Pointer Dereference | CWE-395-catching-nullpointerexception |
| CWE-396 | weakness | Base | Overly-Broad Catch Block | Declaration of Catch for Generic Exception | CWE-396-overly-broad-catch-block |
| CWE-397 | weakness | Base | Overly-Broad Throws Declaration | Declaration of Throws for Generic Exception | CWE-397-overly-broad-throws-declaration |
| CWE-398 | category |  | 7PK - Code Quality | 7PK - Code Quality | CWE-398-7pk-code-quality |
| CWE-399 | category |  | Resource Management Errors | Resource Management Errors | CWE-399-resource-management-errors |
| CWE-400 | weakness | Class | Denial of Service | Uncontrolled Resource Consumption | CWE-400-denial-of-service |
| CWE-401 | weakness | Variant | Memory leak | Missing Release of Memory after Effective Lifetime | CWE-401-memory-leak |
| CWE-402 | weakness | Class | Resource leaks | Transmission of Private Resources into a New Sphere ('Resource Leak') | CWE-402-resource-leaks |
| CWE-403 | weakness | Base | UNIX file descriptor leak | Exposure of File Descriptor to Unintended Control Sphere ('File Descriptor Leak') | CWE-403-unix-file-descriptor-leak |
| CWE-404 | weakness | Class | Improper resource shutdown or release | Improper Resource Shutdown or Release | CWE-404-improper-resource-shutdown-or-release |
| CWE-405 | weakness | Class | Asymmetric resource consumption (amplification) | Asymmetric Resource Consumption (Amplification) | CWE-405-asymmetric-resource-consumption-amplification |
| CWE-406 | weakness | Class | Network Amplification | Insufficient Control of Network Message Volume (Network Amplification) | CWE-406-network-amplification |
| CWE-407 | weakness | Class | Algorithmic Complexity | Inefficient Algorithmic Complexity | CWE-407-algorithmic-complexity |
| CWE-408 | weakness | Base | Early Amplification | Incorrect Behavior Order: Early Amplification | CWE-408-early-amplification |
| CWE-409 | weakness | Base | Data Amplification | Improper Handling of Highly Compressed Data (Data Amplification) | CWE-409-data-amplification |
| CWE-410 | weakness | Class | Insufficient Resource Pool | Insufficient Resource Pool | CWE-410-insufficient-resource-pool |
| CWE-411 | category |  | Resource Locking problems | Resource Locking Problems | CWE-411-resource-locking-problems |
| CWE-412 | weakness | Base | Unrestricted Critical Resource Lock | Unrestricted Externally Accessible Lock | CWE-412-unrestricted-critical-resource-lock |
| CWE-413 | weakness | Base | Insufficient Resource Locking | Improper Resource Locking | CWE-413-insufficient-resource-locking |
| CWE-414 | weakness | Base | Missing Lock Check | Missing Lock Check | CWE-414-missing-lock-check |
| CWE-415 | weakness | Variant | DFREE - Double-Free Vulnerability | Double Free | CWE-415-dfree-double-free-vulnerability |
| CWE-416 | weakness | Variant | Use After Free | Use After Free | CWE-416-use-after-free |
| CWE-417 | category |  | Channel and Path Errors | Communication Channel Errors | CWE-417-channel-and-path-errors |
| CWE-418 | category |  | DEPRECATED: Channel Errors | DEPRECATED: Channel Errors | CWE-418-deprecated-channel-errors |
| CWE-419 | weakness | Base | Unprotected Primary Channel | Unprotected Primary Channel | CWE-419-unprotected-primary-channel |
| CWE-420 | weakness | Base | Unprotected Alternate Channel | Unprotected Alternate Channel | CWE-420-unprotected-alternate-channel |
| CWE-421 | weakness | Base | Alternate Channel Race Condition | Race Condition During Access to Alternate Channel | CWE-421-alternate-channel-race-condition |
| CWE-422 | weakness | Variant | Unprotected Windows Messaging Channel ('Shatter') | Unprotected Windows Messaging Channel ('Shatter') | CWE-422-unprotected-windows-messaging-channel-shatter |
| CWE-423 | weakness | Base | DEPRECATED: Proxied Trusted Channel | DEPRECATED: Proxied Trusted Channel | CWE-423-deprecated-proxied-trusted-channel |
| CWE-424 | weakness | Class | Alternate Path Errors | Improper Protection of Alternate Path | CWE-424-alternate-path-errors |
| CWE-425 | weakness | Base | Direct Request aka 'Forced Browsing' | Direct Request ('Forced Browsing') | CWE-425-direct-request-aka-forced-browsing |
| CWE-426 | weakness | Base | Untrusted Search Path | Untrusted Search Path | CWE-426-untrusted-search-path |
| CWE-427 | weakness | Base | Uncontrolled Search Path Element | Uncontrolled Search Path Element | CWE-427-uncontrolled-search-path-element |
| CWE-428 | weakness | Base | Unquoted Search Path or Element | Unquoted Search Path or Element | CWE-428-unquoted-search-path-or-element |
| CWE-429 | category |  | Handler Errors | Handler Errors | CWE-429-handler-errors |
| CWE-430 | weakness | Base | Improper Handler Deployment | Deployment of Wrong Handler | CWE-430-improper-handler-deployment |
| CWE-431 | weakness | Base | Missing Handler | Missing Handler | CWE-431-missing-handler |
| CWE-432 | weakness | Base | Dangerous handler not cleared/disabled during sensitive operations | Dangerous Signal Handler not Disabled During Sensitive Operations | CWE-432-dangerous-handler-not-cleared-disabled-during-sensitive |
| CWE-433 | weakness | Variant | Unparsed Raw Web Content Delivery | Unparsed Raw Web Content Delivery | CWE-433-unparsed-raw-web-content-delivery |
| CWE-434 | weakness | Base | Unrestricted File Upload | Unrestricted Upload of File with Dangerous Type | CWE-434-unrestricted-file-upload |
| CWE-435 | weakness | Pillar | Interaction Errors | Improper Interaction Between Multiple Correctly-Behaving Entities | CWE-435-interaction-errors |
| CWE-436 | weakness | Class | Multiple Interpretation Error (MIE) | Interpretation Conflict | CWE-436-multiple-interpretation-error-mie |
| CWE-437 | weakness | Base | Extra Unhandled Features | Incomplete Model of Endpoint Features | CWE-437-extra-unhandled-features |
| CWE-438 | category |  | Behavioral problems | Behavioral Problems | CWE-438-behavioral-problems |
| CWE-439 | weakness | Base | CHANGE Behavioral Change | Behavioral Change in New Version or Environment | CWE-439-change-behavioral-change |
| CWE-440 | weakness | Base | Expected behavior violation | Expected Behavior Violation | CWE-440-expected-behavior-violation |
| CWE-441 | weakness | Class | Unintended proxy/intermediary | Unintended Proxy or Intermediary ('Confused Deputy') | CWE-441-unintended-proxy-intermediary |
| CWE-442 | category |  | DEPRECATED: Web Problems | DEPRECATED: Web Problems | CWE-442-deprecated-web-problems |
| CWE-443 | weakness | Base | DEPRECATED: HTTP response splitting | DEPRECATED: HTTP response splitting | CWE-443-deprecated-http-response-splitting |
| CWE-444 | weakness | Base | HTTP Request Smuggling | Inconsistent Interpretation of HTTP Requests ('HTTP Request/Response Smuggling') | CWE-444-http-request-smuggling |
| CWE-445 | category |  | DEPRECATED: User Interface Errors | DEPRECATED: User Interface Errors | CWE-445-deprecated-user-interface-errors |
| CWE-446 | weakness | Class | User interface inconsistency | UI Discrepancy for Security Feature | CWE-446-user-interface-inconsistency |
| CWE-447 | weakness | Base | Unimplemented or unsupported feature in UI | Unimplemented or Unsupported Feature in UI | CWE-447-unimplemented-or-unsupported-feature-in-ui |
| CWE-448 | weakness | Base | Obsolete feature in UI | Obsolete Feature in UI | CWE-448-obsolete-feature-in-ui |
| CWE-449 | weakness | Base | The UI performs the wrong action | The UI Performs the Wrong Action | CWE-449-the-ui-performs-the-wrong-action |
| CWE-450 | weakness | Base | Multiple Interpretations of UI Input | Multiple Interpretations of UI Input | CWE-450-multiple-interpretations-of-ui-input |
| CWE-451 | weakness | Class | UI Misrepresentation of Critical Information | User Interface (UI) Misrepresentation of Critical Information | CWE-451-ui-misrepresentation-of-critical-information |
| CWE-452 | category |  | Initialization and Cleanup Errors | Initialization and Cleanup Errors | CWE-452-initialization-and-cleanup-errors |
| CWE-453 | weakness | Variant | Insecure default variable initialization | Insecure Default Variable Initialization | CWE-453-insecure-default-variable-initialization |
| CWE-454 | weakness | Base | External initialization of trusted variables or values | External Initialization of Trusted Variables or Data Stores | CWE-454-external-initialization-of-trusted-variables-or-values |
| CWE-455 | weakness | Base | Non-exit on Failed Initialization | Non-exit on Failed Initialization | CWE-455-non-exit-on-failed-initialization |
| CWE-456 | weakness | Variant | Missing Initialization | Missing Initialization of a Variable | CWE-456-missing-initialization |
| CWE-457 | weakness | Variant | Uninitialized Variable | Use of Uninitialized Variable | CWE-457-uninitialized-variable |
| CWE-458 | weakness | Base | DEPRECATED: Incorrect Initialization | DEPRECATED: Incorrect Initialization | CWE-458-deprecated-incorrect-initialization |
| CWE-459 | weakness | Base | Incomplete Cleanup | Incomplete Cleanup | CWE-459-incomplete-cleanup |
| CWE-460 | weakness | Base | Improper cleanup on thrown exception | Improper Cleanup on Thrown Exception | CWE-460-improper-cleanup-on-thrown-exception |
| CWE-461 | category |  | DEPRECATED: Data Structure Issues | DEPRECATED: Data Structure Issues | CWE-461-deprecated-data-structure-issues |
| CWE-462 | weakness | Variant | Duplicate key in associative list (alist) | Duplicate Key in Associative List (Alist) | CWE-462-duplicate-key-in-associative-list-alist |
| CWE-463 | weakness | Base | Deletion of data-structure sentinel | Deletion of Data Structure Sentinel | CWE-463-deletion-of-data-structure-sentinel |
| CWE-464 | weakness | Base | Addition of data-structure sentinel | Addition of Data Structure Sentinel | CWE-464-addition-of-data-structure-sentinel |
| CWE-465 | category |  | Pointer Issues | Pointer Issues | CWE-465-pointer-issues |
| CWE-466 | weakness | Base | Illegal Pointer Value | Return of Pointer Value Outside of Expected Range | CWE-466-illegal-pointer-value |
| CWE-467 | weakness | Variant | Use of sizeof() on a pointer type | Use of sizeof() on a Pointer Type | CWE-467-use-of-sizeof-on-a-pointer-type |
| CWE-468 | weakness | Base | Unintentional pointer scaling | Incorrect Pointer Scaling | CWE-468-unintentional-pointer-scaling |
| CWE-469 | weakness | Base | Improper pointer subtraction | Use of Pointer Subtraction to Determine Size | CWE-469-improper-pointer-subtraction |
| CWE-470 | weakness | Base | Unsafe Reflection | Use of Externally-Controlled Input to Select Classes or Code ('Unsafe Reflection') | CWE-470-unsafe-reflection |
| CWE-471 | weakness | Base | Modification of Assumed-Immutable Data | Modification of Assumed-Immutable Data (MAID) | CWE-471-modification-of-assumed-immutable-data |
| CWE-472 | weakness | Base | Web Parameter Tampering | External Control of Assumed-Immutable Web Parameter | CWE-472-web-parameter-tampering |
| CWE-473 | weakness | Variant | PHP External Variable Modification | PHP External Variable Modification | CWE-473-php-external-variable-modification |
| CWE-474 | weakness | Base | Inconsistent Implementations | Use of Function with Inconsistent Implementations | CWE-474-inconsistent-implementations |
| CWE-475 | weakness | Base | Undefined Behavior | Undefined Behavior for Input to API | CWE-475-undefined-behavior |
| CWE-476 | weakness | Base | Null Dereference (Null Pointer Dereference) | NULL Pointer Dereference | CWE-476-null-dereference-null-pointer-dereference |
| CWE-477 | weakness | Base | Obsolete | Use of Obsolete Function | CWE-477-obsolete |
| CWE-478 | weakness | Base | Failure to account for default case in switch | Missing Default Case in Multiple Condition Expression | CWE-478-failure-to-account-for-default-case-in-switch |
| CWE-479 | weakness | Variant | Unsafe function call from a signal handler | Signal Handler Use of a Non-reentrant Function | CWE-479-unsafe-function-call-from-a-signal-handler |
| CWE-480 | weakness | Base | Using the wrong operator | Use of Incorrect Operator | CWE-480-using-the-wrong-operator |
| CWE-481 | weakness | Variant | Assigning instead of comparing | Assigning instead of Comparing | CWE-481-assigning-instead-of-comparing |
| CWE-482 | weakness | Variant | Comparing instead of assigning | Comparing instead of Assigning | CWE-482-comparing-instead-of-assigning |
| CWE-483 | weakness | Base | Incorrect block delimitation | Incorrect Block Delimitation | CWE-483-incorrect-block-delimitation |
| CWE-484 | weakness | Base | Omitted break statement | Omitted Break Statement in Switch | CWE-484-omitted-break-statement |
| CWE-485 | category |  | 7PK - Encapsulation | 7PK - Encapsulation | CWE-485-7pk-encapsulation |
| CWE-486 | weakness | Variant | Comparing Classes by Name | Comparison of Classes by Name | CWE-486-comparing-classes-by-name |
| CWE-487 | weakness | Base | Relying on package-level scope | Reliance on Package-level Scope | CWE-487-relying-on-package-level-scope |
| CWE-488 | weakness | Base | Data Leaking Between Users | Exposure of Data Element to Wrong Session | CWE-488-data-leaking-between-users |
| CWE-489 | weakness | Base | Leftover Debug Code | Active Debug Code | CWE-489-leftover-debug-code |
| CWE-490 | category |  | DEPRECATED: Mobile Code Issues | DEPRECATED: Mobile Code Issues | CWE-490-deprecated-mobile-code-issues |
| CWE-491 | weakness | Variant | Mobile Code: Object Hijack | Public cloneable() Method Without Final ('Object Hijack') | CWE-491-mobile-code-object-hijack |
| CWE-492 | weakness | Variant | Mobile Code: Use of Inner Class | Use of Inner Class Containing Sensitive Data | CWE-492-mobile-code-use-of-inner-class |
| CWE-493 | weakness | Variant | Mobile Code: Non-Final Public Field | Critical Public Variable Without Final Modifier | CWE-493-mobile-code-non-final-public-field |
| CWE-494 | weakness | Base | Invoking untrusted mobile code | Download of Code Without Integrity Check | CWE-494-invoking-untrusted-mobile-code |
| CWE-495 | weakness | Variant | Private Array-Typed Field Returned From A Public Method | Private Data Structure Returned From A Public Method | CWE-495-private-array-typed-field-returned-from-public-method |
| CWE-496 | weakness | Variant | Public Data Assigned to Private Array-Typed Field | Public Data Assigned to Private Array-Typed Field | CWE-496-public-data-assigned-to-private-array-typed-field |
| CWE-497 | weakness | Base | System Information Leak | Exposure of Sensitive System Information to an Unauthorized Control Sphere | CWE-497-system-information-leak |
| CWE-498 | weakness | Variant | Information leak through class cloning | Cloneable Class Containing Sensitive Information | CWE-498-information-leak-through-class-cloning |
| CWE-499 | weakness | Variant | Information leak through serialization | Serializable Class Containing Sensitive Data | CWE-499-information-leak-through-serialization |
| CWE-500 | weakness | Variant | Overflow of static internal buffer | Public Static Field Not Marked Final | CWE-500-overflow-of-static-internal-buffer |
| CWE-501 | weakness | Base | Trust Boundary Violation | Trust Boundary Violation | CWE-501-trust-boundary-violation |
| CWE-502 | weakness | Base | Deserialization of untrusted data | Deserialization of Untrusted Data | CWE-502-deserialization-of-untrusted-data |
| CWE-503 | category |  | DEPRECATED: Byte/Object Code | DEPRECATED: Byte/Object Code | CWE-503-deprecated-byte-object-code |
| CWE-504 | category |  | DEPRECATED: Motivation/Intent | DEPRECATED: Motivation/Intent | CWE-504-deprecated-motivation-intent |
| CWE-505 | category |  | DEPRECATED: Intentionally Introduced Weakness | DEPRECATED: Intentionally Introduced Weakness | CWE-505-deprecated-intentionally-introduced-weakness |
| CWE-506 | weakness | Class | Embedded Malicious Code | Embedded Malicious Code | CWE-506-embedded-malicious-code |
| CWE-507 | weakness | Base | Trojan Horse | Trojan Horse | CWE-507-trojan-horse |
| CWE-508 | weakness | Base | Non-Replicating Malicious Code | Non-Replicating Malicious Code | CWE-508-non-replicating-malicious-code |
| CWE-509 | weakness | Base | Replicating Malicious Code | Replicating Malicious Code (Virus or Worm) | CWE-509-replicating-malicious-code |
| CWE-510 | weakness | Base | Trapdoor | Trapdoor | CWE-510-trapdoor |
| CWE-511 | weakness | Base | Logic/Time Bomb | Logic/Time Bomb | CWE-511-logic-time-bomb |
| CWE-512 | weakness | Base | Spyware | Spyware | CWE-512-spyware |
| CWE-513 | category |  | DEPRECATED: Intentionally Introduced Nonmalicious Weakness | DEPRECATED: Intentionally Introduced Nonmalicious Weakness | CWE-513-deprecated-intentionally-introduced-nonmalicious-weakness |
| CWE-514 | weakness | Class | Covert Channel | Covert Channel | CWE-514-covert-channel |
| CWE-515 | weakness | Base | Covert storage channel | Covert Storage Channel | CWE-515-covert-storage-channel |
| CWE-516 | weakness | Base | DEPRECATED: Covert Timing Channel | DEPRECATED: Covert Timing Channel | CWE-516-deprecated-covert-timing-channel |
| CWE-517 | category |  | DEPRECATED: Other Intentional, Nonmalicious Weakness | DEPRECATED: Other Intentional, Nonmalicious Weakness | CWE-517-deprecated-other-intentional-nonmalicious-weakness |
| CWE-518 | category |  | DEPRECATED: Inadvertently Introduced Weakness | DEPRECATED: Inadvertently Introduced Weakness | CWE-518-deprecated-inadvertently-introduced-weakness |
| CWE-519 | category |  | DEPRECATED: .NET Environment Issues | DEPRECATED: .NET Environment Issues | CWE-519-deprecated-net-environment-issues |
| CWE-520 | weakness | Variant | .NET Misconfiguration: Use of Impersonation | .NET Misconfiguration: Use of Impersonation | CWE-520-net-misconfiguration-use-of-impersonation |
| CWE-521 | weakness | Base | Broken Authentication and Session Management | Weak Password Requirements | CWE-521-broken-authentication-and-session-management |
| CWE-522 | weakness | Class | Broken Authentication and Session Management | Insufficiently Protected Credentials | CWE-522-broken-authentication-and-session-management |
| CWE-523 | weakness | Base | Unprotected Transport of Credentials | Unprotected Transport of Credentials | CWE-523-unprotected-transport-of-credentials |
| CWE-524 | weakness | Base | Use of Cache Containing Sensitive Information | Use of Cache Containing Sensitive Information | CWE-524-use-of-cache-containing-sensitive-information |
| CWE-525 | weakness | Variant | Broken Authentication and Session Management | Use of Web Browser Cache Containing Sensitive Information | CWE-525-broken-authentication-and-session-management |
| CWE-526 | weakness | Variant | Cleartext Storage of Sensitive Information in an Environment Variable | Cleartext Storage of Sensitive Information in an Environment Variable | CWE-526-cleartext-storage-sensitive-information-environment-variable |
| CWE-527 | weakness | Variant | Exposure of Version-Control Repository to an Unauthorized Control Sphere | Exposure of Version-Control Repository to an Unauthorized Control Sphere | CWE-527-exposure-version-control-repository-unauthorized-control |
| CWE-528 | weakness | Variant | Exposure of Core Dump File to an Unauthorized Control Sphere | Exposure of Core Dump File to an Unauthorized Control Sphere | CWE-528-exposure-core-dump-file-unauthorized-control-sphere |
| CWE-529 | weakness | Variant | Exposure of Access Control List Files to an Unauthorized Control Sphere | Exposure of Access Control List Files to an Unauthorized Control Sphere | CWE-529-exposure-access-control-list-files-unauthorized-control |
| CWE-530 | weakness | Variant | Exposure of Backup File to an Unauthorized Control Sphere | Exposure of Backup File to an Unauthorized Control Sphere | CWE-530-exposure-backup-file-unauthorized-control-sphere |
| CWE-531 | weakness | Variant | Inclusion of Sensitive Information in Test Code | Inclusion of Sensitive Information in Test Code | CWE-531-inclusion-of-sensitive-information-in-test-code |
| CWE-532 | weakness | Base | Insertion of Sensitive Information into Log File | Insertion of Sensitive Information into Log File | CWE-532-insertion-of-sensitive-information-into-log-file |
| CWE-533 | weakness | Variant | DEPRECATED: Information Exposure Through Server Log Files | DEPRECATED: Information Exposure Through Server Log Files | CWE-533-deprecated-information-exposure-through-server-log-files |
| CWE-534 | weakness | Variant | DEPRECATED: Information Exposure Through Debug Log Files | DEPRECATED: Information Exposure Through Debug Log Files | CWE-534-deprecated-information-exposure-through-debug-log-files |
| CWE-535 | weakness | Variant | Exposure of Information Through Shell Error Message | Exposure of Information Through Shell Error Message | CWE-535-exposure-of-information-through-shell-error-message |
| CWE-536 | weakness | Variant | Servlet Runtime Error Message Containing Sensitive Information | Servlet Runtime Error Message Containing Sensitive Information | CWE-536-servlet-runtime-error-message-containing-sensitive |
| CWE-537 | weakness | Variant | Java Runtime Error Message Containing Sensitive Information | Java Runtime Error Message Containing Sensitive Information | CWE-537-java-runtime-error-message-containing-sensitive-information |
| CWE-538 | weakness | Base | Insertion of Sensitive Information into Externally-Accessible File or Directory | Insertion of Sensitive Information into Externally-Accessible File or Directory | CWE-538-insertion-sensitive-information-into-externally-accessible |
| CWE-539 | weakness | Variant | Use of Persistent Cookies Containing Sensitive Information | Use of Persistent Cookies Containing Sensitive Information | CWE-539-use-of-persistent-cookies-containing-sensitive-information |
| CWE-540 | weakness | Base | Inclusion of Sensitive Information in Source Code | Inclusion of Sensitive Information in Source Code | CWE-540-inclusion-of-sensitive-information-in-source-code |
| CWE-541 | weakness | Variant | Inclusion of Sensitive Information in an Include File | Inclusion of Sensitive Information in an Include File | CWE-541-inclusion-of-sensitive-information-in-an-include-file |
| CWE-542 | weakness | Variant | DEPRECATED: Information Exposure Through Cleanup Log Files | DEPRECATED: Information Exposure Through Cleanup Log Files | CWE-542-deprecated-information-exposure-through-cleanup-log-files |
| CWE-543 | weakness | Variant | Use of Singleton Pattern Without Synchronization in a Multithreaded Context | Use of Singleton Pattern Without Synchronization in a Multithreaded Context | CWE-543-singleton-pattern-without-synchronization-multithreaded |
| CWE-544 | weakness | Base | Missing Standardized Error Handling Mechanism | Missing Standardized Error Handling Mechanism | CWE-544-missing-standardized-error-handling-mechanism |
| CWE-545 | weakness | Variant | DEPRECATED: Use of Dynamic Class Loading | DEPRECATED: Use of Dynamic Class Loading | CWE-545-deprecated-use-of-dynamic-class-loading |
| CWE-546 | weakness | Variant | Suspicious Comment | Suspicious Comment | CWE-546-suspicious-comment |
| CWE-547 | weakness | Base | Use of Hard-coded, Security-relevant Constants | Use of Hard-coded, Security-relevant Constants | CWE-547-use-of-hard-coded-security-relevant-constants |
| CWE-548 | weakness | Variant | Directory Indexing | Exposure of Information Through Directory Listing | CWE-548-directory-indexing |
| CWE-549 | weakness | Base | Missing Password Field Masking | Missing Password Field Masking | CWE-549-missing-password-field-masking |
| CWE-550 | weakness | Variant | Server-generated Error Message Containing Sensitive Information | Server-generated Error Message Containing Sensitive Information | CWE-550-server-generated-error-message-containing-sensitive |
| CWE-551 | weakness | Base | Incorrect Behavior Order: Authorization Before Parsing and Canonicalization | Incorrect Behavior Order: Authorization Before Parsing and Canonicalization | CWE-551-incorrect-behavior-order-authorization-before-parsing-and |
| CWE-552 | weakness | Base | Insecure Configuration Management | Files or Directories Accessible to External Parties | CWE-552-insecure-configuration-management |
| CWE-553 | weakness | Variant | Command Shell in Externally Accessible Directory | Command Shell in Externally Accessible Directory | CWE-553-command-shell-in-externally-accessible-directory |
| CWE-554 | weakness | Variant | ASP.NET Misconfiguration: Not Using Input Validation Framework | ASP.NET Misconfiguration: Not Using Input Validation Framework | CWE-554-asp-net-misconfiguration-not-using-input-validation |
| CWE-555 | weakness | Variant | J2EE Misconfiguration: Plaintext Password in Configuration File | J2EE Misconfiguration: Plaintext Password in Configuration File | CWE-555-j2ee-misconfiguration-plaintext-password-in-configuration |
| CWE-556 | weakness | Variant | ASP.NET Misconfiguration: Use of Identity Impersonation | ASP.NET Misconfiguration: Use of Identity Impersonation | CWE-556-asp-net-misconfiguration-use-of-identity-impersonation |
| CWE-557 | category |  | Concurrency Issues | Concurrency Issues | CWE-557-concurrency-issues |
| CWE-558 | weakness | Variant | Often Misused: Authentication | Use of getlogin() in Multithreaded Application | CWE-558-often-misused-authentication |
| CWE-559 | category |  | DEPRECATED: Often Misused: Arguments and Parameters | DEPRECATED: Often Misused: Arguments and Parameters | CWE-559-deprecated-often-misused-arguments-and-parameters |
| CWE-560 | weakness | Variant | Use of umask with chmod-style Argument | Use of umask() with chmod-style Argument | CWE-560-use-of-umask-with-chmod-style-argument |
| CWE-561 | weakness | Base | Dead Code | Dead Code | CWE-561-dead-code |
| CWE-562 | weakness | Base | Return of Stack Variable Address | Return of Stack Variable Address | CWE-562-return-of-stack-variable-address |
| CWE-563 | weakness | Base | Assignment to Variable without Use | Assignment to Variable without Use | CWE-563-assignment-to-variable-without-use |
| CWE-564 | weakness | Variant | SQL Injection: Hibernate | SQL Injection: Hibernate | CWE-564-sql-injection-hibernate |
| CWE-565 | weakness | Base | Reliance on Cookies without Validation and Integrity Checking | Reliance on Cookies without Validation and Integrity Checking | CWE-565-reliance-on-cookies-without-validation-and-integrity |
| CWE-566 | weakness | Variant | Authorization Bypass Through User-Controlled SQL Primary Key | Authorization Bypass Through User-Controlled SQL Primary Key | CWE-566-authorization-bypass-through-user-controlled-sql-primary-key |
| CWE-567 | weakness | Base | Unsynchronized Access to Shared Data in a Multithreaded Context | Unsynchronized Access to Shared Data in a Multithreaded Context | CWE-567-unsynchronized-access-shared-data-multithreaded-context |
| CWE-568 | weakness | Variant | finalize Method Without super.finalize | finalize() Method Without super.finalize() | CWE-568-finalize-method-without-super-finalize |
| CWE-569 | category |  | Expression Issues | Expression Issues | CWE-569-expression-issues |
| CWE-570 | weakness | Base | Expression is Always False | Expression is Always False | CWE-570-expression-is-always-false |
| CWE-571 | weakness | Base | Expression is Always True | Expression is Always True | CWE-571-expression-is-always-true |
| CWE-572 | weakness | Variant | Call to Thread run instead of start | Call to Thread run() instead of start() | CWE-572-call-to-thread-run-instead-of-start |
| CWE-573 | weakness | Class | Improper Following of Specification by Caller | Improper Following of Specification by Caller | CWE-573-improper-following-of-specification-by-caller |
| CWE-574 | weakness | Variant | EJB Bad Practices: Use of Synchronization Primitives | EJB Bad Practices: Use of Synchronization Primitives | CWE-574-ejb-bad-practices-use-of-synchronization-primitives |
| CWE-575 | weakness | Variant | EJB Bad Practices: Use of AWT Swing | EJB Bad Practices: Use of AWT Swing | CWE-575-ejb-bad-practices-use-of-awt-swing |
| CWE-576 | weakness | Variant | EJB Bad Practices: Use of Java I/O | EJB Bad Practices: Use of Java I/O | CWE-576-ejb-bad-practices-use-of-java-i-o |
| CWE-577 | weakness | Variant | EJB Bad Practices: Use of Sockets | EJB Bad Practices: Use of Sockets | CWE-577-ejb-bad-practices-use-of-sockets |
| CWE-578 | weakness | Variant | EJB Bad Practices: Use of Class Loader | EJB Bad Practices: Use of Class Loader | CWE-578-ejb-bad-practices-use-of-class-loader |
| CWE-579 | weakness | Variant | J2EE Bad Practices: Non-serializable Object Stored in Session | J2EE Bad Practices: Non-serializable Object Stored in Session | CWE-579-j2ee-bad-practices-non-serializable-object-stored-session |
| CWE-580 | weakness | Variant | clone Method Without super.clone | clone() Method Without super.clone() | CWE-580-clone-method-without-super-clone |
| CWE-581 | weakness | Variant | Object Model Violation: Just One of Equals and Hashcode Defined | Object Model Violation: Just One of Equals and Hashcode Defined | CWE-581-object-model-violation-just-one-equals-hashcode-defined |
| CWE-582 | weakness | Variant | Array Declared Public, Final, and Static | Array Declared Public, Final, and Static | CWE-582-array-declared-public-final-and-static |
| CWE-583 | weakness | Variant | finalize Method Declared Public | finalize() Method Declared Public | CWE-583-finalize-method-declared-public |
| CWE-584 | weakness | Base | Return Inside Finally Block | Return Inside Finally Block | CWE-584-return-inside-finally-block |
| CWE-585 | weakness | Variant | Empty Synchronized Block | Empty Synchronized Block | CWE-585-empty-synchronized-block |
| CWE-586 | weakness | Base | Explicit Call to Finalize | Explicit Call to Finalize() | CWE-586-explicit-call-to-finalize |
| CWE-587 | weakness | Variant | Assignment of a Fixed Address to a Pointer | Assignment of a Fixed Address to a Pointer | CWE-587-assignment-of-a-fixed-address-to-a-pointer |
| CWE-588 | weakness | Variant | Attempt to Access Child of a Non-structure Pointer | Attempt to Access Child of a Non-structure Pointer | CWE-588-attempt-access-child-non-structure-pointer |
| CWE-589 | weakness | Variant | Call to Non-ubiquitous API | Call to Non-ubiquitous API | CWE-589-call-to-non-ubiquitous-api |
| CWE-590 | weakness | Variant | Free of Memory not on the Heap | Free of Memory not on the Heap | CWE-590-free-of-memory-not-on-the-heap |
| CWE-591 | weakness | Variant | Insecure Storage | Sensitive Data Storage in Improperly Locked Memory | CWE-591-insecure-storage |
| CWE-592 | weakness | Class | DEPRECATED: Authentication Bypass Issues | DEPRECATED: Authentication Bypass Issues | CWE-592-deprecated-authentication-bypass-issues |
| CWE-593 | weakness | Variant | Authentication Bypass: OpenSSL CTX Object Modified after SSL Objects are Created | Authentication Bypass: OpenSSL CTX Object Modified after SSL Objects are Created | CWE-593-authentication-bypass-openssl-ctx-object-modified-after-ssl |
| CWE-594 | weakness | Variant | J2EE Framework: Saving Unserializable Objects to Disk | J2EE Framework: Saving Unserializable Objects to Disk | CWE-594-j2ee-framework-saving-unserializable-objects-to-disk |
| CWE-595 | weakness | Variant | Comparison of Object References Instead of Object Contents | Comparison of Object References Instead of Object Contents | CWE-595-comparison-of-object-references-instead-of-object-contents |
| CWE-596 | weakness | Base | DEPRECATED: Incorrect Semantic Object Comparison | DEPRECATED: Incorrect Semantic Object Comparison | CWE-596-deprecated-incorrect-semantic-object-comparison |
| CWE-597 | weakness | Variant | Use of Wrong Operator in String Comparison | Use of Wrong Operator in String Comparison | CWE-597-use-of-wrong-operator-in-string-comparison |
| CWE-598 | weakness | Variant | Use of HTTP Request With Sensitive Query String | Use of HTTP Request With Sensitive Query String | CWE-598-use-of-http-request-with-sensitive-query-string |
| CWE-599 | weakness | Variant | Missing Validation of OpenSSL Certificate | Missing Validation of OpenSSL Certificate | CWE-599-missing-validation-of-openssl-certificate |
| CWE-600 | weakness | Variant | Uncaught Exception in Servlet | Uncaught Exception in Servlet | CWE-600-uncaught-exception-in-servlet |
| CWE-601 | weakness | Base | URl Redirector Abuse | URL Redirection to Untrusted Site ('Open Redirect') | CWE-601-url-redirector-abuse |
| CWE-602 | weakness | Class | Client-Side Enforcement of Server-Side Security | Client-Side Enforcement of Server-Side Security | CWE-602-client-side-enforcement-of-server-side-security |
| CWE-603 | weakness | Base | Use of Client-Side Authentication | Use of Client-Side Authentication | CWE-603-use-of-client-side-authentication |
| CWE-605 | weakness | Variant | Multiple Binds to the Same Port | Multiple Binds to the Same Port | CWE-605-multiple-binds-to-the-same-port |
| CWE-606 | weakness | Base | Unchecked Input for Loop Condition | Unchecked Input for Loop Condition | CWE-606-unchecked-input-for-loop-condition |
| CWE-607 | weakness | Variant | Public Static Final Field References Mutable Object | Public Static Final Field References Mutable Object | CWE-607-public-static-final-field-references-mutable-object |
| CWE-608 | weakness | Variant | Struts: Non-private Field in ActionForm Class | Struts: Non-private Field in ActionForm Class | CWE-608-struts-non-private-field-in-actionform-class |
| CWE-609 | weakness | Base | Double-Checked Locking | Double-Checked Locking | CWE-609-double-checked-locking |
| CWE-610 | weakness | Class | Externally Controlled Reference to a Resource in Another Sphere | Externally Controlled Reference to a Resource in Another Sphere | CWE-610-externally-controlled-reference-resource-another-sphere |
| CWE-611 | weakness | Base | XML External Entities | Improper Restriction of XML External Entity Reference | CWE-611-xml-external-entities |
| CWE-612 | weakness | Base | Insecure Indexing | Improper Authorization of Index Containing Sensitive Information | CWE-612-insecure-indexing |
| CWE-613 | weakness | Base | Insufficient Session Expiration | Insufficient Session Expiration | CWE-613-insufficient-session-expiration |
| CWE-614 | weakness | Variant | Sensitive Cookie in HTTPS Session Without 'Secure' Attribute | Sensitive Cookie in HTTPS Session Without 'Secure' Attribute | CWE-614-sensitive-cookie-in-https-session-without-secure-attribute |
| CWE-615 | weakness | Variant | Inclusion of Sensitive Information in Source Code Comments | Inclusion of Sensitive Information in Source Code Comments | CWE-615-inclusion-of-sensitive-information-in-source-code-comments |
| CWE-616 | weakness | Variant | Incomplete Identification of Uploaded File Variables (PHP) | Incomplete Identification of Uploaded File Variables (PHP) | CWE-616-incomplete-identification-of-uploaded-file-variables-php |
| CWE-617 | weakness | Base | Reachable Assertion | Reachable Assertion | CWE-617-reachable-assertion |
| CWE-618 | weakness | Variant | Exposed Unsafe ActiveX Method | Exposed Unsafe ActiveX Method | CWE-618-exposed-unsafe-activex-method |
| CWE-619 | weakness | Base | Cursor Injection | Dangling Database Cursor ('Cursor Injection') | CWE-619-cursor-injection |
| CWE-620 | weakness | Base | Broken Authentication and Session Management | Unverified Password Change | CWE-620-broken-authentication-and-session-management |
| CWE-621 | weakness | Variant | Variable Extraction Error | Variable Extraction Error | CWE-621-variable-extraction-error |
| CWE-622 | weakness | Variant | Improper Validation of Function Hook Arguments | Improper Validation of Function Hook Arguments | CWE-622-improper-validation-of-function-hook-arguments |
| CWE-623 | weakness | Variant | Unsafe ActiveX Control Marked Safe For Scripting | Unsafe ActiveX Control Marked Safe For Scripting | CWE-623-unsafe-activex-control-marked-safe-for-scripting |
| CWE-624 | weakness | Base | Executable Regular Expression Error | Executable Regular Expression Error | CWE-624-executable-regular-expression-error |
| CWE-625 | weakness | Base | Permissive Regular Expression | Permissive Regular Expression | CWE-625-permissive-regular-expression |
| CWE-626 | weakness | Variant | Null Byte Interaction Error | Null Byte Interaction Error (Poison Null Byte) | CWE-626-null-byte-interaction-error |
| CWE-627 | weakness | Variant | Dynamic Variable Evaluation | Dynamic Variable Evaluation | CWE-627-dynamic-variable-evaluation |
| CWE-628 | weakness | Base | Function Call with Incorrectly Specified Arguments | Function Call with Incorrectly Specified Arguments | CWE-628-function-call-with-incorrectly-specified-arguments |
| CWE-632 | category |  | DEPRECATED: Weaknesses that Affect Files or Directories | DEPRECATED: Weaknesses that Affect Files or Directories | CWE-632-deprecated-weaknesses-that-affect-files-or-directories |
| CWE-633 | category |  | DEPRECATED: Weaknesses that Affect Memory | DEPRECATED: Weaknesses that Affect Memory | CWE-633-deprecated-weaknesses-that-affect-memory |
| CWE-634 | category |  | DEPRECATED: Weaknesses that Affect System Processes | DEPRECATED: Weaknesses that Affect System Processes | CWE-634-deprecated-weaknesses-that-affect-system-processes |
| CWE-636 | weakness | Class | Improper Error Handling | Not Failing Securely ('Failing Open') | CWE-636-improper-error-handling |
| CWE-637 | weakness | Class | Unnecessary Complexity in Protection Mechanism | Unnecessary Complexity in Protection Mechanism (Not Using 'Economy of Mechanism') | CWE-637-unnecessary-complexity-in-protection-mechanism |
| CWE-638 | weakness | Class | Not Using Complete Mediation | Not Using Complete Mediation | CWE-638-not-using-complete-mediation |
| CWE-639 | weakness | Base | Authorization Bypass Through User-Controlled Key | Authorization Bypass Through User-Controlled Key | CWE-639-authorization-bypass-through-user-controlled-key |
| CWE-640 | weakness | Base | Insufficient Password Recovery | Weak Password Recovery Mechanism for Forgotten Password | CWE-640-insufficient-password-recovery |
| CWE-641 | weakness | Base | Improper Restriction of Names for Files and Other Resources | Improper Restriction of Names for Files and Other Resources | CWE-641-improper-restriction-names-for-files-other-resources |
| CWE-642 | weakness | Class | External Control of Critical State Data | External Control of Critical State Data | CWE-642-external-control-of-critical-state-data |
| CWE-643 | weakness | Base | XPath Injection | Improper Neutralization of Data within XPath Expressions ('XPath Injection') | CWE-643-xpath-injection |
| CWE-644 | weakness | Variant | Improper Neutralization of HTTP Headers for Scripting Syntax | Improper Neutralization of HTTP Headers for Scripting Syntax | CWE-644-improper-neutralization-of-http-headers-for-scripting-syntax |
| CWE-645 | weakness | Base | Overly Restrictive Account Lockout Mechanism | Overly Restrictive Account Lockout Mechanism | CWE-645-overly-restrictive-account-lockout-mechanism |
| CWE-646 | weakness | Variant | Reliance on File Name or Extension of Externally-Supplied File | Reliance on File Name or Extension of Externally-Supplied File | CWE-646-reliance-on-file-name-extension-externally-supplied-file |
| CWE-647 | weakness | Variant | Use of Non-Canonical URL Paths for Authorization Decisions | Use of Non-Canonical URL Paths for Authorization Decisions | CWE-647-non-canonical-url-paths-for-authorization-decisions |
| CWE-648 | weakness | Base | Incorrect Use of Privileged APIs | Incorrect Use of Privileged APIs | CWE-648-incorrect-use-of-privileged-apis |
| CWE-649 | weakness | Base | Reliance on Obfuscation or Encryption of Security-Relevant Inputs without Integrity Checking | Reliance on Obfuscation or Encryption of Security-Relevant Inputs without Integrity Checking | CWE-649-reliance-on-obfuscation-encryption-security-relevant-inputs |
| CWE-650 | weakness | Variant | Trusting HTTP Permission Methods on the Server Side | Trusting HTTP Permission Methods on the Server Side | CWE-650-trusting-http-permission-methods-on-the-server-side |
| CWE-651 | weakness | Variant | Exposure of WSDL File Containing Sensitive Information | Exposure of WSDL File Containing Sensitive Information | CWE-651-exposure-of-wsdl-file-containing-sensitive-information |
| CWE-652 | weakness | Base | XQuery Injection | Improper Neutralization of Data within XQuery Expressions ('XQuery Injection') | CWE-652-xquery-injection |
| CWE-653 | weakness | Class | Improper Isolation or Compartmentalization | Improper Isolation or Compartmentalization | CWE-653-improper-isolation-or-compartmentalization |
| CWE-654 | weakness | Base | Reliance on a Single Factor in a Security Decision | Reliance on a Single Factor in a Security Decision | CWE-654-reliance-on-single-factor-security-decision |
| CWE-655 | weakness | Class | Insufficient Psychological Acceptability | Insufficient Psychological Acceptability | CWE-655-insufficient-psychological-acceptability |
| CWE-656 | weakness | Class | Reliance on Security Through Obscurity | Reliance on Security Through Obscurity | CWE-656-reliance-on-security-through-obscurity |
| CWE-657 | weakness | Class | Violation of Secure Design Principles | Violation of Secure Design Principles | CWE-657-violation-of-secure-design-principles |
| CWE-662 | weakness | Class | State synchronization error | Improper Synchronization | CWE-662-state-synchronization-error |
| CWE-663 | weakness | Base | Use of a Non-reentrant Function in a Concurrent Context | Use of a Non-reentrant Function in a Concurrent Context | CWE-663-non-reentrant-function-concurrent-context |
| CWE-664 | weakness | Pillar | Improper Control of a Resource Through its Lifetime | Improper Control of a Resource Through its Lifetime | CWE-664-improper-control-of-a-resource-through-its-lifetime |
| CWE-665 | weakness | Class | Incorrect initialization | Improper Initialization | CWE-665-incorrect-initialization |
| CWE-666 | weakness | Class | Operation on Resource in Wrong Phase of Lifetime | Operation on Resource in Wrong Phase of Lifetime | CWE-666-operation-on-resource-in-wrong-phase-of-lifetime |
| CWE-667 | weakness | Class | Improper Locking | Improper Locking | CWE-667-improper-locking |
| CWE-668 | weakness | Class | Exposure of Resource to Wrong Sphere | Exposure of Resource to Wrong Sphere | CWE-668-exposure-of-resource-to-wrong-sphere |
| CWE-669 | weakness | Class | Incorrect Resource Transfer Between Spheres | Incorrect Resource Transfer Between Spheres | CWE-669-incorrect-resource-transfer-between-spheres |
| CWE-670 | weakness | Class | Always-Incorrect Control Flow Implementation | Always-Incorrect Control Flow Implementation | CWE-670-always-incorrect-control-flow-implementation |
| CWE-671 | weakness | Class | Lack of Administrator Control over Security | Lack of Administrator Control over Security | CWE-671-lack-of-administrator-control-over-security |
| CWE-672 | weakness | Class | Operation on a Resource after Expiration or Release | Operation on a Resource after Expiration or Release | CWE-672-operation-on-a-resource-after-expiration-or-release |
| CWE-673 | weakness | Class | External Influence of Sphere Definition | External Influence of Sphere Definition | CWE-673-external-influence-of-sphere-definition |
| CWE-674 | weakness | Class | Denial of Service | Uncontrolled Recursion | CWE-674-denial-of-service |
| CWE-675 | weakness | Class | Multiple Operations on Resource in Single-Operation Context | Multiple Operations on Resource in Single-Operation Context | CWE-675-multiple-operations-on-resource-in-single-operation-context |
| CWE-676 | weakness | Base | Dangerous Functions | Use of Potentially Dangerous Function | CWE-676-dangerous-functions |
| CWE-680 | weakness | Compound | Integer Overflow to Buffer Overflow | Integer Overflow to Buffer Overflow | CWE-680-integer-overflow-to-buffer-overflow |
| CWE-681 | weakness | Base | Incorrect Conversion between Numeric Types | Incorrect Conversion between Numeric Types | CWE-681-incorrect-conversion-between-numeric-types |
| CWE-682 | weakness | Pillar | Incorrect Calculation | Incorrect Calculation | CWE-682-incorrect-calculation |
| CWE-683 | weakness | Variant | Function Call With Incorrect Order of Arguments | Function Call With Incorrect Order of Arguments | CWE-683-function-call-with-incorrect-order-of-arguments |
| CWE-684 | weakness | Class | Incorrect Provision of Specified Functionality | Incorrect Provision of Specified Functionality | CWE-684-incorrect-provision-of-specified-functionality |
| CWE-685 | weakness | Variant | Function Call With Incorrect Number of Arguments | Function Call With Incorrect Number of Arguments | CWE-685-function-call-with-incorrect-number-of-arguments |
| CWE-686 | weakness | Variant | Function Call With Incorrect Argument Type | Function Call With Incorrect Argument Type | CWE-686-function-call-with-incorrect-argument-type |
| CWE-687 | weakness | Variant | Function Call With Incorrectly Specified Argument Value | Function Call With Incorrectly Specified Argument Value | CWE-687-function-call-with-incorrectly-specified-argument-value |
| CWE-688 | weakness | Variant | Function Call With Incorrect Variable or Reference as Argument | Function Call With Incorrect Variable or Reference as Argument | CWE-688-function-call-with-incorrect-variable-reference-argument |
| CWE-689 | weakness | Compound | Permission Race Condition During Resource Copy | Permission Race Condition During Resource Copy | CWE-689-permission-race-condition-during-resource-copy |
| CWE-690 | weakness | Compound | Unchecked Return Value to NULL Pointer Dereference | Unchecked Return Value to NULL Pointer Dereference | CWE-690-unchecked-return-value-to-null-pointer-dereference |
| CWE-691 | weakness | Pillar | Insufficient Process Validation | Insufficient Control Flow Management | CWE-691-insufficient-process-validation |
| CWE-692 | weakness | Compound | Incomplete Denylist to Cross-Site Scripting | Incomplete Denylist to Cross-Site Scripting | CWE-692-incomplete-denylist-to-cross-site-scripting |
| CWE-693 | weakness | Pillar | Protection Mechanism Failure | Protection Mechanism Failure | CWE-693-protection-mechanism-failure |
| CWE-694 | weakness | Base | Use of Multiple Resources with Duplicate Identifier | Use of Multiple Resources with Duplicate Identifier | CWE-694-use-of-multiple-resources-with-duplicate-identifier |
| CWE-695 | weakness | Base | Use of Low-Level Functionality | Use of Low-Level Functionality | CWE-695-use-of-low-level-functionality |
| CWE-696 | weakness | Class | Incorrect Behavior Order | Incorrect Behavior Order | CWE-696-incorrect-behavior-order |
| CWE-697 | weakness | Pillar | Incorrect Comparison | Incorrect Comparison | CWE-697-incorrect-comparison |
| CWE-698 | weakness | Base | Execution After Redirect | Execution After Redirect (EAR) | CWE-698-execution-after-redirect |
| CWE-703 | weakness | Pillar | Improper Check or Handling of Exceptional Conditions | Improper Check or Handling of Exceptional Conditions | CWE-703-improper-check-or-handling-of-exceptional-conditions |
| CWE-704 | weakness | Class | Incorrect Type Conversion or Cast | Incorrect Type Conversion or Cast | CWE-704-incorrect-type-conversion-or-cast |
| CWE-705 | weakness | Class | Incorrect Control Flow Scoping | Incorrect Control Flow Scoping | CWE-705-incorrect-control-flow-scoping |
| CWE-706 | weakness | Class | Use of Incorrectly-Resolved Name or Reference | Use of Incorrectly-Resolved Name or Reference | CWE-706-use-of-incorrectly-resolved-name-or-reference |
| CWE-707 | weakness | Pillar | Improper Neutralization | Improper Neutralization | CWE-707-improper-neutralization |
| CWE-708 | weakness | Base | Incorrect Ownership Assignment | Incorrect Ownership Assignment | CWE-708-incorrect-ownership-assignment |
| CWE-710 | weakness | Pillar | Improper Adherence to Coding Standards | Improper Adherence to Coding Standards | CWE-710-improper-adherence-to-coding-standards |
| CWE-712 | category |  | OWASP Top Ten 2007 Category A1 - Cross Site Scripting | OWASP Top Ten 2007 Category A1 - Cross Site Scripting (XSS) | CWE-712-owasp-top-ten-2007-category-a1-cross-site |
| CWE-713 | category |  | OWASP Top Ten 2007 Category A2 - Injection Flaws | OWASP Top Ten 2007 Category A2 - Injection Flaws | CWE-713-owasp-top-ten-2007-category-a2-injection-flaws |
| CWE-714 | category |  | OWASP Top Ten 2007 Category A3 - Malicious File Execution | OWASP Top Ten 2007 Category A3 - Malicious File Execution | CWE-714-owasp-top-ten-2007-category-a3-malicious-file |
| CWE-715 | category |  | OWASP Top Ten 2007 Category A4 - Insecure Direct Object Reference | OWASP Top Ten 2007 Category A4 - Insecure Direct Object Reference | CWE-715-owasp-top-ten-2007-category-a4-insecure-direct |
| CWE-716 | category |  | OWASP Top Ten 2007 Category A5 - Cross Site Request Forgery | OWASP Top Ten 2007 Category A5 - Cross Site Request Forgery (CSRF) | CWE-716-owasp-top-ten-2007-category-a5-cross-site |
| CWE-717 | category |  | OWASP Top Ten 2007 Category A6 - Information Leakage and Improper Error Handling | OWASP Top Ten 2007 Category A6 - Information Leakage and Improper Error Handling | CWE-717-owasp-top-ten-2007-category-a6-information-leakage |
| CWE-718 | category |  | OWASP Top Ten 2007 Category A7 - Broken Authentication and Session Management | OWASP Top Ten 2007 Category A7 - Broken Authentication and Session Management | CWE-718-owasp-top-ten-2007-category-a7-broken-authentication |
| CWE-719 | category |  | OWASP Top Ten 2007 Category A8 - Insecure Cryptographic Storage | OWASP Top Ten 2007 Category A8 - Insecure Cryptographic Storage | CWE-719-owasp-top-ten-2007-category-a8-insecure-cryptographic |
| CWE-720 | category |  | OWASP Top Ten 2007 Category A9 - Insecure Communications | OWASP Top Ten 2007 Category A9 - Insecure Communications | CWE-720-owasp-top-ten-2007-category-a9-insecure-communications |
| CWE-721 | category |  | OWASP Top Ten 2007 Category A10 - Failure to Restrict URL Access | OWASP Top Ten 2007 Category A10 - Failure to Restrict URL Access | CWE-721-owasp-top-ten-2007-category-a10-failure-restrict |
| CWE-722 | category |  | OWASP Top Ten 2004 Category A1 - Unvalidated Input | OWASP Top Ten 2004 Category A1 - Unvalidated Input | CWE-722-owasp-top-ten-2004-category-a1-unvalidated-input |
| CWE-723 | category |  | OWASP Top Ten 2004 Category A2 - Broken Access Control | OWASP Top Ten 2004 Category A2 - Broken Access Control | CWE-723-owasp-top-ten-2004-category-a2-broken-access |
| CWE-724 | category |  | OWASP Top Ten 2004 Category A3 - Broken Authentication and Session Management | OWASP Top Ten 2004 Category A3 - Broken Authentication and Session Management | CWE-724-owasp-top-ten-2004-category-a3-broken-authentication |
| CWE-725 | category |  | OWASP Top Ten 2004 Category A4 - Cross-Site Scripting Flaws | OWASP Top Ten 2004 Category A4 - Cross-Site Scripting (XSS) Flaws | CWE-725-owasp-top-ten-2004-category-a4-cross-site |
| CWE-726 | category |  | OWASP Top Ten 2004 Category A5 - Buffer Overflows | OWASP Top Ten 2004 Category A5 - Buffer Overflows | CWE-726-owasp-top-ten-2004-category-a5-buffer-overflows |
| CWE-727 | category |  | OWASP Top Ten 2004 Category A6 - Injection Flaws | OWASP Top Ten 2004 Category A6 - Injection Flaws | CWE-727-owasp-top-ten-2004-category-a6-injection-flaws |
| CWE-728 | category |  | OWASP Top Ten 2004 Category A7 - Improper Error Handling | OWASP Top Ten 2004 Category A7 - Improper Error Handling | CWE-728-owasp-top-ten-2004-category-a7-improper-error |
| CWE-729 | category |  | OWASP Top Ten 2004 Category A8 - Insecure Storage | OWASP Top Ten 2004 Category A8 - Insecure Storage | CWE-729-owasp-top-ten-2004-category-a8-insecure-storage |
| CWE-730 | category |  | OWASP Top Ten 2004 Category A9 - Denial of Service | OWASP Top Ten 2004 Category A9 - Denial of Service | CWE-730-owasp-top-ten-2004-category-a9-denial-service |
| CWE-731 | category |  | OWASP Top Ten 2004 Category A10 - Insecure Configuration Management | OWASP Top Ten 2004 Category A10 - Insecure Configuration Management | CWE-731-owasp-top-ten-2004-category-a10-insecure-configuration |
| CWE-732 | weakness | Class | Incorrect Permission Assignment for Critical Resource | Incorrect Permission Assignment for Critical Resource | CWE-732-incorrect-permission-assignment-for-critical-resource |
| CWE-733 | weakness | Base | Compiler Optimization Removal or Modification of Security-critical Code | Compiler Optimization Removal or Modification of Security-critical Code | CWE-733-compiler-optimization-removal-modification-security-critical |
| CWE-735 | category |  | CERT C Secure Coding Standard Chapter 2 - Preprocessor | CERT C Secure Coding Standard (2008) Chapter 2 - Preprocessor (PRE) | CWE-735-cert-c-secure-coding-standard-chapter-2-preprocessor |
| CWE-736 | category |  | CERT C Secure Coding Standard Chapter 3 - Declarations and Initialization | CERT C Secure Coding Standard (2008) Chapter 3 - Declarations and Initialization (DCL) | CWE-736-cert-c-secure-coding-standard-chapter-3-declarations |
| CWE-737 | category |  | CERT C Secure Coding Standard Chapter 4 - Expressions | CERT C Secure Coding Standard (2008) Chapter 4 - Expressions (EXP) | CWE-737-cert-c-secure-coding-standard-chapter-4-expressions |
| CWE-738 | category |  | CERT C Secure Coding Standard Chapter 5 - Integers | CERT C Secure Coding Standard (2008) Chapter 5 - Integers (INT) | CWE-738-cert-c-secure-coding-standard-chapter-5-integers |
| CWE-739 | category |  | CERT C Secure Coding Standard Chapter 6 - Floating Point | CERT C Secure Coding Standard (2008) Chapter 6 - Floating Point (FLP) | CWE-739-cert-c-secure-coding-standard-chapter-6-floating |
| CWE-740 | category |  | CERT C Secure Coding Standard Chapter 7 - Arrays | CERT C Secure Coding Standard (2008) Chapter 7 - Arrays (ARR) | CWE-740-cert-c-secure-coding-standard-chapter-7-arrays |
| CWE-741 | category |  | CERT C Secure Coding Standard Chapter 8 - Characters and Strings | CERT C Secure Coding Standard (2008) Chapter 8 - Characters and Strings (STR) | CWE-741-cert-c-secure-coding-standard-chapter-8-characters |
| CWE-742 | category |  | CERT C Secure Coding Standard Chapter 9 - Memory Management | CERT C Secure Coding Standard (2008) Chapter 9 - Memory Management (MEM) | CWE-742-cert-c-secure-coding-standard-chapter-9-memory |
| CWE-743 | category |  | CERT C Secure Coding Standard Chapter 10 - Input Output | CERT C Secure Coding Standard (2008) Chapter 10 - Input Output (FIO) | CWE-743-cert-c-secure-coding-standard-chapter-10-input |
| CWE-744 | category |  | CERT C Secure Coding Standard Chapter 11 - Environment | CERT C Secure Coding Standard (2008) Chapter 11 - Environment (ENV) | CWE-744-cert-c-secure-coding-standard-chapter-11-environment |
| CWE-745 | category |  | CERT C Secure Coding Standard Chapter 12 - Signals | CERT C Secure Coding Standard (2008) Chapter 12 - Signals (SIG) | CWE-745-cert-c-secure-coding-standard-chapter-12-signals |
| CWE-746 | category |  | CERT C Secure Coding Standard Chapter 13 - Error Handling | CERT C Secure Coding Standard (2008) Chapter 13 - Error Handling (ERR) | CWE-746-cert-c-secure-coding-standard-chapter-13-error |
| CWE-747 | category |  | CERT C Secure Coding Standard Chapter 14 - Miscellaneous | CERT C Secure Coding Standard (2008) Chapter 14 - Miscellaneous (MSC) | CWE-747-cert-c-secure-coding-standard-chapter-14-miscellaneous |
| CWE-748 | category |  | CERT C Secure Coding Standard Appendix - POSIX | CERT C Secure Coding Standard (2008) Appendix - POSIX (POS) | CWE-748-cert-c-secure-coding-standard-appendix-posix |
| CWE-749 | weakness | Base | Exposed Dangerous Method or Function | Exposed Dangerous Method or Function | CWE-749-exposed-dangerous-method-or-function |
| CWE-751 | category |  | 2009 Top 25 - Insecure Interaction Between Components | 2009 Top 25 - Insecure Interaction Between Components | CWE-751-2009-top-25-insecure-interaction-between-components |
| CWE-752 | category |  | 2009 Top 25 - Risky Resource Management | 2009 Top 25 - Risky Resource Management | CWE-752-2009-top-25-risky-resource-management |
| CWE-753 | category |  | 2009 Top 25 - Porous Defenses | 2009 Top 25 - Porous Defenses | CWE-753-2009-top-25-porous-defenses |
| CWE-754 | weakness | Class | Improper Check for Unusual or Exceptional Conditions | Improper Check for Unusual or Exceptional Conditions | CWE-754-improper-check-for-unusual-or-exceptional-conditions |
| CWE-755 | weakness | Class | Improper Handling of Exceptional Conditions | Improper Handling of Exceptional Conditions | CWE-755-improper-handling-of-exceptional-conditions |
| CWE-756 | weakness | Base | Missing Custom Error Page | Missing Custom Error Page | CWE-756-missing-custom-error-page |
| CWE-757 | weakness | Base | Algorithm Downgrade | Selection of Less-Secure Algorithm During Negotiation ('Algorithm Downgrade') | CWE-757-algorithm-downgrade |
| CWE-758 | weakness | Class | Reliance on Undefined, Unspecified, or Implementation-Defined Behavior | Reliance on Undefined, Unspecified, or Implementation-Defined Behavior | CWE-758-reliance-on-undefined-unspecified-or-implementation-defined |
| CWE-759 | weakness | Variant | Use of a One-Way Hash without a Salt | Use of a One-Way Hash without a Salt | CWE-759-one-way-hash-without-salt |
| CWE-760 | weakness | Variant | Use of a One-Way Hash with a Predictable Salt | Use of a One-Way Hash with a Predictable Salt | CWE-760-one-way-hash-with-predictable-salt |
| CWE-761 | weakness | Variant | Free of Pointer not at Start of Buffer | Free of Pointer not at Start of Buffer | CWE-761-free-of-pointer-not-at-start-of-buffer |
| CWE-762 | weakness | Variant | Mismatched Memory Management Routines | Mismatched Memory Management Routines | CWE-762-mismatched-memory-management-routines |
| CWE-763 | weakness | Base | Release of Invalid Pointer or Reference | Release of Invalid Pointer or Reference | CWE-763-release-of-invalid-pointer-or-reference |
| CWE-764 | weakness | Base | Multiple Locks of a Critical Resource | Multiple Locks of a Critical Resource | CWE-764-multiple-locks-of-a-critical-resource |
| CWE-765 | weakness | Base | Multiple Unlocks of a Critical Resource | Multiple Unlocks of a Critical Resource | CWE-765-multiple-unlocks-of-a-critical-resource |
| CWE-766 | weakness | Base | Failure to protect stored data from modification | Critical Data Element Declared Public | CWE-766-failure-to-protect-stored-data-from-modification |
| CWE-767 | weakness | Base | Failure to protect stored data from modification | Access to Critical Private Variable via Public Method | CWE-767-failure-to-protect-stored-data-from-modification |
| CWE-768 | weakness | Variant | Failure to protect stored data from modification | Incorrect Short Circuit Evaluation | CWE-768-failure-to-protect-stored-data-from-modification |
| CWE-769 | weakness | Base | DEPRECATED: Uncontrolled File Descriptor Consumption | DEPRECATED: Uncontrolled File Descriptor Consumption | CWE-769-deprecated-uncontrolled-file-descriptor-consumption |
| CWE-770 | weakness | Base | Allocation of Resources Without Limits or Throttling | Allocation of Resources Without Limits or Throttling | CWE-770-allocation-of-resources-without-limits-or-throttling |
| CWE-771 | weakness | Base | Missing Reference to Active Allocated Resource | Missing Reference to Active Allocated Resource | CWE-771-missing-reference-to-active-allocated-resource |
| CWE-772 | weakness | Base | Missing Release of Resource after Effective Lifetime | Missing Release of Resource after Effective Lifetime | CWE-772-missing-release-of-resource-after-effective-lifetime |
| CWE-773 | weakness | Variant | Missing Reference to Active File Descriptor or Handle | Missing Reference to Active File Descriptor or Handle | CWE-773-missing-reference-to-active-file-descriptor-or-handle |
| CWE-774 | weakness | Variant | Allocation of File Descriptors or Handles Without Limits or Throttling | Allocation of File Descriptors or Handles Without Limits or Throttling | CWE-774-allocation-file-descriptors-handles-without-limits |
| CWE-775 | weakness | Variant | Missing Release of File Descriptor or Handle after Effective Lifetime | Missing Release of File Descriptor or Handle after Effective Lifetime | CWE-775-missing-release-file-descriptor-handle-after-effective |
| CWE-776 | weakness | Base | XML Entity Expansion | Improper Restriction of Recursive Entity References in DTDs ('XML Entity Expansion') | CWE-776-xml-entity-expansion |
| CWE-777 | weakness | Variant | Regular Expression without Anchors | Regular Expression without Anchors | CWE-777-regular-expression-without-anchors |
| CWE-778 | weakness | Base | Insufficient Logging | Insufficient Logging | CWE-778-insufficient-logging |
| CWE-779 | weakness | Base | Logging of Excessive Data | Logging of Excessive Data | CWE-779-logging-of-excessive-data |
| CWE-780 | weakness | Variant | Use of RSA Algorithm without OAEP | Use of RSA Algorithm without OAEP | CWE-780-use-of-rsa-algorithm-without-oaep |
| CWE-781 | weakness | Variant | Improper Address Validation in IOCTL with METHOD_NEITHER I/O Control Code | Improper Address Validation in IOCTL with METHOD_NEITHER I/O Control Code | CWE-781-improper-address-validation-ioctl-with-method-neither-i |
| CWE-782 | weakness | Variant | Exposed IOCTL with Insufficient Access Control | Exposed IOCTL with Insufficient Access Control | CWE-782-exposed-ioctl-with-insufficient-access-control |
| CWE-783 | weakness | Base | Operator Precedence Logic Error | Operator Precedence Logic Error | CWE-783-operator-precedence-logic-error |
| CWE-784 | weakness | Variant | Reliance on Cookies without Validation and Integrity Checking in a Security Decision | Reliance on Cookies without Validation and Integrity Checking in a Security Decision | CWE-784-reliance-on-cookies-without-validation-integrity-checking |
| CWE-785 | weakness | Variant | Often Misused: File System | Use of Path Manipulation Function without Maximum-sized Buffer | CWE-785-often-misused-file-system |
| CWE-786 | weakness | Base | Access of Memory Location Before Start of Buffer | Access of Memory Location Before Start of Buffer | CWE-786-access-of-memory-location-before-start-of-buffer |
| CWE-787 | weakness | Base | Out-of-bounds Write | Out-of-bounds Write | CWE-787-out-of-bounds-write |
| CWE-788 | weakness | Base | Access of Memory Location After End of Buffer | Access of Memory Location After End of Buffer | CWE-788-access-of-memory-location-after-end-of-buffer |
| CWE-789 | weakness | Variant | SOAP Array Abuse | Memory Allocation with Excessive Size Value | CWE-789-soap-array-abuse |
| CWE-790 | weakness | Class | Improper Filtering of Special Elements | Improper Filtering of Special Elements | CWE-790-improper-filtering-of-special-elements |
| CWE-791 | weakness | Base | Incomplete Filtering of Special Elements | Incomplete Filtering of Special Elements | CWE-791-incomplete-filtering-of-special-elements |
| CWE-792 | weakness | Variant | Incomplete Filtering of One or More Instances of Special Elements | Incomplete Filtering of One or More Instances of Special Elements | CWE-792-incomplete-filtering-one-more-instances-special-elements |
| CWE-793 | weakness | Variant | Only Filtering One Instance of a Special Element | Only Filtering One Instance of a Special Element | CWE-793-only-filtering-one-instance-of-a-special-element |
| CWE-794 | weakness | Variant | Incomplete Filtering of Multiple Instances of Special Elements | Incomplete Filtering of Multiple Instances of Special Elements | CWE-794-incomplete-filtering-of-multiple-instances-of-special |
| CWE-795 | weakness | Base | Only Filtering Special Elements at a Specified Location | Only Filtering Special Elements at a Specified Location | CWE-795-only-filtering-special-elements-at-a-specified-location |
| CWE-796 | weakness | Variant | Only Filtering Special Elements Relative to a Marker | Only Filtering Special Elements Relative to a Marker | CWE-796-only-filtering-special-elements-relative-to-a-marker |
| CWE-797 | weakness | Variant | Only Filtering Special Elements at an Absolute Position | Only Filtering Special Elements at an Absolute Position | CWE-797-only-filtering-special-elements-at-an-absolute-position |
| CWE-798 | weakness | Base | Use of Hard-coded Credentials | Use of Hard-coded Credentials | CWE-798-use-of-hard-coded-credentials |
| CWE-799 | weakness | Class | Insufficient Anti-Automation | Improper Control of Interaction Frequency | CWE-799-insufficient-anti-automation |
| CWE-801 | category |  | 2010 Top 25 - Insecure Interaction Between Components | 2010 Top 25 - Insecure Interaction Between Components | CWE-801-2010-top-25-insecure-interaction-between-components |
| CWE-802 | category |  | 2010 Top 25 - Risky Resource Management | 2010 Top 25 - Risky Resource Management | CWE-802-2010-top-25-risky-resource-management |
| CWE-803 | category |  | 2010 Top 25 - Porous Defenses | 2010 Top 25 - Porous Defenses | CWE-803-2010-top-25-porous-defenses |
| CWE-804 | weakness | Base | Insufficient Anti-Automation | Guessable CAPTCHA | CWE-804-insufficient-anti-automation |
| CWE-805 | weakness | Base | Buffer Access with Incorrect Length Value | Buffer Access with Incorrect Length Value | CWE-805-buffer-access-with-incorrect-length-value |
| CWE-806 | weakness | Variant | Buffer Access Using Size of Source Buffer | Buffer Access Using Size of Source Buffer | CWE-806-buffer-access-using-size-of-source-buffer |
| CWE-807 | weakness | Base | Reliance on Untrusted Inputs in a Security Decision | Reliance on Untrusted Inputs in a Security Decision | CWE-807-reliance-on-untrusted-inputs-in-a-security-decision |
| CWE-808 | category |  | 2010 Top 25 - Weaknesses On the Cusp | 2010 Top 25 - Weaknesses On the Cusp | CWE-808-2010-top-25-weaknesses-on-the-cusp |
| CWE-810 | category |  | OWASP Top Ten 2010 Category A1 - Injection | OWASP Top Ten 2010 Category A1 - Injection | CWE-810-owasp-top-ten-2010-category-a1-injection |
| CWE-811 | category |  | OWASP Top Ten 2010 Category A2 - Cross-Site Scripting | OWASP Top Ten 2010 Category A2 - Cross-Site Scripting (XSS) | CWE-811-owasp-top-ten-2010-category-a2-cross-site |
| CWE-812 | category |  | OWASP Top Ten 2010 Category A3 - Broken Authentication and Session Management | OWASP Top Ten 2010 Category A3 - Broken Authentication and Session Management | CWE-812-owasp-top-ten-2010-category-a3-broken-authentication |
| CWE-813 | category |  | OWASP Top Ten 2010 Category A4 - Insecure Direct Object References | OWASP Top Ten 2010 Category A4 - Insecure Direct Object References | CWE-813-owasp-top-ten-2010-category-a4-insecure-direct |
| CWE-814 | category |  | OWASP Top Ten 2010 Category A5 - Cross-Site Request Forgery | OWASP Top Ten 2010 Category A5 - Cross-Site Request Forgery(CSRF) | CWE-814-owasp-top-ten-2010-category-a5-cross-site |
| CWE-815 | category |  | OWASP Top Ten 2010 Category A6 - Security Misconfiguration | OWASP Top Ten 2010 Category A6 - Security Misconfiguration | CWE-815-owasp-top-ten-2010-category-a6-security-misconfiguration |
| CWE-816 | category |  | OWASP Top Ten 2010 Category A7 - Insecure Cryptographic Storage | OWASP Top Ten 2010 Category A7 - Insecure Cryptographic Storage | CWE-816-owasp-top-ten-2010-category-a7-insecure-cryptographic |
| CWE-817 | category |  | OWASP Top Ten 2010 Category A8 - Failure to Restrict URL Access | OWASP Top Ten 2010 Category A8 - Failure to Restrict URL Access | CWE-817-owasp-top-ten-2010-category-a8-failure-restrict |
| CWE-818 | category |  | OWASP Top Ten 2010 Category A9 - Insufficient Transport Layer Protection | OWASP Top Ten 2010 Category A9 - Insufficient Transport Layer Protection | CWE-818-owasp-top-ten-2010-category-a9-insufficient-transport |
| CWE-819 | category |  | OWASP Top Ten 2010 Category A10 - Unvalidated Redirects and Forwards | OWASP Top Ten 2010 Category A10 - Unvalidated Redirects and Forwards | CWE-819-owasp-top-ten-2010-category-a10-unvalidated-redirects |
| CWE-820 | weakness | Base | Missing Synchronization | Missing Synchronization | CWE-820-missing-synchronization |
| CWE-821 | weakness | Base | Incorrect Synchronization | Incorrect Synchronization | CWE-821-incorrect-synchronization |
| CWE-822 | weakness | Base | Untrusted Pointer Dereference | Untrusted Pointer Dereference | CWE-822-untrusted-pointer-dereference |
| CWE-823 | weakness | Base | Use of Out-of-range Pointer Offset | Use of Out-of-range Pointer Offset | CWE-823-use-of-out-of-range-pointer-offset |
| CWE-824 | weakness | Base | Access of Uninitialized Pointer | Access of Uninitialized Pointer | CWE-824-access-of-uninitialized-pointer |
| CWE-825 | weakness | Base | Expired Pointer Dereference | Expired Pointer Dereference | CWE-825-expired-pointer-dereference |
| CWE-826 | weakness | Base | Premature Release of Resource During Expected Lifetime | Premature Release of Resource During Expected Lifetime | CWE-826-premature-release-of-resource-during-expected-lifetime |
| CWE-827 | weakness | Variant | Improper Control of Document Type Definition | Improper Control of Document Type Definition | CWE-827-improper-control-of-document-type-definition |
| CWE-828 | weakness | Variant | Signal Handler with Functionality that is not Asynchronous-Safe | Signal Handler with Functionality that is not Asynchronous-Safe | CWE-828-signal-handler-with-functionality-that-is-not-asynchronous |
| CWE-829 | weakness | Base | Inclusion of Functionality from Untrusted Control Sphere | Inclusion of Functionality from Untrusted Control Sphere | CWE-829-inclusion-of-functionality-from-untrusted-control-sphere |
| CWE-830 | weakness | Variant | Inclusion of Web Functionality from an Untrusted Source | Inclusion of Web Functionality from an Untrusted Source | CWE-830-inclusion-of-web-functionality-from-an-untrusted-source |
| CWE-831 | weakness | Variant | Signal Handler Function Associated with Multiple Signals | Signal Handler Function Associated with Multiple Signals | CWE-831-signal-handler-function-associated-with-multiple-signals |
| CWE-832 | weakness | Base | Unlock of a Resource that is not Locked | Unlock of a Resource that is not Locked | CWE-832-unlock-of-a-resource-that-is-not-locked |
| CWE-833 | weakness | Base | Deadlock | Deadlock | CWE-833-deadlock |
| CWE-834 | weakness | Class | Excessive Iteration | Excessive Iteration | CWE-834-excessive-iteration |
| CWE-835 | weakness | Base | Infinite Loop | Loop with Unreachable Exit Condition ('Infinite Loop') | CWE-835-infinite-loop |
| CWE-836 | weakness | Base | Use of Password Hash Instead of Password for Authentication | Use of Password Hash Instead of Password for Authentication | CWE-836-password-hash-instead-password-for-authentication |
| CWE-837 | weakness | Base | Improper Enforcement of a Single, Unique Action | Improper Enforcement of a Single, Unique Action | CWE-837-improper-enforcement-of-a-single-unique-action |
| CWE-838 | weakness | Base | Inappropriate Encoding for Output Context | Inappropriate Encoding for Output Context | CWE-838-inappropriate-encoding-for-output-context |
| CWE-839 | weakness | Base | Numeric Range Comparison Without Minimum Check | Numeric Range Comparison Without Minimum Check | CWE-839-numeric-range-comparison-without-minimum-check |
| CWE-840 | category |  | Business Logic Errors | Business Logic Errors | CWE-840-business-logic-errors |
| CWE-841 | weakness | Class | Insufficient Process Validation | Improper Enforcement of Behavioral Workflow | CWE-841-insufficient-process-validation |
| CWE-842 | weakness | Base | Placement of User into Incorrect Group | Placement of User into Incorrect Group | CWE-842-placement-of-user-into-incorrect-group |
| CWE-843 | weakness | Base | Type Confusion | Access of Resource Using Incompatible Type ('Type Confusion') | CWE-843-type-confusion |
| CWE-845 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 2 - Input Validation and Data Sanitization | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 2 - Input Validation and Data Sanitization (IDS) | CWE-845-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-846 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 3 - Declarations and Initialization | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 3 - Declarations and Initialization (DCL) | CWE-846-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-847 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 4 - Expressions | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 4 - Expressions (EXP) | CWE-847-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-848 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 5 - Numeric Types and Operations | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 5 - Numeric Types and Operations (NUM) | CWE-848-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-849 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 6 - Object Orientation | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 6 - Object Orientation (OBJ) | CWE-849-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-850 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 7 - Methods | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 7 - Methods (MET) | CWE-850-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-851 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 8 - Exceptional Behavior | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 8 - Exceptional Behavior (ERR) | CWE-851-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-852 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 9 - Visibility and Atomicity | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 9 - Visibility and Atomicity (VNA) | CWE-852-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-853 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 10 - Locking | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 10 - Locking (LCK) | CWE-853-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-854 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 11 - Thread APIs | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 11 - Thread APIs (THI) | CWE-854-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-855 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 12 - Thread Pools | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 12 - Thread Pools (TPS) | CWE-855-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-856 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 13 - Thread-Safety Miscellaneous | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 13 - Thread-Safety Miscellaneous (TSM) | CWE-856-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-857 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 14 - Input Output | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 14 - Input Output (FIO) | CWE-857-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-858 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 15 - Serialization | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 15 - Serialization (SER) | CWE-858-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-859 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 16 - Platform Security | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 16 - Platform Security (SEC) | CWE-859-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-860 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 17 - Runtime Environment | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 17 - Runtime Environment (ENV) | CWE-860-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-861 | category |  | The CERT Oracle Secure Coding Standard for Java Chapter 18 - Miscellaneous | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 18 - Miscellaneous (MSC) | CWE-861-cert-oracle-secure-coding-standard-for-java-chapter |
| CWE-862 | weakness | Class | Missing Authorization | Missing Authorization | CWE-862-missing-authorization |
| CWE-863 | weakness | Class | Incorrect Authorization | Incorrect Authorization | CWE-863-incorrect-authorization |
| CWE-864 | category |  | 2011 Top 25 - Insecure Interaction Between Components | 2011 Top 25 - Insecure Interaction Between Components | CWE-864-2011-top-25-insecure-interaction-between-components |
| CWE-865 | category |  | 2011 Top 25 - Risky Resource Management | 2011 Top 25 - Risky Resource Management | CWE-865-2011-top-25-risky-resource-management |
| CWE-866 | category |  | 2011 Top 25 - Porous Defenses | 2011 Top 25 - Porous Defenses | CWE-866-2011-top-25-porous-defenses |
| CWE-867 | category |  | 2011 Top 25 - Weaknesses On the Cusp | 2011 Top 25 - Weaknesses On the Cusp | CWE-867-2011-top-25-weaknesses-on-the-cusp |
| CWE-869 | category |  | CERT C++ Secure Coding Section 01 - Preprocessor | CERT C++ Secure Coding Section 01 - Preprocessor (PRE) | CWE-869-cert-c-secure-coding-section-01-preprocessor |
| CWE-870 | category |  | CERT C++ Secure Coding Section 02 - Declarations and Initialization | CERT C++ Secure Coding Section 02 - Declarations and Initialization (DCL) | CWE-870-cert-c-secure-coding-section-02-declarations-initialization |
| CWE-871 | category |  | CERT C++ Secure Coding Section 03 - Expressions | CERT C++ Secure Coding Section 03 - Expressions (EXP) | CWE-871-cert-c-secure-coding-section-03-expressions |
| CWE-872 | category |  | CERT C++ Secure Coding Section 04 - Integers | CERT C++ Secure Coding Section 04 - Integers (INT) | CWE-872-cert-c-secure-coding-section-04-integers |
| CWE-873 | category |  | CERT C++ Secure Coding Section 05 - Floating Point Arithmetic | CERT C++ Secure Coding Section 05 - Floating Point Arithmetic (FLP) | CWE-873-cert-c-secure-coding-section-05-floating-point |
| CWE-874 | category |  | CERT C++ Secure Coding Section 06 - Arrays and the STL | CERT C++ Secure Coding Section 06 - Arrays and the STL (ARR) | CWE-874-cert-c-secure-coding-section-06-arrays-stl |
| CWE-875 | category |  | CERT C++ Secure Coding Section 07 - Characters and Strings | CERT C++ Secure Coding Section 07 - Characters and Strings (STR) | CWE-875-cert-c-secure-coding-section-07-characters-strings |
| CWE-876 | category |  | CERT C++ Secure Coding Section 08 - Memory Management | CERT C++ Secure Coding Section 08 - Memory Management (MEM) | CWE-876-cert-c-secure-coding-section-08-memory-management |
| CWE-877 | category |  | CERT C++ Secure Coding Section 09 - Input Output | CERT C++ Secure Coding Section 09 - Input Output (FIO) | CWE-877-cert-c-secure-coding-section-09-input-output |
| CWE-878 | category |  | CERT C++ Secure Coding Section 10 - Environment | CERT C++ Secure Coding Section 10 - Environment (ENV) | CWE-878-cert-c-secure-coding-section-10-environment |
| CWE-879 | category |  | CERT C++ Secure Coding Section 11 - Signals | CERT C++ Secure Coding Section 11 - Signals (SIG) | CWE-879-cert-c-secure-coding-section-11-signals |
| CWE-880 | category |  | CERT C++ Secure Coding Section 12 - Exceptions and Error Handling | CERT C++ Secure Coding Section 12 - Exceptions and Error Handling (ERR) | CWE-880-cert-c-secure-coding-section-12-exceptions-error |
| CWE-881 | category |  | CERT C++ Secure Coding Section 13 - Object Oriented Programming | CERT C++ Secure Coding Section 13 - Object Oriented Programming (OOP) | CWE-881-cert-c-secure-coding-section-13-object-oriented |
| CWE-882 | category |  | CERT C++ Secure Coding Section 14 - Concurrency | CERT C++ Secure Coding Section 14 - Concurrency (CON) | CWE-882-cert-c-secure-coding-section-14-concurrency |
| CWE-883 | category |  | CERT C++ Secure Coding Section 49 - Miscellaneous | CERT C++ Secure Coding Section 49 - Miscellaneous (MSC) | CWE-883-cert-c-secure-coding-section-49-miscellaneous |
| CWE-885 | category |  | SFP Primary Cluster: Risky Values | SFP Primary Cluster: Risky Values | CWE-885-sfp-primary-cluster-risky-values |
| CWE-886 | category |  | SFP Primary Cluster: Unused entities | SFP Primary Cluster: Unused entities | CWE-886-sfp-primary-cluster-unused-entities |
| CWE-887 | category |  | SFP Primary Cluster: API | SFP Primary Cluster: API | CWE-887-sfp-primary-cluster-api |
| CWE-889 | category |  | SFP Primary Cluster: Exception Management | SFP Primary Cluster: Exception Management | CWE-889-sfp-primary-cluster-exception-management |
| CWE-890 | category |  | SFP Primary Cluster: Memory Access | SFP Primary Cluster: Memory Access | CWE-890-sfp-primary-cluster-memory-access |
| CWE-891 | category |  | SFP Primary Cluster: Memory Management | SFP Primary Cluster: Memory Management | CWE-891-sfp-primary-cluster-memory-management |
| CWE-892 | category |  | SFP Primary Cluster: Resource Management | SFP Primary Cluster: Resource Management | CWE-892-sfp-primary-cluster-resource-management |
| CWE-893 | category |  | SFP Primary Cluster: Path Resolution | SFP Primary Cluster: Path Resolution | CWE-893-sfp-primary-cluster-path-resolution |
| CWE-894 | category |  | SFP Primary Cluster: Synchronization | SFP Primary Cluster: Synchronization | CWE-894-sfp-primary-cluster-synchronization |
| CWE-895 | category |  | SFP Primary Cluster: Information Leak | SFP Primary Cluster: Information Leak | CWE-895-sfp-primary-cluster-information-leak |
| CWE-896 | category |  | SFP Primary Cluster: Tainted Input | SFP Primary Cluster: Tainted Input | CWE-896-sfp-primary-cluster-tainted-input |
| CWE-897 | category |  | SFP Primary Cluster: Entry Points | SFP Primary Cluster: Entry Points | CWE-897-sfp-primary-cluster-entry-points |
| CWE-898 | category |  | SFP Primary Cluster: Authentication | SFP Primary Cluster: Authentication | CWE-898-sfp-primary-cluster-authentication |
| CWE-899 | category |  | SFP Primary Cluster: Access Control | SFP Primary Cluster: Access Control | CWE-899-sfp-primary-cluster-access-control |
| CWE-901 | category |  | SFP Primary Cluster: Privilege | SFP Primary Cluster: Privilege | CWE-901-sfp-primary-cluster-privilege |
| CWE-902 | category |  | SFP Primary Cluster: Channel | SFP Primary Cluster: Channel | CWE-902-sfp-primary-cluster-channel |
| CWE-903 | category |  | SFP Primary Cluster: Cryptography | SFP Primary Cluster: Cryptography | CWE-903-sfp-primary-cluster-cryptography |
| CWE-904 | category |  | SFP Primary Cluster: Malware | SFP Primary Cluster: Malware | CWE-904-sfp-primary-cluster-malware |
| CWE-905 | category |  | SFP Primary Cluster: Predictability | SFP Primary Cluster: Predictability | CWE-905-sfp-primary-cluster-predictability |
| CWE-906 | category |  | SFP Primary Cluster: UI | SFP Primary Cluster: UI | CWE-906-sfp-primary-cluster-ui |
| CWE-907 | category |  | SFP Primary Cluster: Other | SFP Primary Cluster: Other | CWE-907-sfp-primary-cluster-other |
| CWE-908 | weakness | Base | Use of Uninitialized Resource | Use of Uninitialized Resource | CWE-908-use-of-uninitialized-resource |
| CWE-909 | weakness | Class | Missing Initialization of Resource | Missing Initialization of Resource | CWE-909-missing-initialization-of-resource |
| CWE-910 | weakness | Base | Use of Expired File Descriptor | Use of Expired File Descriptor | CWE-910-use-of-expired-file-descriptor |
| CWE-911 | weakness | Base | Improper Update of Reference Count | Improper Update of Reference Count | CWE-911-improper-update-of-reference-count |
| CWE-912 | weakness | Class | Hidden Functionality | Hidden Functionality | CWE-912-hidden-functionality |
| CWE-913 | weakness | Class | Improper Control of Dynamically-Managed Code Resources | Improper Control of Dynamically-Managed Code Resources | CWE-913-improper-control-of-dynamically-managed-code-resources |
| CWE-914 | weakness | Base | Improper Control of Dynamically-Identified Variables | Improper Control of Dynamically-Identified Variables | CWE-914-improper-control-of-dynamically-identified-variables |
| CWE-915 | weakness | Base | Improperly Controlled Modification of Dynamically-Determined Object Attributes | Improperly Controlled Modification of Dynamically-Determined Object Attributes | CWE-915-improperly-controlled-modification-of-dynamically-determined |
| CWE-916 | weakness | Base | Use of Password Hash With Insufficient Computational Effort | Use of Password Hash With Insufficient Computational Effort | CWE-916-use-of-password-hash-with-insufficient-computational-effort |
| CWE-917 | weakness | Base | Expression Language Injection | Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection') | CWE-917-expression-language-injection |
| CWE-918 | weakness | Base | Server-Side Request Forgery | Server-Side Request Forgery (SSRF) | CWE-918-server-side-request-forgery |
| CWE-920 | weakness | Base | Improper Restriction of Power Consumption | Improper Restriction of Power Consumption | CWE-920-improper-restriction-of-power-consumption |
| CWE-921 | weakness | Base | Storage of Sensitive Data in a Mechanism without Access Control | Storage of Sensitive Data in a Mechanism without Access Control | CWE-921-storage-sensitive-data-mechanism-without-access-control |
| CWE-922 | weakness | Class | Insecure Storage of Sensitive Information | Insecure Storage of Sensitive Information | CWE-922-insecure-storage-of-sensitive-information |
| CWE-923 | weakness | Class | Improper Restriction of Communication Channel to Intended Endpoints | Improper Restriction of Communication Channel to Intended Endpoints | CWE-923-improper-restriction-of-communication-channel-to-intended |
| CWE-924 | weakness | Base | Improper Enforcement of Message Integrity During Transmission in a Communication Channel | Improper Enforcement of Message Integrity During Transmission in a Communication Channel | CWE-924-improper-enforcement-message-integrity-during-transmission |
| CWE-925 | weakness | Variant | Improper Verification of Intent by Broadcast Receiver | Improper Verification of Intent by Broadcast Receiver | CWE-925-improper-verification-of-intent-by-broadcast-receiver |
| CWE-926 | weakness | Variant | Improper Export of Android Application Components | Improper Export of Android Application Components | CWE-926-improper-export-of-android-application-components |
| CWE-927 | weakness | Variant | Use of Implicit Intent for Sensitive Communication | Use of Implicit Intent for Sensitive Communication | CWE-927-use-of-implicit-intent-for-sensitive-communication |
| CWE-929 | category |  | OWASP Top Ten 2013 Category A1 - Injection | OWASP Top Ten 2013 Category A1 - Injection | CWE-929-owasp-top-ten-2013-category-a1-injection |
| CWE-930 | category |  | OWASP Top Ten 2013 Category A2 - Broken Authentication and Session Management | OWASP Top Ten 2013 Category A2 - Broken Authentication and Session Management | CWE-930-owasp-top-ten-2013-category-a2-broken-authentication |
| CWE-931 | category |  | OWASP Top Ten 2013 Category A3 - Cross-Site Scripting | OWASP Top Ten 2013 Category A3 - Cross-Site Scripting (XSS) | CWE-931-owasp-top-ten-2013-category-a3-cross-site |
| CWE-932 | category |  | OWASP Top Ten 2013 Category A4 - Insecure Direct Object References | OWASP Top Ten 2013 Category A4 - Insecure Direct Object References | CWE-932-owasp-top-ten-2013-category-a4-insecure-direct |
| CWE-933 | category |  | OWASP Top Ten 2013 Category A5 - Security Misconfiguration | OWASP Top Ten 2013 Category A5 - Security Misconfiguration | CWE-933-owasp-top-ten-2013-category-a5-security-misconfiguration |
| CWE-934 | category |  | OWASP Top Ten 2013 Category A6 - Sensitive Data Exposure | OWASP Top Ten 2013 Category A6 - Sensitive Data Exposure | CWE-934-owasp-top-ten-2013-category-a6-sensitive-data |
| CWE-935 | category |  | OWASP Top Ten 2013 Category A7 - Missing Function Level Access Control | OWASP Top Ten 2013 Category A7 - Missing Function Level Access Control | CWE-935-owasp-top-ten-2013-category-a7-missing-function |
| CWE-936 | category |  | OWASP Top Ten 2013 Category A8 - Cross-Site Request Forgery | OWASP Top Ten 2013 Category A8 - Cross-Site Request Forgery (CSRF) | CWE-936-owasp-top-ten-2013-category-a8-cross-site |
| CWE-937 | category |  | OWASP Top Ten 2013 Category A9 - Using Components with Known Vulnerabilities | OWASP Top Ten 2013 Category A9 - Using Components with Known Vulnerabilities | CWE-937-owasp-top-ten-2013-category-a9-components-with |
| CWE-938 | category |  | OWASP Top Ten 2013 Category A10 - Unvalidated Redirects and Forwards | OWASP Top Ten 2013 Category A10 - Unvalidated Redirects and Forwards | CWE-938-owasp-top-ten-2013-category-a10-unvalidated-redirects |
| CWE-939 | weakness | Base | Improper Authorization in Handler for Custom URL Scheme | Improper Authorization in Handler for Custom URL Scheme | CWE-939-improper-authorization-in-handler-for-custom-url-scheme |
| CWE-940 | weakness | Base | Improper Verification of Source of a Communication Channel | Improper Verification of Source of a Communication Channel | CWE-940-improper-verification-of-source-of-a-communication-channel |
| CWE-941 | weakness | Base | Incorrectly Specified Destination in a Communication Channel | Incorrectly Specified Destination in a Communication Channel | CWE-941-incorrectly-specified-destination-in-a-communication-channel |
| CWE-942 | weakness | Variant | Permissive Cross-domain Security Policy with Untrusted Domains | Permissive Cross-domain Security Policy with Untrusted Domains | CWE-942-permissive-cross-domain-security-policy-with-untrusted |
| CWE-943 | weakness | Class | Improper Neutralization of Special Elements in Data Query Logic | Improper Neutralization of Special Elements in Data Query Logic | CWE-943-improper-neutralization-special-elements-data-query-logic |
| CWE-944 | category |  | SFP Secondary Cluster: Access Management | SFP Secondary Cluster: Access Management | CWE-944-sfp-secondary-cluster-access-management |
| CWE-945 | category |  | SFP Secondary Cluster: Insecure Resource Access | SFP Secondary Cluster: Insecure Resource Access | CWE-945-sfp-secondary-cluster-insecure-resource-access |
| CWE-946 | category |  | SFP Secondary Cluster: Insecure Resource Permissions | SFP Secondary Cluster: Insecure Resource Permissions | CWE-946-sfp-secondary-cluster-insecure-resource-permissions |
| CWE-947 | category |  | SFP Secondary Cluster: Authentication Bypass | SFP Secondary Cluster: Authentication Bypass | CWE-947-sfp-secondary-cluster-authentication-bypass |
| CWE-948 | category |  | SFP Secondary Cluster: Digital Certificate | SFP Secondary Cluster: Digital Certificate | CWE-948-sfp-secondary-cluster-digital-certificate |
| CWE-949 | category |  | SFP Secondary Cluster: Faulty Endpoint Authentication | SFP Secondary Cluster: Faulty Endpoint Authentication | CWE-949-sfp-secondary-cluster-faulty-endpoint-authentication |
| CWE-950 | category |  | SFP Secondary Cluster: Hardcoded Sensitive Data | SFP Secondary Cluster: Hardcoded Sensitive Data | CWE-950-sfp-secondary-cluster-hardcoded-sensitive-data |
| CWE-951 | category |  | SFP Secondary Cluster: Insecure Authentication Policy | SFP Secondary Cluster: Insecure Authentication Policy | CWE-951-sfp-secondary-cluster-insecure-authentication-policy |
| CWE-952 | category |  | SFP Secondary Cluster: Missing Authentication | SFP Secondary Cluster: Missing Authentication | CWE-952-sfp-secondary-cluster-missing-authentication |
| CWE-953 | category |  | SFP Secondary Cluster: Missing Endpoint Authentication | SFP Secondary Cluster: Missing Endpoint Authentication | CWE-953-sfp-secondary-cluster-missing-endpoint-authentication |
| CWE-954 | category |  | SFP Secondary Cluster: Multiple Binds to the Same Port | SFP Secondary Cluster: Multiple Binds to the Same Port | CWE-954-sfp-secondary-cluster-multiple-binds-same-port |
| CWE-955 | category |  | SFP Secondary Cluster: Unrestricted Authentication | SFP Secondary Cluster: Unrestricted Authentication | CWE-955-sfp-secondary-cluster-unrestricted-authentication |
| CWE-956 | category |  | SFP Secondary Cluster: Channel Attack | SFP Secondary Cluster: Channel Attack | CWE-956-sfp-secondary-cluster-channel-attack |
| CWE-957 | category |  | SFP Secondary Cluster: Protocol Error | SFP Secondary Cluster: Protocol Error | CWE-957-sfp-secondary-cluster-protocol-error |
| CWE-958 | category |  | SFP Secondary Cluster: Broken Cryptography | SFP Secondary Cluster: Broken Cryptography | CWE-958-sfp-secondary-cluster-broken-cryptography |
| CWE-959 | category |  | SFP Secondary Cluster: Weak Cryptography | SFP Secondary Cluster: Weak Cryptography | CWE-959-sfp-secondary-cluster-weak-cryptography |
| CWE-960 | category |  | SFP Secondary Cluster: Ambiguous Exception Type | SFP Secondary Cluster: Ambiguous Exception Type | CWE-960-sfp-secondary-cluster-ambiguous-exception-type |
| CWE-961 | category |  | SFP Secondary Cluster: Incorrect Exception Behavior | SFP Secondary Cluster: Incorrect Exception Behavior | CWE-961-sfp-secondary-cluster-incorrect-exception-behavior |
| CWE-962 | category |  | SFP Secondary Cluster: Unchecked Status Condition | SFP Secondary Cluster: Unchecked Status Condition | CWE-962-sfp-secondary-cluster-unchecked-status-condition |
| CWE-963 | category |  | SFP Secondary Cluster: Exposed Data | SFP Secondary Cluster: Exposed Data | CWE-963-sfp-secondary-cluster-exposed-data |
| CWE-964 | category |  | SFP Secondary Cluster: Exposure Temporary File | SFP Secondary Cluster: Exposure Temporary File | CWE-964-sfp-secondary-cluster-exposure-temporary-file |
| CWE-965 | category |  | SFP Secondary Cluster: Insecure Session Management | SFP Secondary Cluster: Insecure Session Management | CWE-965-sfp-secondary-cluster-insecure-session-management |
| CWE-966 | category |  | SFP Secondary Cluster: Other Exposures | SFP Secondary Cluster: Other Exposures | CWE-966-sfp-secondary-cluster-other-exposures |
| CWE-967 | category |  | SFP Secondary Cluster: State Disclosure | SFP Secondary Cluster: State Disclosure | CWE-967-sfp-secondary-cluster-state-disclosure |
| CWE-968 | category |  | SFP Secondary Cluster: Covert Channel | SFP Secondary Cluster: Covert Channel | CWE-968-sfp-secondary-cluster-covert-channel |
| CWE-969 | category |  | SFP Secondary Cluster: Faulty Memory Release | SFP Secondary Cluster: Faulty Memory Release | CWE-969-sfp-secondary-cluster-faulty-memory-release |
| CWE-970 | category |  | SFP Secondary Cluster: Faulty Buffer Access | SFP Secondary Cluster: Faulty Buffer Access | CWE-970-sfp-secondary-cluster-faulty-buffer-access |
| CWE-971 | category |  | SFP Secondary Cluster: Faulty Pointer Use | SFP Secondary Cluster: Faulty Pointer Use | CWE-971-sfp-secondary-cluster-faulty-pointer-use |
| CWE-972 | category |  | SFP Secondary Cluster: Faulty String Expansion | SFP Secondary Cluster: Faulty String Expansion | CWE-972-sfp-secondary-cluster-faulty-string-expansion |
| CWE-973 | category |  | SFP Secondary Cluster: Improper NULL Termination | SFP Secondary Cluster: Improper NULL Termination | CWE-973-sfp-secondary-cluster-improper-null-termination |
| CWE-974 | category |  | SFP Secondary Cluster: Incorrect Buffer Length Computation | SFP Secondary Cluster: Incorrect Buffer Length Computation | CWE-974-sfp-secondary-cluster-incorrect-buffer-length-computation |
| CWE-975 | category |  | SFP Secondary Cluster: Architecture | SFP Secondary Cluster: Architecture | CWE-975-sfp-secondary-cluster-architecture |
| CWE-976 | category |  | SFP Secondary Cluster: Compiler | SFP Secondary Cluster: Compiler | CWE-976-sfp-secondary-cluster-compiler |
| CWE-977 | category |  | SFP Secondary Cluster: Design | SFP Secondary Cluster: Design | CWE-977-sfp-secondary-cluster-design |
| CWE-978 | category |  | SFP Secondary Cluster: Implementation | SFP Secondary Cluster: Implementation | CWE-978-sfp-secondary-cluster-implementation |
| CWE-979 | category |  | SFP Secondary Cluster: Failed Chroot Jail | SFP Secondary Cluster: Failed Chroot Jail | CWE-979-sfp-secondary-cluster-failed-chroot-jail |
| CWE-980 | category |  | SFP Secondary Cluster: Link in Resource Name Resolution | SFP Secondary Cluster: Link in Resource Name Resolution | CWE-980-sfp-secondary-cluster-link-in-resource-name-resolution |
| CWE-981 | category |  | SFP Secondary Cluster: Path Traversal | SFP Secondary Cluster: Path Traversal | CWE-981-sfp-secondary-cluster-path-traversal |
| CWE-982 | category |  | SFP Secondary Cluster: Failure to Release Resource | SFP Secondary Cluster: Failure to Release Resource | CWE-982-sfp-secondary-cluster-failure-to-release-resource |
| CWE-983 | category |  | SFP Secondary Cluster: Faulty Resource Use | SFP Secondary Cluster: Faulty Resource Use | CWE-983-sfp-secondary-cluster-faulty-resource-use |
| CWE-984 | category |  | SFP Secondary Cluster: Life Cycle | SFP Secondary Cluster: Life Cycle | CWE-984-sfp-secondary-cluster-life-cycle |
| CWE-985 | category |  | SFP Secondary Cluster: Unrestricted Consumption | SFP Secondary Cluster: Unrestricted Consumption | CWE-985-sfp-secondary-cluster-unrestricted-consumption |
| CWE-986 | category |  | SFP Secondary Cluster: Missing Lock | SFP Secondary Cluster: Missing Lock | CWE-986-sfp-secondary-cluster-missing-lock |
| CWE-987 | category |  | SFP Secondary Cluster: Multiple Locks/Unlocks | SFP Secondary Cluster: Multiple Locks/Unlocks | CWE-987-sfp-secondary-cluster-multiple-locks-unlocks |
| CWE-988 | category |  | SFP Secondary Cluster: Race Condition Window | SFP Secondary Cluster: Race Condition Window | CWE-988-sfp-secondary-cluster-race-condition-window |
| CWE-989 | category |  | SFP Secondary Cluster: Unrestricted Lock | SFP Secondary Cluster: Unrestricted Lock | CWE-989-sfp-secondary-cluster-unrestricted-lock |
| CWE-990 | category |  | SFP Secondary Cluster: Tainted Input to Command | SFP Secondary Cluster: Tainted Input to Command | CWE-990-sfp-secondary-cluster-tainted-input-to-command |
| CWE-991 | category |  | SFP Secondary Cluster: Tainted Input to Environment | SFP Secondary Cluster: Tainted Input to Environment | CWE-991-sfp-secondary-cluster-tainted-input-to-environment |
| CWE-992 | category |  | SFP Secondary Cluster: Faulty Input Transformation | SFP Secondary Cluster: Faulty Input Transformation | CWE-992-sfp-secondary-cluster-faulty-input-transformation |
| CWE-993 | category |  | SFP Secondary Cluster: Incorrect Input Handling | SFP Secondary Cluster: Incorrect Input Handling | CWE-993-sfp-secondary-cluster-incorrect-input-handling |
| CWE-994 | category |  | SFP Secondary Cluster: Tainted Input to Variable | SFP Secondary Cluster: Tainted Input to Variable | CWE-994-sfp-secondary-cluster-tainted-input-to-variable |
| CWE-995 | category |  | SFP Secondary Cluster: Feature | SFP Secondary Cluster: Feature | CWE-995-sfp-secondary-cluster-feature |
| CWE-996 | category |  | SFP Secondary Cluster: Security | SFP Secondary Cluster: Security | CWE-996-sfp-secondary-cluster-security |
| CWE-997 | category |  | SFP Secondary Cluster: Information Loss | SFP Secondary Cluster: Information Loss | CWE-997-sfp-secondary-cluster-information-loss |
| CWE-998 | category |  | SFP Secondary Cluster: Glitch in Computation | SFP Secondary Cluster: Glitch in Computation | CWE-998-sfp-secondary-cluster-glitch-in-computation |
| CWE-1001 | category |  | SFP Secondary Cluster: Use of an Improper API | SFP Secondary Cluster: Use of an Improper API | CWE-1001-sfp-secondary-cluster-use-of-an-improper-api |
| CWE-1002 | category |  | SFP Secondary Cluster: Unexpected Entry Points | SFP Secondary Cluster: Unexpected Entry Points | CWE-1002-sfp-secondary-cluster-unexpected-entry-points |
| CWE-1004 | weakness | Variant | Sensitive Cookie Without 'HttpOnly' Flag | Sensitive Cookie Without 'HttpOnly' Flag | CWE-1004-sensitive-cookie-without-httponly-flag |
| CWE-1005 | category |  | 7PK - Input Validation and Representation | 7PK - Input Validation and Representation | CWE-1005-7pk-input-validation-and-representation |
| CWE-1006 | category |  | Bad Coding Practices | Bad Coding Practices | CWE-1006-bad-coding-practices |
| CWE-1007 | weakness | Base | Insufficient Visual Distinction of Homoglyphs Presented to User | Insufficient Visual Distinction of Homoglyphs Presented to User | CWE-1007-insufficient-visual-distinction-of-homoglyphs-presented-to |
| CWE-1009 | category |  | Audit | Audit | CWE-1009-audit |
| CWE-1010 | category |  | Authenticate Actors | Authenticate Actors | CWE-1010-authenticate-actors |
| CWE-1011 | category |  | Authorize Actors | Authorize Actors | CWE-1011-authorize-actors |
| CWE-1012 | category |  | Cross Cutting | Cross Cutting | CWE-1012-cross-cutting |
| CWE-1013 | category |  | Encrypt Data | Encrypt Data | CWE-1013-encrypt-data |
| CWE-1014 | category |  | Identify Actors | Identify Actors | CWE-1014-identify-actors |
| CWE-1015 | category |  | Limit Access | Limit Access | CWE-1015-limit-access |
| CWE-1016 | category |  | Limit Exposure | Limit Exposure | CWE-1016-limit-exposure |
| CWE-1017 | category |  | Lock Computer | Lock Computer | CWE-1017-lock-computer |
| CWE-1018 | category |  | Manage User Sessions | Manage User Sessions | CWE-1018-manage-user-sessions |
| CWE-1019 | category |  | Validate Inputs | Validate Inputs | CWE-1019-validate-inputs |
| CWE-1020 | category |  | Verify Message Integrity | Verify Message Integrity | CWE-1020-verify-message-integrity |
| CWE-1021 | weakness | Base | Improper Restriction of Rendered UI Layers or Frames | Improper Restriction of Rendered UI Layers or Frames | CWE-1021-improper-restriction-of-rendered-ui-layers-or-frames |
| CWE-1022 | weakness | Variant | Use of Web Link to Untrusted Target with window.opener Access | Use of Web Link to Untrusted Target with window.opener Access | CWE-1022-web-link-untrusted-target-with-window-opener-access |
| CWE-1023 | weakness | Class | Incomplete Comparison with Missing Factors | Incomplete Comparison with Missing Factors | CWE-1023-incomplete-comparison-with-missing-factors |
| CWE-1024 | weakness | Base | Comparison of Incompatible Types | Comparison of Incompatible Types | CWE-1024-comparison-of-incompatible-types |
| CWE-1025 | weakness | Base | Comparison Using Wrong Factors | Comparison Using Wrong Factors | CWE-1025-comparison-using-wrong-factors |
| CWE-1027 | category |  | OWASP Top Ten 2017 Category A1 - Injection | OWASP Top Ten 2017 Category A1 - Injection | CWE-1027-owasp-top-ten-2017-category-a1-injection |
| CWE-1028 | category |  | OWASP Top Ten 2017 Category A2 - Broken Authentication | OWASP Top Ten 2017 Category A2 - Broken Authentication | CWE-1028-owasp-top-ten-2017-category-a2-broken-authentication |
| CWE-1029 | category |  | OWASP Top Ten 2017 Category A3 - Sensitive Data Exposure | OWASP Top Ten 2017 Category A3 - Sensitive Data Exposure | CWE-1029-owasp-top-ten-2017-category-a3-sensitive-data |
| CWE-1030 | category |  | OWASP Top Ten 2017 Category A4 - XML External Entities | OWASP Top Ten 2017 Category A4 - XML External Entities (XXE) | CWE-1030-owasp-top-ten-2017-category-a4-xml-external |
| CWE-1031 | category |  | OWASP Top Ten 2017 Category A5 - Broken Access Control | OWASP Top Ten 2017 Category A5 - Broken Access Control | CWE-1031-owasp-top-ten-2017-category-a5-broken-access |
| CWE-1032 | category |  | OWASP Top Ten 2017 Category A6 - Security Misconfiguration | OWASP Top Ten 2017 Category A6 - Security Misconfiguration | CWE-1032-owasp-top-ten-2017-category-a6-security-misconfiguration |
| CWE-1033 | category |  | OWASP Top Ten 2017 Category A7 - Cross-Site Scripting | OWASP Top Ten 2017 Category A7 - Cross-Site Scripting (XSS) | CWE-1033-owasp-top-ten-2017-category-a7-cross-site |
| CWE-1034 | category |  | OWASP Top Ten 2017 Category A8 - Insecure Deserialization | OWASP Top Ten 2017 Category A8 - Insecure Deserialization | CWE-1034-owasp-top-ten-2017-category-a8-insecure-deserialization |
| CWE-1035 | category |  | OWASP Top Ten 2017 Category A9 - Using Components with Known Vulnerabilities | OWASP Top Ten 2017 Category A9 - Using Components with Known Vulnerabilities | CWE-1035-owasp-top-ten-2017-category-a9-components-with |
| CWE-1036 | category |  | OWASP Top Ten 2017 Category A10 - Insufficient Logging & Monitoring | OWASP Top Ten 2017 Category A10 - Insufficient Logging & Monitoring | CWE-1036-owasp-top-ten-2017-category-a10-insufficient-logging |
| CWE-1037 | weakness | Base | Processor Optimization Removal or Modification of Security-critical Code | Processor Optimization Removal or Modification of Security-critical Code | CWE-1037-processor-optimization-removal-modification-security |
| CWE-1038 | weakness | Class | Insecure Automated Optimizations | Insecure Automated Optimizations | CWE-1038-insecure-automated-optimizations |
| CWE-1039 | weakness | Class | Inadequate Detection or Handling of Adversarial Input Perturbations in Automated Recognition Mechanism | Inadequate Detection or Handling of Adversarial Input Perturbations in Automated Recognition Mechanism | CWE-1039-inadequate-detection-handling-adversarial-input |
| CWE-1041 | weakness | Base | Use of Redundant Code | Use of Redundant Code | CWE-1041-use-of-redundant-code |
| CWE-1042 | weakness | Variant | Static Member Data Element outside of a Singleton Class Element | Static Member Data Element outside of a Singleton Class Element | CWE-1042-static-member-data-element-outside-singleton-class-element |
| CWE-1043 | weakness | Base | Data Element Aggregating an Excessively Large Number of Non-Primitive Elements | Data Element Aggregating an Excessively Large Number of Non-Primitive Elements | CWE-1043-data-element-aggregating-excessively-large-number-non |
| CWE-1044 | weakness | Base | Architecture with Number of Horizontal Layers Outside of Expected Range | Architecture with Number of Horizontal Layers Outside of Expected Range | CWE-1044-architecture-with-number-horizontal-layers-outside-expected |
| CWE-1045 | weakness | Base | Parent Class with a Virtual Destructor and a Child Class without a Virtual Destructor | Parent Class with a Virtual Destructor and a Child Class without a Virtual Destructor | CWE-1045-parent-class-with-virtual-destructor-child-class-without |
| CWE-1046 | weakness | Base | Creation of Immutable Text Using String Concatenation | Creation of Immutable Text Using String Concatenation | CWE-1046-creation-of-immutable-text-using-string-concatenation |
| CWE-1047 | weakness | Base | Modules with Circular Dependencies | Modules with Circular Dependencies | CWE-1047-modules-with-circular-dependencies |
| CWE-1048 | weakness | Base | Invokable Control Element with Large Number of Outward Calls | Invokable Control Element with Large Number of Outward Calls | CWE-1048-invokable-control-element-with-large-number-outward-calls |
| CWE-1049 | weakness | Base | Excessive Data Query Operations in a Large Data Table | Excessive Data Query Operations in a Large Data Table | CWE-1049-excessive-data-query-operations-large-data-table |
| CWE-1050 | weakness | Base | Excessive Platform Resource Consumption within a Loop | Excessive Platform Resource Consumption within a Loop | CWE-1050-excessive-platform-resource-consumption-within-a-loop |
| CWE-1051 | weakness | Base | Initialization with Hard-Coded Network Resource Configuration Data | Initialization with Hard-Coded Network Resource Configuration Data | CWE-1051-initialization-with-hard-coded-network-resource |
| CWE-1052 | weakness | Base | Excessive Use of Hard-Coded Literals in Initialization | Excessive Use of Hard-Coded Literals in Initialization | CWE-1052-excessive-use-of-hard-coded-literals-in-initialization |
| CWE-1053 | weakness | Base | Missing Documentation for Design | Missing Documentation for Design | CWE-1053-missing-documentation-for-design |
| CWE-1054 | weakness | Base | Invocation of a Control Element at an Unnecessarily Deep Horizontal Layer | Invocation of a Control Element at an Unnecessarily Deep Horizontal Layer | CWE-1054-invocation-control-element-at-unnecessarily-deep-horizontal |
| CWE-1055 | weakness | Base | Multiple Inheritance from Concrete Classes | Multiple Inheritance from Concrete Classes | CWE-1055-multiple-inheritance-from-concrete-classes |
| CWE-1056 | weakness | Base | Invokable Control Element with Variadic Parameters | Invokable Control Element with Variadic Parameters | CWE-1056-invokable-control-element-with-variadic-parameters |
| CWE-1057 | weakness | Base | Data Access Operations Outside of Expected Data Manager Component | Data Access Operations Outside of Expected Data Manager Component | CWE-1057-data-access-operations-outside-expected-data-manager |
| CWE-1058 | weakness | Base | Invokable Control Element in Multi-Thread Context with non-Final Static Storable or Member Element | Invokable Control Element in Multi-Thread Context with non-Final Static Storable or Member Element | CWE-1058-invokable-control-element-multi-thread-context-with-non |
| CWE-1059 | weakness | Class | Insufficient Technical Documentation | Insufficient Technical Documentation | CWE-1059-insufficient-technical-documentation |
| CWE-1060 | weakness | Base | Excessive Number of Inefficient Server-Side Data Accesses | Excessive Number of Inefficient Server-Side Data Accesses | CWE-1060-excessive-number-of-inefficient-server-side-data-accesses |
| CWE-1061 | weakness | Class | Insufficient Encapsulation | Insufficient Encapsulation | CWE-1061-insufficient-encapsulation |
| CWE-1062 | weakness | Base | Parent Class with References to Child Class | Parent Class with References to Child Class | CWE-1062-parent-class-with-references-to-child-class |
| CWE-1063 | weakness | Base | Creation of Class Instance within a Static Code Block | Creation of Class Instance within a Static Code Block | CWE-1063-creation-class-instance-within-static-code-block |
| CWE-1064 | weakness | Base | Invokable Control Element with Signature Containing an Excessive Number of Parameters | Invokable Control Element with Signature Containing an Excessive Number of Parameters | CWE-1064-invokable-control-element-with-signature-containing |
| CWE-1065 | weakness | Base | Runtime Resource Management Control Element in a Component Built to Run on Application Servers | Runtime Resource Management Control Element in a Component Built to Run on Application Servers | CWE-1065-runtime-resource-management-control-element-component-built |
| CWE-1066 | weakness | Base | Missing Serialization Control Element | Missing Serialization Control Element | CWE-1066-missing-serialization-control-element |
| CWE-1067 | weakness | Base | Excessive Execution of Sequential Searches of Data Resource | Excessive Execution of Sequential Searches of Data Resource | CWE-1067-excessive-execution-of-sequential-searches-of-data-resource |
| CWE-1068 | weakness | Base | Inconsistency Between Implementation and Documented Design | Inconsistency Between Implementation and Documented Design | CWE-1068-inconsistency-between-implementation-and-documented-design |
| CWE-1069 | weakness | Variant | Empty Exception Block | Empty Exception Block | CWE-1069-empty-exception-block |
| CWE-1070 | weakness | Base | Serializable Data Element Containing non-Serializable Item Elements | Serializable Data Element Containing non-Serializable Item Elements | CWE-1070-serializable-data-element-containing-non-serializable-item |
| CWE-1071 | weakness | Base | Empty Code Block | Empty Code Block | CWE-1071-empty-code-block |
| CWE-1072 | weakness | Base | Data Resource Access without Use of Connection Pooling | Data Resource Access without Use of Connection Pooling | CWE-1072-data-resource-access-without-use-of-connection-pooling |
| CWE-1073 | weakness | Base | Non-SQL Invokable Control Element with Excessive Number of Data Resource Accesses | Non-SQL Invokable Control Element with Excessive Number of Data Resource Accesses | CWE-1073-non-sql-invokable-control-element-with-excessive-number |
| CWE-1074 | weakness | Base | Class with Excessively Deep Inheritance | Class with Excessively Deep Inheritance | CWE-1074-class-with-excessively-deep-inheritance |
| CWE-1075 | weakness | Base | Unconditional Control Flow Transfer outside of Switch Block | Unconditional Control Flow Transfer outside of Switch Block | CWE-1075-unconditional-control-flow-transfer-outside-of-switch-block |
| CWE-1076 | weakness | Class | Insufficient Adherence to Expected Conventions | Insufficient Adherence to Expected Conventions | CWE-1076-insufficient-adherence-to-expected-conventions |
| CWE-1077 | weakness | Variant | Floating Point Comparison with Incorrect Operator | Floating Point Comparison with Incorrect Operator | CWE-1077-floating-point-comparison-with-incorrect-operator |
| CWE-1078 | weakness | Class | Inappropriate Source Code Style or Formatting | Inappropriate Source Code Style or Formatting | CWE-1078-inappropriate-source-code-style-or-formatting |
| CWE-1079 | weakness | Base | Parent Class without Virtual Destructor Method | Parent Class without Virtual Destructor Method | CWE-1079-parent-class-without-virtual-destructor-method |
| CWE-1080 | weakness | Base | Source Code File with Excessive Number of Lines of Code | Source Code File with Excessive Number of Lines of Code | CWE-1080-source-code-file-with-excessive-number-lines-code |
| CWE-1082 | weakness | Base | Class Instance Self Destruction Control Element | Class Instance Self Destruction Control Element | CWE-1082-class-instance-self-destruction-control-element |
| CWE-1083 | weakness | Base | Data Access from Outside Expected Data Manager Component | Data Access from Outside Expected Data Manager Component | CWE-1083-data-access-from-outside-expected-data-manager-component |
| CWE-1084 | weakness | Base | Invokable Control Element with Excessive File or Data Access Operations | Invokable Control Element with Excessive File or Data Access Operations | CWE-1084-invokable-control-element-with-excessive-file-data-access |
| CWE-1085 | weakness | Base | Invokable Control Element with Excessive Volume of Commented-out Code | Invokable Control Element with Excessive Volume of Commented-out Code | CWE-1085-invokable-control-element-with-excessive-volume-commented |
| CWE-1086 | weakness | Base | Class with Excessive Number of Child Classes | Class with Excessive Number of Child Classes | CWE-1086-class-with-excessive-number-of-child-classes |
| CWE-1087 | weakness | Base | Class with Virtual Method without a Virtual Destructor | Class with Virtual Method without a Virtual Destructor | CWE-1087-class-with-virtual-method-without-a-virtual-destructor |
| CWE-1088 | weakness | Base | Synchronous Access of Remote Resource without Timeout | Synchronous Access of Remote Resource without Timeout | CWE-1088-synchronous-access-of-remote-resource-without-timeout |
| CWE-1089 | weakness | Base | Large Data Table with Excessive Number of Indices | Large Data Table with Excessive Number of Indices | CWE-1089-large-data-table-with-excessive-number-of-indices |
| CWE-1090 | weakness | Base | Method Containing Access of a Member Element from Another Class | Method Containing Access of a Member Element from Another Class | CWE-1090-method-containing-access-member-element-from-another-class |
| CWE-1091 | weakness | Base | Use of Object without Invoking Destructor Method | Use of Object without Invoking Destructor Method | CWE-1091-use-of-object-without-invoking-destructor-method |
| CWE-1092 | weakness | Base | Use of Same Invokable Control Element in Multiple Architectural Layers | Use of Same Invokable Control Element in Multiple Architectural Layers | CWE-1092-same-invokable-control-element-multiple-architectural-layers |
| CWE-1093 | weakness | Class | Excessively Complex Data Representation | Excessively Complex Data Representation | CWE-1093-excessively-complex-data-representation |
| CWE-1094 | weakness | Base | Excessive Index Range Scan for a Data Resource | Excessive Index Range Scan for a Data Resource | CWE-1094-excessive-index-range-scan-for-a-data-resource |
| CWE-1095 | weakness | Base | Loop Condition Value Update within the Loop | Loop Condition Value Update within the Loop | CWE-1095-loop-condition-value-update-within-the-loop |
| CWE-1096 | weakness | Variant | Singleton Class Instance Creation without Proper Locking or Synchronization | Singleton Class Instance Creation without Proper Locking or Synchronization | CWE-1096-singleton-class-instance-creation-without-proper-locking |
| CWE-1097 | weakness | Base | Persistent Storable Data Element without Associated Comparison Control Element | Persistent Storable Data Element without Associated Comparison Control Element | CWE-1097-persistent-storable-data-element-without-associated |
| CWE-1098 | weakness | Base | Data Element containing Pointer Item without Proper Copy Control Element | Data Element containing Pointer Item without Proper Copy Control Element | CWE-1098-data-element-containing-pointer-item-without-proper-copy |
| CWE-1099 | weakness | Base | Inconsistent Naming Conventions for Identifiers | Inconsistent Naming Conventions for Identifiers | CWE-1099-inconsistent-naming-conventions-for-identifiers |
| CWE-1100 | weakness | Base | Insufficient Isolation of System-Dependent Functions | Insufficient Isolation of System-Dependent Functions | CWE-1100-insufficient-isolation-of-system-dependent-functions |
| CWE-1101 | weakness | Base | Reliance on Runtime Component in Generated Code | Reliance on Runtime Component in Generated Code | CWE-1101-reliance-on-runtime-component-in-generated-code |
| CWE-1102 | weakness | Base | Reliance on Machine-Dependent Data Representation | Reliance on Machine-Dependent Data Representation | CWE-1102-reliance-on-machine-dependent-data-representation |
| CWE-1103 | weakness | Base | Use of Platform-Dependent Third Party Components | Use of Platform-Dependent Third Party Components | CWE-1103-use-of-platform-dependent-third-party-components |
| CWE-1104 | weakness | Base | Use of Unmaintained Third Party Components | Use of Unmaintained Third Party Components | CWE-1104-use-of-unmaintained-third-party-components |
| CWE-1105 | weakness | Base | Insufficient Encapsulation of Machine-Dependent Functionality | Insufficient Encapsulation of Machine-Dependent Functionality | CWE-1105-insufficient-encapsulation-of-machine-dependent |
| CWE-1106 | weakness | Base | Insufficient Use of Symbolic Constants | Insufficient Use of Symbolic Constants | CWE-1106-insufficient-use-of-symbolic-constants |
| CWE-1107 | weakness | Base | Insufficient Isolation of Symbolic Constant Definitions | Insufficient Isolation of Symbolic Constant Definitions | CWE-1107-insufficient-isolation-of-symbolic-constant-definitions |
| CWE-1108 | weakness | Base | Excessive Reliance on Global Variables | Excessive Reliance on Global Variables | CWE-1108-excessive-reliance-on-global-variables |
| CWE-1109 | weakness | Base | Use of Same Variable for Multiple Purposes | Use of Same Variable for Multiple Purposes | CWE-1109-use-of-same-variable-for-multiple-purposes |
| CWE-1110 | weakness | Base | Incomplete Design Documentation | Incomplete Design Documentation | CWE-1110-incomplete-design-documentation |
| CWE-1111 | weakness | Base | Incomplete I/O Documentation | Incomplete I/O Documentation | CWE-1111-incomplete-i-o-documentation |
| CWE-1112 | weakness | Base | Incomplete Documentation of Program Execution | Incomplete Documentation of Program Execution | CWE-1112-incomplete-documentation-of-program-execution |
| CWE-1113 | weakness | Base | Inappropriate Comment Style | Inappropriate Comment Style | CWE-1113-inappropriate-comment-style |
| CWE-1114 | weakness | Base | Inappropriate Whitespace Style | Inappropriate Whitespace Style | CWE-1114-inappropriate-whitespace-style |
| CWE-1115 | weakness | Base | Source Code Element without Standard Prologue | Source Code Element without Standard Prologue | CWE-1115-source-code-element-without-standard-prologue |
| CWE-1116 | weakness | Base | Inaccurate Source Code Comments | Inaccurate Source Code Comments | CWE-1116-inaccurate-source-code-comments |
| CWE-1117 | weakness | Base | Callable with Insufficient Behavioral Summary | Callable with Insufficient Behavioral Summary | CWE-1117-callable-with-insufficient-behavioral-summary |
| CWE-1118 | weakness | Base | Insufficient Documentation of Error Handling Techniques | Insufficient Documentation of Error Handling Techniques | CWE-1118-insufficient-documentation-of-error-handling-techniques |
| CWE-1119 | weakness | Base | Excessive Use of Unconditional Branching | Excessive Use of Unconditional Branching | CWE-1119-excessive-use-of-unconditional-branching |
| CWE-1120 | weakness | Class | Excessive Code Complexity | Excessive Code Complexity | CWE-1120-excessive-code-complexity |
| CWE-1121 | weakness | Base | Excessive McCabe Cyclomatic Complexity | Excessive McCabe Cyclomatic Complexity | CWE-1121-excessive-mccabe-cyclomatic-complexity |
| CWE-1122 | weakness | Base | Excessive Halstead Complexity | Excessive Halstead Complexity | CWE-1122-excessive-halstead-complexity |
| CWE-1123 | weakness | Base | Excessive Use of Self-Modifying Code | Excessive Use of Self-Modifying Code | CWE-1123-excessive-use-of-self-modifying-code |
| CWE-1124 | weakness | Base | Excessively Deep Nesting | Excessively Deep Nesting | CWE-1124-excessively-deep-nesting |
| CWE-1125 | weakness | Base | Excessive Attack Surface | Excessive Attack Surface | CWE-1125-excessive-attack-surface |
| CWE-1126 | weakness | Base | Declaration of Variable with Unnecessarily Wide Scope | Declaration of Variable with Unnecessarily Wide Scope | CWE-1126-declaration-of-variable-with-unnecessarily-wide-scope |
| CWE-1127 | weakness | Base | Compilation with Insufficient Warnings or Errors | Compilation with Insufficient Warnings or Errors | CWE-1127-compilation-with-insufficient-warnings-or-errors |
| CWE-1129 | category |  | CISQ Quality Measures - Reliability | CISQ Quality Measures (2016) - Reliability | CWE-1129-cisq-quality-measures-reliability |
| CWE-1130 | category |  | CISQ Quality Measures - Maintainability | CISQ Quality Measures (2016) - Maintainability | CWE-1130-cisq-quality-measures-maintainability |
| CWE-1131 | category |  | CISQ Quality Measures - Security | CISQ Quality Measures (2016) - Security | CWE-1131-cisq-quality-measures-security |
| CWE-1132 | category |  | CISQ Quality Measures - Performance Efficiency | CISQ Quality Measures (2016) - Performance Efficiency | CWE-1132-cisq-quality-measures-performance-efficiency |
| CWE-1134 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 00. Input Validation and Data Sanitization | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 00. Input Validation and Data Sanitization (IDS) | CWE-1134-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1135 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 01. Declarations and Initialization | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 01. Declarations and Initialization (DCL) | CWE-1135-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1136 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 02. Expressions | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 02. Expressions (EXP) | CWE-1136-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1137 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 03. Numeric Types and Operations | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 03. Numeric Types and Operations (NUM) | CWE-1137-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1138 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 04. Characters and Strings | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 04. Characters and Strings (STR) | CWE-1138-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1139 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 05. Object Orientation | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 05. Object Orientation (OBJ) | CWE-1139-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1140 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 06. Methods | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 06. Methods (MET) | CWE-1140-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1141 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 07. Exceptional Behavior | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 07. Exceptional Behavior (ERR) | CWE-1141-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1142 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 08. Visibility and Atomicity | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 08. Visibility and Atomicity (VNA) | CWE-1142-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1143 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 09. Locking | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 09. Locking (LCK) | CWE-1143-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1144 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 10. Thread APIs | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 10. Thread APIs (THI) | CWE-1144-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1145 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 11. Thread Pools | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 11. Thread Pools (TPS) | CWE-1145-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1146 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 12. Thread-Safety Miscellaneous | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 12. Thread-Safety Miscellaneous (TSM) | CWE-1146-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1147 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 13. Input Output | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 13. Input Output (FIO) | CWE-1147-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1148 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 14. Serialization | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 14. Serialization (SER) | CWE-1148-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1149 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 15. Platform Security | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 15. Platform Security (SEC) | CWE-1149-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1150 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 16. Runtime Environment | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 16. Runtime Environment (ENV) | CWE-1150-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1151 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 17. Java Native Interface | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 17. Java Native Interface (JNI) | CWE-1151-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1152 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 49. Miscellaneous | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 49. Miscellaneous (MSC) | CWE-1152-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1153 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 50. Android | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 50. Android (DRD) | CWE-1153-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1155 | category |  | SEI CERT C Coding Standard - Guidelines 01. Preprocessor | SEI CERT C Coding Standard - Guidelines 01. Preprocessor (PRE) | CWE-1155-sei-cert-c-coding-standard-guidelines-01-preprocessor |
| CWE-1156 | category |  | SEI CERT C Coding Standard - Guidelines 02. Declarations and Initialization | SEI CERT C Coding Standard - Guidelines 02. Declarations and Initialization (DCL) | CWE-1156-sei-cert-c-coding-standard-guidelines-02-declarations |
| CWE-1157 | category |  | SEI CERT C Coding Standard - Guidelines 03. Expressions | SEI CERT C Coding Standard - Guidelines 03. Expressions (EXP) | CWE-1157-sei-cert-c-coding-standard-guidelines-03-expressions |
| CWE-1158 | category |  | SEI CERT C Coding Standard - Guidelines 04. Integers | SEI CERT C Coding Standard - Guidelines 04. Integers (INT) | CWE-1158-sei-cert-c-coding-standard-guidelines-04-integers |
| CWE-1159 | category |  | SEI CERT C Coding Standard - Guidelines 05. Floating Point | SEI CERT C Coding Standard - Guidelines 05. Floating Point (FLP) | CWE-1159-sei-cert-c-coding-standard-guidelines-05-floating |
| CWE-1160 | category |  | SEI CERT C Coding Standard - Guidelines 06. Arrays | SEI CERT C Coding Standard - Guidelines 06. Arrays (ARR) | CWE-1160-sei-cert-c-coding-standard-guidelines-06-arrays |
| CWE-1161 | category |  | SEI CERT C Coding Standard - Guidelines 07. Characters and Strings | SEI CERT C Coding Standard - Guidelines 07. Characters and Strings (STR) | CWE-1161-sei-cert-c-coding-standard-guidelines-07-characters |
| CWE-1162 | category |  | SEI CERT C Coding Standard - Guidelines 08. Memory Management | SEI CERT C Coding Standard - Guidelines 08. Memory Management (MEM) | CWE-1162-sei-cert-c-coding-standard-guidelines-08-memory |
| CWE-1163 | category |  | SEI CERT C Coding Standard - Guidelines 09. Input Output | SEI CERT C Coding Standard - Guidelines 09. Input Output (FIO) | CWE-1163-sei-cert-c-coding-standard-guidelines-09-input |
| CWE-1164 | weakness | Class | Irrelevant Code | Irrelevant Code | CWE-1164-irrelevant-code |
| CWE-1165 | category |  | SEI CERT C Coding Standard - Guidelines 10. Environment | SEI CERT C Coding Standard - Guidelines 10. Environment (ENV) | CWE-1165-sei-cert-c-coding-standard-guidelines-10-environment |
| CWE-1166 | category |  | SEI CERT C Coding Standard - Guidelines 11. Signals | SEI CERT C Coding Standard - Guidelines 11. Signals (SIG) | CWE-1166-sei-cert-c-coding-standard-guidelines-11-signals |
| CWE-1167 | category |  | SEI CERT C Coding Standard - Guidelines 12. Error Handling | SEI CERT C Coding Standard - Guidelines 12. Error Handling (ERR) | CWE-1167-sei-cert-c-coding-standard-guidelines-12-error |
| CWE-1168 | category |  | SEI CERT C Coding Standard - Guidelines 13. Application Programming Interfaces | SEI CERT C Coding Standard - Guidelines 13. Application Programming Interfaces (API) | CWE-1168-sei-cert-c-coding-standard-guidelines-13-application |
| CWE-1169 | category |  | SEI CERT C Coding Standard - Guidelines 14. Concurrency | SEI CERT C Coding Standard - Guidelines 14. Concurrency (CON) | CWE-1169-sei-cert-c-coding-standard-guidelines-14-concurrency |
| CWE-1170 | category |  | SEI CERT C Coding Standard - Guidelines 48. Miscellaneous | SEI CERT C Coding Standard - Guidelines 48. Miscellaneous (MSC) | CWE-1170-sei-cert-c-coding-standard-guidelines-48-miscellaneous |
| CWE-1171 | category |  | SEI CERT C Coding Standard - Guidelines 50. POSIX | SEI CERT C Coding Standard - Guidelines 50. POSIX (POS) | CWE-1171-sei-cert-c-coding-standard-guidelines-50-posix |
| CWE-1172 | category |  | SEI CERT C Coding Standard - Guidelines 51. Microsoft Windows | SEI CERT C Coding Standard - Guidelines 51. Microsoft Windows (WIN) | CWE-1172-sei-cert-c-coding-standard-guidelines-51-microsoft |
| CWE-1173 | weakness | Base | Improper Use of Validation Framework | Improper Use of Validation Framework | CWE-1173-improper-use-of-validation-framework |
| CWE-1174 | weakness | Variant | ASP.NET Misconfiguration: Improper Model Validation | ASP.NET Misconfiguration: Improper Model Validation | CWE-1174-asp-net-misconfiguration-improper-model-validation |
| CWE-1175 | category |  | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 18. Concurrency | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 18. Concurrency (CON) | CWE-1175-sei-cert-oracle-secure-coding-standard-for-java |
| CWE-1176 | weakness | Class | Inefficient CPU Computation | Inefficient CPU Computation | CWE-1176-inefficient-cpu-computation |
| CWE-1177 | weakness | Class | Use of Prohibited Code | Use of Prohibited Code | CWE-1177-use-of-prohibited-code |
| CWE-1179 | category |  | SEI CERT Perl Coding Standard - Guidelines 01. Input Validation and Data Sanitization | SEI CERT Perl Coding Standard - Guidelines 01. Input Validation and Data Sanitization (IDS) | CWE-1179-sei-cert-perl-coding-standard-guidelines-01-input |
| CWE-1180 | category |  | SEI CERT Perl Coding Standard - Guidelines 02. Declarations and Initialization | SEI CERT Perl Coding Standard - Guidelines 02. Declarations and Initialization (DCL) | CWE-1180-sei-cert-perl-coding-standard-guidelines-02-declarations |
| CWE-1181 | category |  | SEI CERT Perl Coding Standard - Guidelines 03. Expressions | SEI CERT Perl Coding Standard - Guidelines 03. Expressions (EXP) | CWE-1181-sei-cert-perl-coding-standard-guidelines-03-expressions |
| CWE-1182 | category |  | SEI CERT Perl Coding Standard - Guidelines 04. Integers | SEI CERT Perl Coding Standard - Guidelines 04. Integers (INT) | CWE-1182-sei-cert-perl-coding-standard-guidelines-04-integers |
| CWE-1183 | category |  | SEI CERT Perl Coding Standard - Guidelines 05. Strings | SEI CERT Perl Coding Standard - Guidelines 05. Strings (STR) | CWE-1183-sei-cert-perl-coding-standard-guidelines-05-strings |
| CWE-1184 | category |  | SEI CERT Perl Coding Standard - Guidelines 06. Object-Oriented Programming | SEI CERT Perl Coding Standard - Guidelines 06. Object-Oriented Programming (OOP) | CWE-1184-sei-cert-perl-coding-standard-guidelines-06-object |
| CWE-1185 | category |  | SEI CERT Perl Coding Standard - Guidelines 07. File Input and Output | SEI CERT Perl Coding Standard - Guidelines 07. File Input and Output (FIO) | CWE-1185-sei-cert-perl-coding-standard-guidelines-07-file |
| CWE-1186 | category |  | SEI CERT Perl Coding Standard - Guidelines 50. Miscellaneous | SEI CERT Perl Coding Standard - Guidelines 50. Miscellaneous (MSC) | CWE-1186-sei-cert-perl-coding-standard-guidelines-50-miscellaneous |
| CWE-1187 | weakness | Base | DEPRECATED: Use of Uninitialized Resource | DEPRECATED: Use of Uninitialized Resource | CWE-1187-deprecated-use-of-uninitialized-resource |
| CWE-1188 | weakness | Base | Initialization of a Resource with an Insecure Default | Initialization of a Resource with an Insecure Default | CWE-1188-initialization-of-a-resource-with-an-insecure-default |
| CWE-1189 | weakness | Base | Improper Isolation of Shared Resources on System-on-a-Chip | Improper Isolation of Shared Resources on System-on-a-Chip (SoC) | CWE-1189-improper-isolation-shared-resources-on-system-on-chip |
| CWE-1190 | weakness | Base | DMA Device Enabled Too Early in Boot Phase | DMA Device Enabled Too Early in Boot Phase | CWE-1190-dma-device-enabled-too-early-in-boot-phase |
| CWE-1191 | weakness | Base | On-Chip Debug and Test Interface With Improper Access Control | On-Chip Debug and Test Interface With Improper Access Control | CWE-1191-on-chip-debug-test-interface-with-improper-access |
| CWE-1192 | weakness | Base | Improper Identifier for IP Block used in System-On-Chip | Improper Identifier for IP Block used in System-On-Chip (SOC) | CWE-1192-improper-identifier-for-ip-block-system-on-chip |
| CWE-1193 | weakness | Base | Power-On of Untrusted Execution Core Before Enabling Fabric Access Control | Power-On of Untrusted Execution Core Before Enabling Fabric Access Control | CWE-1193-power-on-untrusted-execution-core-before-enabling-fabric |
| CWE-1195 | category |  | Manufacturing and Life Cycle Management Concerns | Manufacturing and Life Cycle Management Concerns | CWE-1195-manufacturing-and-life-cycle-management-concerns |
| CWE-1196 | category |  | Security Flow Issues | Security Flow Issues | CWE-1196-security-flow-issues |
| CWE-1197 | category |  | Integration Issues | Integration Issues | CWE-1197-integration-issues |
| CWE-1198 | category |  | Privilege Separation and Access Control Issues | Privilege Separation and Access Control Issues | CWE-1198-privilege-separation-and-access-control-issues |
| CWE-1199 | category |  | General Circuit and Logic Design Concerns | General Circuit and Logic Design Concerns | CWE-1199-general-circuit-and-logic-design-concerns |
| CWE-1201 | category |  | Core and Compute Issues | Core and Compute Issues | CWE-1201-core-and-compute-issues |
| CWE-1202 | category |  | Memory and Storage Issues | Memory and Storage Issues | CWE-1202-memory-and-storage-issues |
| CWE-1203 | category |  | Peripherals, On-chip Fabric, and Interface/IO Problems | Peripherals, On-chip Fabric, and Interface/IO Problems | CWE-1203-peripherals-on-chip-fabric-and-interface-io-problems |
| CWE-1204 | weakness | Base | Generation of Weak Initialization Vector | Generation of Weak Initialization Vector (IV) | CWE-1204-generation-of-weak-initialization-vector |
| CWE-1205 | category |  | Security Primitives and Cryptography Issues | Security Primitives and Cryptography Issues | CWE-1205-security-primitives-and-cryptography-issues |
| CWE-1206 | category |  | Power, Clock, Thermal, and Reset Concerns | Power, Clock, Thermal, and Reset Concerns | CWE-1206-power-clock-thermal-and-reset-concerns |
| CWE-1207 | category |  | Debug and Test Problems | Debug and Test Problems | CWE-1207-debug-and-test-problems |
| CWE-1208 | category |  | Cross-Cutting Problems | Cross-Cutting Problems | CWE-1208-cross-cutting-problems |
| CWE-1209 | weakness | Base | Failure to Disable Reserved Bits | Failure to Disable Reserved Bits | CWE-1209-failure-to-disable-reserved-bits |
| CWE-1210 | category |  | Audit / Logging Errors | Audit / Logging Errors | CWE-1210-audit-logging-errors |
| CWE-1211 | category |  | Authentication Errors | Authentication Errors | CWE-1211-authentication-errors |
| CWE-1212 | category |  | Authorization Errors | Authorization Errors | CWE-1212-authorization-errors |
| CWE-1213 | category |  | Random Number Issues | Random Number Issues | CWE-1213-random-number-issues |
| CWE-1214 | category |  | Data Integrity Issues | Data Integrity Issues | CWE-1214-data-integrity-issues |
| CWE-1215 | category |  | Data Validation Issues | Data Validation Issues | CWE-1215-data-validation-issues |
| CWE-1216 | category |  | Lockout Mechanism Errors | Lockout Mechanism Errors | CWE-1216-lockout-mechanism-errors |
| CWE-1217 | category |  | User Session Errors | User Session Errors | CWE-1217-user-session-errors |
| CWE-1218 | category |  | Memory Buffer Errors | Memory Buffer Errors | CWE-1218-memory-buffer-errors |
| CWE-1219 | category |  | File Handling Issues | File Handling Issues | CWE-1219-file-handling-issues |
| CWE-1220 | weakness | Base | Insufficient Granularity of Access Control | Insufficient Granularity of Access Control | CWE-1220-insufficient-granularity-of-access-control |
| CWE-1221 | weakness | Base | Incorrect Register Defaults or Module Parameters | Incorrect Register Defaults or Module Parameters | CWE-1221-incorrect-register-defaults-or-module-parameters |
| CWE-1222 | weakness | Variant | Insufficient Granularity of Address Regions Protected by Register Locks | Insufficient Granularity of Address Regions Protected by Register Locks | CWE-1222-insufficient-granularity-address-regions-protected-by |
| CWE-1223 | weakness | Base | Race Condition for Write-Once Attributes | Race Condition for Write-Once Attributes | CWE-1223-race-condition-for-write-once-attributes |
| CWE-1224 | weakness | Base | Improper Restriction of Write-Once Bit Fields | Improper Restriction of Write-Once Bit Fields | CWE-1224-improper-restriction-of-write-once-bit-fields |
| CWE-1225 | category |  | Documentation Issues | Documentation Issues | CWE-1225-documentation-issues |
| CWE-1226 | category |  | Complexity Issues | Complexity Issues | CWE-1226-complexity-issues |
| CWE-1227 | category |  | Encapsulation Issues | Encapsulation Issues | CWE-1227-encapsulation-issues |
| CWE-1228 | category |  | API / Function Errors | API / Function Errors | CWE-1228-api-function-errors |
| CWE-1229 | weakness | Class | Creation of Emergent Resource | Creation of Emergent Resource | CWE-1229-creation-of-emergent-resource |
| CWE-1230 | weakness | Base | Exposure of Sensitive Information Through Metadata | Exposure of Sensitive Information Through Metadata | CWE-1230-exposure-of-sensitive-information-through-metadata |
| CWE-1231 | weakness | Base | Improper Prevention of Lock Bit Modification | Improper Prevention of Lock Bit Modification | CWE-1231-improper-prevention-of-lock-bit-modification |
| CWE-1232 | weakness | Base | Improper Lock Behavior After Power State Transition | Improper Lock Behavior After Power State Transition | CWE-1232-improper-lock-behavior-after-power-state-transition |
| CWE-1233 | weakness | Base | Security-Sensitive Hardware Controls with Missing Lock Bit Protection | Security-Sensitive Hardware Controls with Missing Lock Bit Protection | CWE-1233-security-sensitive-hardware-controls-with-missing-lock-bit |
| CWE-1234 | weakness | Base | Hardware Internal or Debug Modes Allow Override of Locks | Hardware Internal or Debug Modes Allow Override of Locks | CWE-1234-hardware-internal-debug-modes-allow-override-locks |
| CWE-1235 | weakness | Base | Incorrect Use of Autoboxing and Unboxing for Performance Critical Operations | Incorrect Use of Autoboxing and Unboxing for Performance Critical Operations | CWE-1235-incorrect-autoboxing-unboxing-for-performance-critical |
| CWE-1236 | weakness | Base | Improper Neutralization of Formula Elements in a CSV File | Improper Neutralization of Formula Elements in a CSV File | CWE-1236-improper-neutralization-formula-elements-csv-file |
| CWE-1237 | category |  | SFP Primary Cluster: Faulty Resource Release | SFP Primary Cluster: Faulty Resource Release | CWE-1237-sfp-primary-cluster-faulty-resource-release |
| CWE-1238 | category |  | SFP Primary Cluster: Failure to Release Memory | SFP Primary Cluster: Failure to Release Memory | CWE-1238-sfp-primary-cluster-failure-to-release-memory |
| CWE-1239 | weakness | Variant | Improper Zeroization of Hardware Register | Improper Zeroization of Hardware Register | CWE-1239-improper-zeroization-of-hardware-register |
| CWE-1240 | weakness | Base | Use of a Cryptographic Primitive with a Risky Implementation | Use of a Cryptographic Primitive with a Risky Implementation | CWE-1240-cryptographic-primitive-with-risky-implementation |
| CWE-1241 | weakness | Base | Use of Predictable Algorithm in Random Number Generator | Use of Predictable Algorithm in Random Number Generator | CWE-1241-use-of-predictable-algorithm-in-random-number-generator |
| CWE-1242 | weakness | Base | Inclusion of Undocumented Features or Chicken Bits | Inclusion of Undocumented Features or Chicken Bits | CWE-1242-inclusion-of-undocumented-features-or-chicken-bits |
| CWE-1243 | weakness | Base | Sensitive Non-Volatile Information Not Protected During Debug | Sensitive Non-Volatile Information Not Protected During Debug | CWE-1243-sensitive-non-volatile-information-not-protected-during |
| CWE-1244 | weakness | Base | Internal Asset Exposed to Unsafe Debug Access Level or State | Internal Asset Exposed to Unsafe Debug Access Level or State | CWE-1244-internal-asset-exposed-unsafe-debug-access-level-state |
| CWE-1245 | weakness | Base | Improper Finite State Machines in Hardware Logic | Improper Finite State Machines (FSMs) in Hardware Logic | CWE-1245-improper-finite-state-machines-in-hardware-logic |
| CWE-1246 | weakness | Base | Improper Write Handling in Limited-write Non-Volatile Memories | Improper Write Handling in Limited-write Non-Volatile Memories | CWE-1246-improper-write-handling-limited-write-non-volatile-memories |
| CWE-1247 | weakness | Base | Improper Protection Against Voltage and Clock Glitches | Improper Protection Against Voltage and Clock Glitches | CWE-1247-improper-protection-against-voltage-and-clock-glitches |
| CWE-1248 | weakness | Base | Semiconductor Defects in Hardware Logic with Security-Sensitive Implications | Semiconductor Defects in Hardware Logic with Security-Sensitive Implications | CWE-1248-semiconductor-defects-hardware-logic-with-security-sensitive |
| CWE-1249 | weakness | Base | Application-Level Admin Tool with Inconsistent View of Underlying Operating System | Application-Level Admin Tool with Inconsistent View of Underlying Operating System | CWE-1249-application-level-admin-tool-with-inconsistent-view |
| CWE-1250 | weakness | Base | Improper Preservation of Consistency Between Independent Representations of Shared State | Improper Preservation of Consistency Between Independent Representations of Shared State | CWE-1250-improper-preservation-consistency-between-independent |
| CWE-1251 | weakness | Base | Mirrored Regions with Different Values | Mirrored Regions with Different Values | CWE-1251-mirrored-regions-with-different-values |
| CWE-1252 | weakness | Base | CPU Hardware Not Configured to Support Exclusivity of Write and Execute Operations | CPU Hardware Not Configured to Support Exclusivity of Write and Execute Operations | CWE-1252-cpu-hardware-not-configured-support-exclusivity-write |
| CWE-1253 | weakness | Base | Incorrect Selection of Fuse Values | Incorrect Selection of Fuse Values | CWE-1253-incorrect-selection-of-fuse-values |
| CWE-1254 | weakness | Base | Incorrect Comparison Logic Granularity | Incorrect Comparison Logic Granularity | CWE-1254-incorrect-comparison-logic-granularity |
| CWE-1255 | weakness | Variant | Comparison Logic is Vulnerable to Power Side-Channel Attacks | Comparison Logic is Vulnerable to Power Side-Channel Attacks | CWE-1255-comparison-logic-is-vulnerable-power-side-channel-attacks |
| CWE-1256 | weakness | Base | Improper Restriction of Software Interfaces to Hardware Features | Improper Restriction of Software Interfaces to Hardware Features | CWE-1256-improper-restriction-of-software-interfaces-to-hardware |
| CWE-1257 | weakness | Base | Improper Access Control Applied to Mirrored or Aliased Memory Regions | Improper Access Control Applied to Mirrored or Aliased Memory Regions | CWE-1257-improper-access-control-applied-mirrored-aliased-memory |
| CWE-1258 | weakness | Base | Exposure of Sensitive System Information Due to Uncleared Debug Information | Exposure of Sensitive System Information Due to Uncleared Debug Information | CWE-1258-exposure-sensitive-system-information-due-uncleared-debug |
| CWE-1259 | weakness | Base | Improper Restriction of Security Token Assignment | Improper Restriction of Security Token Assignment | CWE-1259-improper-restriction-of-security-token-assignment |
| CWE-1260 | weakness | Base | Improper Handling of Overlap Between Protected Memory Ranges | Improper Handling of Overlap Between Protected Memory Ranges | CWE-1260-improper-handling-of-overlap-between-protected-memory-ranges |
| CWE-1261 | weakness | Base | Improper Handling of Single Event Upsets | Improper Handling of Single Event Upsets | CWE-1261-improper-handling-of-single-event-upsets |
| CWE-1262 | weakness | Base | Improper Access Control for Register Interface | Improper Access Control for Register Interface | CWE-1262-improper-access-control-for-register-interface |
| CWE-1263 | weakness | Class | Improper Physical Access Control | Improper Physical Access Control | CWE-1263-improper-physical-access-control |
| CWE-1264 | weakness | Base | Hardware Logic with Insecure De-Synchronization between Control and Data Channels | Hardware Logic with Insecure De-Synchronization between Control and Data Channels | CWE-1264-hardware-logic-with-insecure-de-synchronization-between |
| CWE-1265 | weakness | Base | Unintended Reentrant Invocation of Non-reentrant Code Via Nested Calls | Unintended Reentrant Invocation of Non-reentrant Code Via Nested Calls | CWE-1265-unintended-reentrant-invocation-non-reentrant-code-via |
| CWE-1266 | weakness | Base | Improper Scrubbing of Sensitive Data from Decommissioned Device | Improper Scrubbing of Sensitive Data from Decommissioned Device | CWE-1266-improper-scrubbing-of-sensitive-data-from-decommissioned |
| CWE-1267 | weakness | Base | Policy Uses Obsolete Encoding | Policy Uses Obsolete Encoding | CWE-1267-policy-uses-obsolete-encoding |
| CWE-1268 | weakness | Base | Policy Privileges are not Assigned Consistently Between Control and Data Agents | Policy Privileges are not Assigned Consistently Between Control and Data Agents | CWE-1268-policy-privileges-are-not-assigned-consistently-between |
| CWE-1269 | weakness | Base | Product Released in Non-Release Configuration | Product Released in Non-Release Configuration | CWE-1269-product-released-in-non-release-configuration |
| CWE-1270 | weakness | Base | Generation of Incorrect Security Tokens | Generation of Incorrect Security Tokens | CWE-1270-generation-of-incorrect-security-tokens |
| CWE-1271 | weakness | Base | Uninitialized Value on Reset for Registers Holding Security Settings | Uninitialized Value on Reset for Registers Holding Security Settings | CWE-1271-uninitialized-value-on-reset-for-registers-holding-security |
| CWE-1272 | weakness | Base | Sensitive Information Uncleared Before Debug/Power State Transition | Sensitive Information Uncleared Before Debug/Power State Transition | CWE-1272-sensitive-information-uncleared-before-debug-power-state |
| CWE-1273 | weakness | Base | Device Unlock Credential Sharing | Device Unlock Credential Sharing | CWE-1273-device-unlock-credential-sharing |
| CWE-1274 | weakness | Base | Improper Access Control for Volatile Memory Containing Boot Code | Improper Access Control for Volatile Memory Containing Boot Code | CWE-1274-improper-access-control-for-volatile-memory-containing-boot |
| CWE-1275 | weakness | Variant | Sensitive Cookie with Improper SameSite Attribute | Sensitive Cookie with Improper SameSite Attribute | CWE-1275-sensitive-cookie-with-improper-samesite-attribute |
| CWE-1276 | weakness | Base | Hardware Child Block Incorrectly Connected to Parent System | Hardware Child Block Incorrectly Connected to Parent System | CWE-1276-hardware-child-block-incorrectly-connected-to-parent-system |
| CWE-1277 | weakness | Base | Firmware Not Updateable | Firmware Not Updateable | CWE-1277-firmware-not-updateable |
| CWE-1278 | weakness | Base | Missing Protection Against Hardware Reverse Engineering Using Integrated Circuit Imaging Techniques | Missing Protection Against Hardware Reverse Engineering Using Integrated Circuit (IC) Imaging Techniques | CWE-1278-missing-protection-against-hardware-reverse-engineering |
| CWE-1279 | weakness | Base | Cryptographic Operations are run Before Supporting Units are Ready | Cryptographic Operations are run Before Supporting Units are Ready | CWE-1279-cryptographic-operations-are-run-before-supporting-units-are |
| CWE-1280 | weakness | Base | Access Control Check Implemented After Asset is Accessed | Access Control Check Implemented After Asset is Accessed | CWE-1280-access-control-check-implemented-after-asset-is-accessed |
| CWE-1281 | weakness | Base | Sequence of Processor Instructions Leads to Unexpected Behavior | Sequence of Processor Instructions Leads to Unexpected Behavior | CWE-1281-sequence-of-processor-instructions-leads-to-unexpected |
| CWE-1282 | weakness | Base | Assumed-Immutable Data is Stored in Writable Memory | Assumed-Immutable Data is Stored in Writable Memory | CWE-1282-assumed-immutable-data-is-stored-in-writable-memory |
| CWE-1283 | weakness | Base | Mutable Attestation or Measurement Reporting Data | Mutable Attestation or Measurement Reporting Data | CWE-1283-mutable-attestation-or-measurement-reporting-data |
| CWE-1284 | weakness | Base | Improper Validation of Specified Quantity in Input | Improper Validation of Specified Quantity in Input | CWE-1284-improper-validation-of-specified-quantity-in-input |
| CWE-1285 | weakness | Base | Improper Validation of Specified Index, Position, or Offset in Input | Improper Validation of Specified Index, Position, or Offset in Input | CWE-1285-improper-validation-specified-index-position-offset-input |
| CWE-1286 | weakness | Base | Improper Validation of Syntactic Correctness of Input | Improper Validation of Syntactic Correctness of Input | CWE-1286-improper-validation-of-syntactic-correctness-of-input |
| CWE-1287 | weakness | Base | Improper Validation of Specified Type of Input | Improper Validation of Specified Type of Input | CWE-1287-improper-validation-of-specified-type-of-input |
| CWE-1288 | weakness | Base | Improper Validation of Consistency within Input | Improper Validation of Consistency within Input | CWE-1288-improper-validation-of-consistency-within-input |
| CWE-1289 | weakness | Base | Improper Validation of Unsafe Equivalence in Input | Improper Validation of Unsafe Equivalence in Input | CWE-1289-improper-validation-of-unsafe-equivalence-in-input |
| CWE-1290 | weakness | Base | Incorrect Decoding of Security Identifiers | Incorrect Decoding of Security Identifiers | CWE-1290-incorrect-decoding-of-security-identifiers |
| CWE-1291 | weakness | Base | Public Key Re-Use for Signing both Debug and Production Code | Public Key Re-Use for Signing both Debug and Production Code | CWE-1291-public-key-re-for-signing-both-debug-production |
| CWE-1292 | weakness | Base | Incorrect Conversion of Security Identifiers | Incorrect Conversion of Security Identifiers | CWE-1292-incorrect-conversion-of-security-identifiers |
| CWE-1293 | weakness | Base | Missing Source Correlation of Multiple Independent Data | Missing Source Correlation of Multiple Independent Data | CWE-1293-missing-source-correlation-of-multiple-independent-data |
| CWE-1294 | weakness | Class | Insecure Security Identifier Mechanism | Insecure Security Identifier Mechanism | CWE-1294-insecure-security-identifier-mechanism |
| CWE-1295 | weakness | Base | Debug Messages Revealing Unnecessary Information | Debug Messages Revealing Unnecessary Information | CWE-1295-debug-messages-revealing-unnecessary-information |
| CWE-1296 | weakness | Base | Incorrect Chaining or Granularity of Debug Components | Incorrect Chaining or Granularity of Debug Components | CWE-1296-incorrect-chaining-or-granularity-of-debug-components |
| CWE-1297 | weakness | Base | Unprotected Confidential Information on Device is Accessible by OSAT Vendors | Unprotected Confidential Information on Device is Accessible by OSAT Vendors | CWE-1297-unprotected-confidential-information-on-device-is-accessible |
| CWE-1298 | weakness | Base | Hardware Logic Contains Race Conditions | Hardware Logic Contains Race Conditions | CWE-1298-hardware-logic-contains-race-conditions |
| CWE-1299 | weakness | Base | Missing Protection Mechanism for Alternate Hardware Interface | Missing Protection Mechanism for Alternate Hardware Interface | CWE-1299-missing-protection-mechanism-for-alternate-hardware |
| CWE-1300 | weakness | Base | Improper Protection of Physical Side Channels | Improper Protection of Physical Side Channels | CWE-1300-improper-protection-of-physical-side-channels |
| CWE-1301 | weakness | Base | Insufficient or Incomplete Data Removal within Hardware Component | Insufficient or Incomplete Data Removal within Hardware Component | CWE-1301-insufficient-or-incomplete-data-removal-within-hardware |
| CWE-1302 | weakness | Base | Missing Source Identifier in Entity Transactions on a System-On-Chip | Missing Source Identifier in Entity Transactions on a System-On-Chip (SOC) | CWE-1302-missing-source-identifier-entity-transactions-on-system-on |
| CWE-1303 | weakness | Base | Non-Transparent Sharing of Microarchitectural Resources | Non-Transparent Sharing of Microarchitectural Resources | CWE-1303-non-transparent-sharing-of-microarchitectural-resources |
| CWE-1304 | weakness | Base | Improperly Preserved Integrity of Hardware Configuration State During a Power Save/Restore Operation | Improperly Preserved Integrity of Hardware Configuration State During a Power Save/Restore Operation | CWE-1304-improperly-preserved-integrity-hardware-configuration-state |
| CWE-1306 | category |  | CISQ Quality Measures - Reliability | CISQ Quality Measures - Reliability | CWE-1306-cisq-quality-measures-reliability |
| CWE-1307 | category |  | CISQ Quality Measures - Maintainability | CISQ Quality Measures - Maintainability | CWE-1307-cisq-quality-measures-maintainability |
| CWE-1308 | category |  | CISQ Quality Measures - Security | CISQ Quality Measures - Security | CWE-1308-cisq-quality-measures-security |
| CWE-1309 | category |  | CISQ Quality Measures - Efficiency | CISQ Quality Measures - Efficiency | CWE-1309-cisq-quality-measures-efficiency |
| CWE-1310 | weakness | Base | Missing Ability to Patch ROM Code | Missing Ability to Patch ROM Code | CWE-1310-missing-ability-to-patch-rom-code |
| CWE-1311 | weakness | Base | Improper Translation of Security Attributes by Fabric Bridge | Improper Translation of Security Attributes by Fabric Bridge | CWE-1311-improper-translation-of-security-attributes-by-fabric-bridge |
| CWE-1312 | weakness | Base | Missing Protection for Mirrored Regions in On-Chip Fabric Firewall | Missing Protection for Mirrored Regions in On-Chip Fabric Firewall | CWE-1312-missing-protection-for-mirrored-regions-on-chip-fabric |
| CWE-1313 | weakness | Base | Hardware Allows Activation of Test or Debug Logic at Runtime | Hardware Allows Activation of Test or Debug Logic at Runtime | CWE-1313-hardware-allows-activation-test-debug-logic-at-runtime |
| CWE-1314 | weakness | Base | Missing Write Protection for Parametric Data Values | Missing Write Protection for Parametric Data Values | CWE-1314-missing-write-protection-for-parametric-data-values |
| CWE-1315 | weakness | Base | Improper Setting of Bus Controlling Capability in Fabric End-point | Improper Setting of Bus Controlling Capability in Fabric End-point | CWE-1315-improper-setting-bus-controlling-capability-fabric-end-point |
| CWE-1316 | weakness | Base | Fabric-Address Map Allows Programming of Unwarranted Overlaps of Protected and Unprotected Ranges | Fabric-Address Map Allows Programming of Unwarranted Overlaps of Protected and Unprotected Ranges | CWE-1316-fabric-address-map-allows-programming-unwarranted-overlaps |
| CWE-1317 | weakness | Base | Improper Access Control in Fabric Bridge | Improper Access Control in Fabric Bridge | CWE-1317-improper-access-control-in-fabric-bridge |
| CWE-1318 | weakness | Base | Missing Support for Security Features in On-chip Fabrics or Buses | Missing Support for Security Features in On-chip Fabrics or Buses | CWE-1318-missing-support-for-security-features-on-chip-fabrics |
| CWE-1319 | weakness | Base | Improper Protection against Electromagnetic Fault Injection | Improper Protection against Electromagnetic Fault Injection (EM-FI) | CWE-1319-improper-protection-against-electromagnetic-fault-injection |
| CWE-1320 | weakness | Base | Improper Protection for Outbound Error Messages and Alert Signals | Improper Protection for Outbound Error Messages and Alert Signals | CWE-1320-improper-protection-for-outbound-error-messages-alert |
| CWE-1321 | weakness | Variant | Prototype Pollution | Improperly Controlled Modification of Object Prototype Attributes ('Prototype Pollution') | CWE-1321-prototype-pollution |
| CWE-1322 | weakness | Base | Use of Blocking Code in Single-threaded, Non-blocking Context | Use of Blocking Code in Single-threaded, Non-blocking Context | CWE-1322-blocking-code-single-threaded-non-blocking-context |
| CWE-1323 | weakness | Base | Improper Management of Sensitive Trace Data | Improper Management of Sensitive Trace Data | CWE-1323-improper-management-of-sensitive-trace-data |
| CWE-1324 | weakness | Base | DEPRECATED: Sensitive Information Accessible by Physical Probing of JTAG Interface | DEPRECATED: Sensitive Information Accessible by Physical Probing of JTAG Interface | CWE-1324-deprecated-sensitive-information-accessible-by-physical |
| CWE-1325 | weakness | Base | Improperly Controlled Sequential Memory Allocation | Improperly Controlled Sequential Memory Allocation | CWE-1325-improperly-controlled-sequential-memory-allocation |
| CWE-1326 | weakness | Base | Missing Immutable Root of Trust in Hardware | Missing Immutable Root of Trust in Hardware | CWE-1326-missing-immutable-root-of-trust-in-hardware |
| CWE-1327 | weakness | Base | Binding to an Unrestricted IP Address | Binding to an Unrestricted IP Address | CWE-1327-binding-to-an-unrestricted-ip-address |
| CWE-1328 | weakness | Base | Security Version Number Mutable to Older Versions | Security Version Number Mutable to Older Versions | CWE-1328-security-version-number-mutable-to-older-versions |
| CWE-1329 | weakness | Base | Reliance on Component That is Not Updateable | Reliance on Component That is Not Updateable | CWE-1329-reliance-on-component-that-is-not-updateable |
| CWE-1330 | weakness | Variant | Remanent Data Readable after Memory Erase | Remanent Data Readable after Memory Erase | CWE-1330-remanent-data-readable-after-memory-erase |
| CWE-1331 | weakness | Base | Improper Isolation of Shared Resources in Network On Chip | Improper Isolation of Shared Resources in Network On Chip (NoC) | CWE-1331-improper-isolation-shared-resources-network-on-chip |
| CWE-1332 | weakness | Base | Improper Handling of Faults that Lead to Instruction Skips | Improper Handling of Faults that Lead to Instruction Skips | CWE-1332-improper-handling-faults-that-lead-instruction-skips |
| CWE-1333 | weakness | Base | Inefficient Regular Expression Complexity | Inefficient Regular Expression Complexity | CWE-1333-inefficient-regular-expression-complexity |
| CWE-1334 | weakness | Base | Unauthorized Error Injection Can Degrade Hardware Redundancy | Unauthorized Error Injection Can Degrade Hardware Redundancy | CWE-1334-unauthorized-error-injection-can-degrade-hardware-redundancy |
| CWE-1335 | weakness | Base | Incorrect Bitwise Shift of Integer | Incorrect Bitwise Shift of Integer | CWE-1335-incorrect-bitwise-shift-of-integer |
| CWE-1336 | weakness | Base | Improper Neutralization of Special Elements Used in a Template Engine | Improper Neutralization of Special Elements Used in a Template Engine | CWE-1336-improper-neutralization-special-elements-template-engine |
| CWE-1338 | weakness | Base | Improper Protections Against Hardware Overheating | Improper Protections Against Hardware Overheating | CWE-1338-improper-protections-against-hardware-overheating |
| CWE-1339 | weakness | Base | Insufficient Precision or Accuracy of a Real Number | Insufficient Precision or Accuracy of a Real Number | CWE-1339-insufficient-precision-or-accuracy-of-a-real-number |
| CWE-1341 | weakness | Base | Multiple Releases of Same Resource or Handle | Multiple Releases of Same Resource or Handle | CWE-1341-multiple-releases-of-same-resource-or-handle |
| CWE-1342 | weakness | Base | Information Exposure through Microarchitectural State after Transient Execution | Information Exposure through Microarchitectural State after Transient Execution | CWE-1342-information-exposure-through-microarchitectural-state-after |
| CWE-1345 | category |  | OWASP Top Ten 2021 Category A01:2021 - Broken Access Control | OWASP Top Ten 2021 Category A01:2021 - Broken Access Control | CWE-1345-owasp-top-ten-2021-category-a01-2021-broken |
| CWE-1346 | category |  | OWASP Top Ten 2021 Category A02:2021 - Cryptographic Failures | OWASP Top Ten 2021 Category A02:2021 - Cryptographic Failures | CWE-1346-owasp-top-ten-2021-category-a02-2021-cryptographic |
| CWE-1347 | category |  | OWASP Top Ten 2021 Category A03:2021 - Injection | OWASP Top Ten 2021 Category A03:2021 - Injection | CWE-1347-owasp-top-ten-2021-category-a03-2021-injection |
| CWE-1348 | category |  | OWASP Top Ten 2021 Category A04:2021 - Insecure Design | OWASP Top Ten 2021 Category A04:2021 - Insecure Design | CWE-1348-owasp-top-ten-2021-category-a04-2021-insecure |
| CWE-1349 | category |  | OWASP Top Ten 2021 Category A05:2021 - Security Misconfiguration | OWASP Top Ten 2021 Category A05:2021 - Security Misconfiguration | CWE-1349-owasp-top-ten-2021-category-a05-2021-security |
| CWE-1351 | weakness | Base | Improper Handling of Hardware Behavior in Exceptionally Cold Environments | Improper Handling of Hardware Behavior in Exceptionally Cold Environments | CWE-1351-improper-handling-hardware-behavior-exceptionally-cold |
| CWE-1352 | category |  | OWASP Top Ten 2021 Category A06:2021 - Vulnerable and Outdated Components | OWASP Top Ten 2021 Category A06:2021 - Vulnerable and Outdated Components | CWE-1352-owasp-top-ten-2021-category-a06-2021-vulnerable |
| CWE-1353 | category |  | OWASP Top Ten 2021 Category A07:2021 - Identification and Authentication Failures | OWASP Top Ten 2021 Category A07:2021 - Identification and Authentication Failures | CWE-1353-owasp-top-ten-2021-category-a07-2021-identification |
| CWE-1354 | category |  | OWASP Top Ten 2021 Category A08:2021 - Software and Data Integrity Failures | OWASP Top Ten 2021 Category A08:2021 - Software and Data Integrity Failures | CWE-1354-owasp-top-ten-2021-category-a08-2021-software |
| CWE-1355 | category |  | OWASP Top Ten 2021 Category A09:2021 - Security Logging and Monitoring Failures | OWASP Top Ten 2021 Category A09:2021 - Security Logging and Monitoring Failures | CWE-1355-owasp-top-ten-2021-category-a09-2021-security |
| CWE-1356 | category |  | OWASP Top Ten 2021 Category A10:2021 - Server-Side Request Forgery | OWASP Top Ten 2021 Category A10:2021 - Server-Side Request Forgery (SSRF) | CWE-1356-owasp-top-ten-2021-category-a10-2021-server |
| CWE-1357 | weakness | Class | Reliance on Insufficiently Trustworthy Component | Reliance on Insufficiently Trustworthy Component | CWE-1357-reliance-on-insufficiently-trustworthy-component |
| CWE-1359 | category |  | ICS Communications | ICS Communications | CWE-1359-ics-communications |
| CWE-1360 | category |  | ICS Dependencies | ICS Dependencies (& Architecture) | CWE-1360-ics-dependencies |
| CWE-1361 | category |  | ICS Supply Chain | ICS Supply Chain | CWE-1361-ics-supply-chain |
| CWE-1362 | category |  | ICS Engineering | ICS Engineering (Constructions/Deployment) | CWE-1362-ics-engineering |
| CWE-1363 | category |  | ICS Operations | ICS Operations (& Maintenance) | CWE-1363-ics-operations |
| CWE-1364 | category |  | ICS Communications: Zone Boundary Failures | ICS Communications: Zone Boundary Failures | CWE-1364-ics-communications-zone-boundary-failures |
| CWE-1365 | category |  | ICS Communications: Unreliability | ICS Communications: Unreliability | CWE-1365-ics-communications-unreliability |
| CWE-1366 | category |  | ICS Communications: Frail Security in Protocols | ICS Communications: Frail Security in Protocols | CWE-1366-ics-communications-frail-security-in-protocols |
| CWE-1367 | category |  | ICS Dependencies : External Physical Systems | ICS Dependencies (& Architecture): External Physical Systems | CWE-1367-ics-dependencies-external-physical-systems |
| CWE-1368 | category |  | ICS Dependencies : External Digital Systems | ICS Dependencies (& Architecture): External Digital Systems | CWE-1368-ics-dependencies-external-digital-systems |
| CWE-1369 | category |  | ICS Supply Chain: IT/OT Convergence/Expansion | ICS Supply Chain: IT/OT Convergence/Expansion | CWE-1369-ics-supply-chain-it-ot-convergence-expansion |
| CWE-1370 | category |  | ICS Supply Chain: Common Mode Frailties | ICS Supply Chain: Common Mode Frailties | CWE-1370-ics-supply-chain-common-mode-frailties |
| CWE-1371 | category |  | ICS Supply Chain: Poorly Documented or Undocumented Features | ICS Supply Chain: Poorly Documented or Undocumented Features | CWE-1371-ics-supply-chain-poorly-documented-or-undocumented-features |
| CWE-1372 | category |  | ICS Supply Chain: OT Counterfeit and Malicious Corruption | ICS Supply Chain: OT Counterfeit and Malicious Corruption | CWE-1372-ics-supply-chain-ot-counterfeit-and-malicious-corruption |
| CWE-1373 | category |  | ICS Engineering : Trust Model Problems | ICS Engineering (Construction/Deployment): Trust Model Problems | CWE-1373-ics-engineering-trust-model-problems |
| CWE-1374 | category |  | ICS Engineering : Maker Breaker Blindness | ICS Engineering (Construction/Deployment): Maker Breaker Blindness | CWE-1374-ics-engineering-maker-breaker-blindness |
| CWE-1375 | category |  | ICS Engineering : Gaps in Details/Data | ICS Engineering (Construction/Deployment): Gaps in Details/Data | CWE-1375-ics-engineering-gaps-in-details-data |
| CWE-1376 | category |  | ICS Engineering : Security Gaps in Commissioning | ICS Engineering (Construction/Deployment): Security Gaps in Commissioning | CWE-1376-ics-engineering-security-gaps-in-commissioning |
| CWE-1377 | category |  | ICS Engineering : Inherent Predictability in Design | ICS Engineering (Construction/Deployment): Inherent Predictability in Design | CWE-1377-ics-engineering-inherent-predictability-in-design |
| CWE-1378 | category |  | ICS Operations : Gaps in obligations and training | ICS Operations (& Maintenance): Gaps in obligations and training | CWE-1378-ics-operations-gaps-in-obligations-and-training |
| CWE-1379 | category |  | ICS Operations : Human factors in ICS environments | ICS Operations (& Maintenance): Human factors in ICS environments | CWE-1379-ics-operations-human-factors-in-ics-environments |
| CWE-1380 | category |  | ICS Operations : Post-analysis changes | ICS Operations (& Maintenance): Post-analysis changes | CWE-1380-ics-operations-post-analysis-changes |
| CWE-1381 | category |  | ICS Operations : Exploitable Standard Operational Procedures | ICS Operations (& Maintenance): Exploitable Standard Operational Procedures | CWE-1381-ics-operations-exploitable-standard-operational-procedures |
| CWE-1382 | category |  | ICS Operations : Emerging Energy Technologies | ICS Operations (& Maintenance): Emerging Energy Technologies | CWE-1382-ics-operations-emerging-energy-technologies |
| CWE-1383 | category |  | ICS Operations : Compliance/Conformance with Regulatory Requirements | ICS Operations (& Maintenance): Compliance/Conformance with Regulatory Requirements | CWE-1383-ics-operations-compliance-conformance-with-regulatory |
| CWE-1384 | weakness | Class | Improper Handling of Physical or Environmental Conditions | Improper Handling of Physical or Environmental Conditions | CWE-1384-improper-handling-of-physical-or-environmental-conditions |
| CWE-1385 | weakness | Variant | Missing Origin Validation in WebSockets | Missing Origin Validation in WebSockets | CWE-1385-missing-origin-validation-in-websockets |
| CWE-1386 | weakness | Base | Insecure Operation on Windows Junction / Mount Point | Insecure Operation on Windows Junction / Mount Point | CWE-1386-insecure-operation-on-windows-junction-mount-point |
| CWE-1388 | category |  | Physical Access Issues and Concerns | Physical Access Issues and Concerns | CWE-1388-physical-access-issues-and-concerns |
| CWE-1389 | weakness | Base | Incorrect Parsing of Numbers with Different Radices | Incorrect Parsing of Numbers with Different Radices | CWE-1389-incorrect-parsing-of-numbers-with-different-radices |
| CWE-1390 | weakness | Class | Weak Authentication | Weak Authentication | CWE-1390-weak-authentication |
| CWE-1391 | weakness | Class | Use of Weak Credentials | Use of Weak Credentials | CWE-1391-use-of-weak-credentials |
| CWE-1392 | weakness | Base | Use of Default Credentials | Use of Default Credentials | CWE-1392-use-of-default-credentials |
| CWE-1393 | weakness | Base | Use of Default Password | Use of Default Password | CWE-1393-use-of-default-password |
| CWE-1394 | weakness | Base | Use of Default Cryptographic Key | Use of Default Cryptographic Key | CWE-1394-use-of-default-cryptographic-key |
| CWE-1395 | weakness | Class | Dependency on Vulnerable Third-Party Component | Dependency on Vulnerable Third-Party Component | CWE-1395-dependency-on-vulnerable-third-party-component |
| CWE-1396 | category |  | Comprehensive Categorization: Access Control | Comprehensive Categorization: Access Control | CWE-1396-comprehensive-categorization-access-control |
| CWE-1397 | category |  | Comprehensive Categorization: Comparison | Comprehensive Categorization: Comparison | CWE-1397-comprehensive-categorization-comparison |
| CWE-1398 | category |  | Comprehensive Categorization: Component Interaction | Comprehensive Categorization: Component Interaction | CWE-1398-comprehensive-categorization-component-interaction |
| CWE-1399 | category |  | Comprehensive Categorization: Memory Safety | Comprehensive Categorization: Memory Safety | CWE-1399-comprehensive-categorization-memory-safety |
| CWE-1401 | category |  | Comprehensive Categorization: Concurrency | Comprehensive Categorization: Concurrency | CWE-1401-comprehensive-categorization-concurrency |
| CWE-1402 | category |  | Comprehensive Categorization: Encryption | Comprehensive Categorization: Encryption | CWE-1402-comprehensive-categorization-encryption |
| CWE-1403 | category |  | Comprehensive Categorization: Exposed Resource | Comprehensive Categorization: Exposed Resource | CWE-1403-comprehensive-categorization-exposed-resource |
| CWE-1404 | category |  | Comprehensive Categorization: File Handling | Comprehensive Categorization: File Handling | CWE-1404-comprehensive-categorization-file-handling |
| CWE-1405 | category |  | Comprehensive Categorization: Improper Check or Handling of Exceptional Conditions | Comprehensive Categorization: Improper Check or Handling of Exceptional Conditions | CWE-1405-comprehensive-categorization-improper-check-handling |
| CWE-1406 | category |  | Comprehensive Categorization: Improper Input Validation | Comprehensive Categorization: Improper Input Validation | CWE-1406-comprehensive-categorization-improper-input-validation |
| CWE-1407 | category |  | Comprehensive Categorization: Improper Neutralization | Comprehensive Categorization: Improper Neutralization | CWE-1407-comprehensive-categorization-improper-neutralization |
| CWE-1408 | category |  | Comprehensive Categorization: Incorrect Calculation | Comprehensive Categorization: Incorrect Calculation | CWE-1408-comprehensive-categorization-incorrect-calculation |
| CWE-1409 | category |  | Comprehensive Categorization: Injection | Comprehensive Categorization: Injection | CWE-1409-comprehensive-categorization-injection |
| CWE-1410 | category |  | Comprehensive Categorization: Insufficient Control Flow Management | Comprehensive Categorization: Insufficient Control Flow Management | CWE-1410-comprehensive-categorization-insufficient-control-flow |
| CWE-1411 | category |  | Comprehensive Categorization: Insufficient Verification of Data Authenticity | Comprehensive Categorization: Insufficient Verification of Data Authenticity | CWE-1411-comprehensive-categorization-insufficient-verification-of |
| CWE-1412 | category |  | Comprehensive Categorization: Poor Coding Practices | Comprehensive Categorization: Poor Coding Practices | CWE-1412-comprehensive-categorization-poor-coding-practices |
| CWE-1413 | category |  | Comprehensive Categorization: Protection Mechanism Failure | Comprehensive Categorization: Protection Mechanism Failure | CWE-1413-comprehensive-categorization-protection-mechanism-failure |
| CWE-1414 | category |  | Comprehensive Categorization: Randomness | Comprehensive Categorization: Randomness | CWE-1414-comprehensive-categorization-randomness |
| CWE-1415 | category |  | Comprehensive Categorization: Resource Control | Comprehensive Categorization: Resource Control | CWE-1415-comprehensive-categorization-resource-control |
| CWE-1416 | category |  | Comprehensive Categorization: Resource Lifecycle Management | Comprehensive Categorization: Resource Lifecycle Management | CWE-1416-comprehensive-categorization-resource-lifecycle-management |
| CWE-1417 | category |  | Comprehensive Categorization: Sensitive Information Exposure | Comprehensive Categorization: Sensitive Information Exposure | CWE-1417-comprehensive-categorization-sensitive-information-exposure |
| CWE-1418 | category |  | Comprehensive Categorization: Violation of Secure Design Principles | Comprehensive Categorization: Violation of Secure Design Principles | CWE-1418-comprehensive-categorization-violation-of-secure-design |
| CWE-1419 | weakness | Class | Incorrect Initialization of Resource | Incorrect Initialization of Resource | CWE-1419-incorrect-initialization-of-resource |
| CWE-1420 | weakness | Base | Exposure of Sensitive Information during Transient Execution | Exposure of Sensitive Information during Transient Execution | CWE-1420-exposure-of-sensitive-information-during-transient-execution |
| CWE-1421 | weakness | Base | Exposure of Sensitive Information in Shared Microarchitectural Structures during Transient Execution | Exposure of Sensitive Information in Shared Microarchitectural Structures during Transient Execution | CWE-1421-exposure-sensitive-information-shared-microarchitectural |
| CWE-1422 | weakness | Base | Exposure of Sensitive Information caused by Incorrect Data Forwarding during Transient Execution | Exposure of Sensitive Information caused by Incorrect Data Forwarding during Transient Execution | CWE-1422-exposure-sensitive-information-caused-by-incorrect-data |
| CWE-1423 | weakness | Base | Exposure of Sensitive Information caused by Shared Microarchitectural Predictor State that Influences Transient Execution | Exposure of Sensitive Information caused by Shared Microarchitectural Predictor State that Influences Transient Execution | CWE-1423-exposure-sensitive-information-caused-by-shared |
| CWE-1426 | weakness | Base | Improper Validation of Generative AI Output | Improper Validation of Generative AI Output | CWE-1426-improper-validation-of-generative-ai-output |
| CWE-1427 | weakness | Base | Improper Neutralization of Input Used for LLM Prompting | Improper Neutralization of Input Used for LLM Prompting | CWE-1427-improper-neutralization-of-input-used-for-llm-prompting |
| CWE-1428 | weakness | Base | Reliance on HTTP instead of HTTPS | Reliance on HTTP instead of HTTPS | CWE-1428-reliance-on-http-instead-of-https |
| CWE-1429 | weakness | Base | Missing Security-Relevant Feedback for Unexecuted Operations in Hardware Interface | Missing Security-Relevant Feedback for Unexecuted Operations in Hardware Interface | CWE-1429-missing-security-relevant-feedback-for-unexecuted-operations |
| CWE-1431 | weakness | Base | Driving Intermediate Cryptographic State/Results to Hardware Module Outputs | Driving Intermediate Cryptographic State/Results to Hardware Module Outputs | CWE-1431-driving-intermediate-cryptographic-state-results-hardware |
| CWE-1433 | category |  | 2025 MIHW Supplement: Expert Insights | 2025 MIHW Supplement: Expert Insights | CWE-1433-2025-mihw-supplement-expert-insights |
| CWE-1434 | weakness | Base | Insecure Setting of Generative AI/ML Model Inference Parameters | Insecure Setting of Generative AI/ML Model Inference Parameters | CWE-1434-insecure-setting-generative-ai-ml-model-inference-parameters |
| CWE-1436 | category |  | OWASP Top Ten 2025 Category A01:2025 - Broken Access Control | OWASP Top Ten 2025 Category A01:2025 - Broken Access Control | CWE-1436-owasp-top-ten-2025-category-a01-2025-broken |
| CWE-1437 | category |  | OWASP Top Ten 2025 Category A02:2025 - Security Misconfiguration | OWASP Top Ten 2025 Category A02:2025 - Security Misconfiguration | CWE-1437-owasp-top-ten-2025-category-a02-2025-security |
| CWE-1438 | category |  | OWASP Top Ten 2025 Category A03:2025 - Software Supply Chain Failures | OWASP Top Ten 2025 Category A03:2025 - Software Supply Chain Failures | CWE-1438-owasp-top-ten-2025-category-a03-2025-software |
| CWE-1439 | category |  | OWASP Top Ten 2025 Category A04:2025 - Cryptographic Failures | OWASP Top Ten 2025 Category A04:2025 - Cryptographic Failures | CWE-1439-owasp-top-ten-2025-category-a04-2025-cryptographic |
| CWE-1440 | category |  | OWASP Top Ten 2025 Category A05:2025 - Injection | OWASP Top Ten 2025 Category A05:2025 - Injection | CWE-1440-owasp-top-ten-2025-category-a05-2025-injection |
| CWE-1441 | category |  | OWASP Top Ten 2025 Category A06:2025 - Insecure Design | OWASP Top Ten 2025 Category A06:2025 - Insecure Design | CWE-1441-owasp-top-ten-2025-category-a06-2025-insecure |
| CWE-1442 | category |  | OWASP Top Ten 2025 Category A07:2025 - Authentication Failures | OWASP Top Ten 2025 Category A07:2025 - Authentication Failures | CWE-1442-owasp-top-ten-2025-category-a07-2025-authentication |
| CWE-1443 | category |  | OWASP Top Ten 2025 Category A08:2025 - Software or Data Integrity Failures | OWASP Top Ten 2025 Category A08:2025 - Software or Data Integrity Failures | CWE-1443-owasp-top-ten-2025-category-a08-2025-software |
| CWE-1444 | category |  | OWASP Top Ten 2025 Category A09:2025 - Logging & Alerting Failures | OWASP Top Ten 2025 Category A09:2025 - Logging & Alerting Failures | CWE-1444-owasp-top-ten-2025-category-a09-2025-logging |
| CWE-1445 | category |  | OWASP Top Ten 2025 Category A10:2025 - Mishandling of Exceptional Conditions | OWASP Top Ten 2025 Category A10:2025 - Mishandling of Exceptional Conditions | CWE-1445-owasp-top-ten-2025-category-a10-2025-mishandling |
| CWE-1446 | category |  | Weaknesses That are Specific to AI/ML Technology | Weaknesses That are Specific to AI/ML Technology | CWE-1446-weaknesses-that-are-specific-to-ai-ml-technology |
| CWE-1447 | category |  | General Software Weaknesses that Appear in Products that Use or Support AI/ML Technology | General Software Weaknesses that Appear in Products that Use or Support AI/ML Technology | CWE-1447-general-software-weaknesses-that-appear-products-that |
