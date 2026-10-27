# PHP-to-Python Migration Audit: `fix_refs`

Comparative technical report, feature coverage, outstanding work, behavioral differences, and testing gaps

## 1. Executive summary

The objective is to replace the existing PHP implementation of `fix_refs` with the Python implementation while preserving the original system's functionality, output, and behavior.

The comparison covers:

- PHP repository: [Mdwiki-TD/fix_refs](https://github.com/Mdwiki-TD/fix_refs)
- Python repository: [MrIbrahem/fix_refs_new_py](https://github.com/MrIbrahem/fix_refs_new_py)

Based on the directory trees provided, the Python project has a substantial foundation and apparent counterparts for many of the PHP system's principal features, including reference processing, language-specific bots, infobox processing, citation parsing, category handling, and general text fixes.

However, having a corresponding file does not establish that a feature has been fully migrated. A Python module may implement only part of its PHP counterpart, use a different algorithm, omit edge cases, or lack integration with the main processing pipeline.

The most important migration questions are therefore:

1. Which PHP capabilities have equivalent Python implementations?
2. Which capabilities are only partially implemented or have no visible counterpart?
3. Which behavioral differences could change the wikitext output?
4. Which PHP tests, validation routines, or diagnostic checks are absent from Python?
5. What evidence is needed before Python can safely replace PHP in production?

### Initial assessment

Broad feature coverage

The Python tree contains apparent counterparts for many of the PHP feature groups.

Implementation parity not yet established

File names and directory structure alone cannot confirm semantic equivalence.

Testing parity requires verification

Neither the presence nor the absence of actual test coverage can be conclusively established from the supplied trees.

Scope limitation: This is a preliminary repository-structure audit, not a verified line-by-line source-code audit. The supplied material identifies file locations but does not include their contents, test files, CI configuration, commit history, or execution results. Consequently, the report distinguishes observed structural facts from migration risks and items requiring verification. It does not claim that either repository has been fully tested.

## 2. Repository architecture comparison

The two projects share a recognizable functional structure, but they do not have identical architectures. Python appears to reorganize some PHP functionality into broader modules, while the PHP project contains a more explicit collection of parser classes and data models.

| PHP component               | Python counterpart                                                      | Preliminary status                             |
| --------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------- |
| `app/Fix/Bots/`             | `fixers/` and `fixers/refs/`                                            | Broad functional coverage                      |
| `app/Fix/HelpsBots/`        | `fixers/` and `lang_bots/`                                              | Broad functional coverage                      |
| `app/Fix/Infoboxes/`        | `infobox/`                                                              | Counterparts present                           |
| `app/Fix/LangBots/`         | `lang_bots/`                                                            | Broad functional coverage                      |
| `app/Fix/Parse/`            | `parsers/` and `mdwiki/`                                                | Partial structural correspondence              |
| `app/Fix/WikiParse/`        | `parsers/`, `fixers/refs/wtp_mapping.py`, possibly a third-party parser | No complete one-to-one mapping visible         |
| `app/Wikibots/Wikitext.php` | Possibly `core/`, `utils/`, or parser integration                       | Requires source inspection                     |
| `app/Index.php`             | Possibly `core/fix_page.py` or `core/fix_page_wrapper.py`               | Entry-point equivalence unverified             |
| `app/Run.php`               | Possibly `core/fix_page_wrapper.py` or another runner                   | Requires source inspection                     |
| `app/LanguageSettings.php`  | `config.py`, `core/settings.py`, possibly `core/mapping.py`             | Configuration may be redistributed             |
| `app/Logger.php`            | No obvious dedicated counterpart                                        | Potential gap                                  |
| `app/Csrf.php`              | No obvious dedicated counterpart                                        | Web-security functionality may be out of scope |
| `bootstrap.php`             | Python initialization and package imports                               | No direct counterpart visible                  |
| `index.php`, `work.php`     | No obvious web entry-point equivalents                                  | Potential deployment or interface gap          |

These mappings are based on likely responsibilities inferred from names, not confirmed call graphs.

### Architectural implications

Three differences deserve particular attention.

1\. PHP has an explicit wiki parser subsystem.

The PHP `WikiParse` directory contains seven parser implementation files and eight data-model files. This suggests a dedicated parsing architecture for templates, parameters, tags, links, tables, categories, and citations.

Python has a smaller, differently organized parser-related structure. It may rely on an external parser library or distribute equivalent logic among several modules. The tree alone cannot establish whether that is a functional improvement, an intentional simplification, or a missing migration.

2\. Python separates reference processing more explicitly.

Python has a dedicated `fixers/refs/` package containing reference expansion, missing-reference handling, reference movement, duplicate removal, and mapping logic. PHP distributes corresponding work among `Bots/`, `HelpsBots/`, and `Parse/`.

This separation may improve maintainability, but it also makes integration testing important: individual Python fixers may work independently without reproducing the order or interactions of the original PHP pipeline.

3\. PHP exposes application and web entry points.

The PHP tree includes `index.php`, `work.php`, `bootstrap.php`, `Run.php`, CSRF handling, and logging. Python includes a core processing layer and configuration, but no obvious direct counterparts for all of these files.

This is a gap only if the replacement must reproduce the same web interface, request handling, deployment model, and operational behavior. If Python is intended solely as a replacement processing engine, some of those components may intentionally be out of scope.

## 3. Feature-by-feature migration inventory

The following inventory identifies the apparent Python counterpart for each PHP feature, what can be concluded from the structure, and what needs to be checked in the actual implementation.

### 3.1 General-purpose fixes and reference utilities

PHP: `src/app/Fix/Bots/` · Python: `fixers/` and `fixers/refs/`

| PHP file                  | Likely Python counterpart              | Audit finding                                                                          |
| ------------------------- | -------------------------------------- | -------------------------------------------------------------------------------------- |
| `AttrsUtils.php`          | No obvious dedicated file              | Check whether attribute parsing and normalization were migrated or absorbed elsewhere. |
| `ExpendRefs.php`          | `fixers/refs/expend_refs.py`           | Directly corresponding feature; implementation parity unverified.                      |
| `MiniFixesBot.php`        | `fixers/mini_fixes.py`                 | Directly corresponding feature.                                                        |
| `MonthsNewValue.php`      | `fixers/months.py`                     | Likely counterpart; verify supported languages, formats, and month-name mappings.      |
| `RedirectHelp.php`        | `fixers/redirect.py`                   | Directly corresponding feature.                                                        |
| `RefsUtils.php`           | `fixers/refs_utils.py`                 | Directly corresponding utility module.                                                 |
| `RemoveDuplicateRefs.php` | `fixers/refs/remove_duplicate_refs.py` | Directly corresponding feature.                                                        |
| `TxtLib2.php`             | No obvious dedicated file              | Check for missing string, text, or wikitext helper functions.                          |

Priority checks

- Whether reference names and attributes are normalized consistently.
- Whether duplicate detection accounts for named references, self-closing references, and references with bodies.
- Whether redirect handling distinguishes redirect pages from ordinary links.
- Whether month conversion handles all original languages, capitalization patterns, and date formats.
- Whether helper functions preserve comments, whitespace, and unrelated text.

The two files with no obvious dedicated counterparts, `AttrsUtils.php` and `TxtLib2.php`, are important audit targets. Their functions may have been consolidated into Python utilities, but that must be demonstrated by searching for their public methods and comparing their callers.

### 3.2 Helper bots

PHP: `src/app/Fix/HelpsBots/` · Python: `fixers/` and `lang_bots/`

| PHP file          | Python counterpart                | Audit finding                                                     |
| ----------------- | --------------------------------- | ----------------------------------------------------------------- |
| `EnLangParam.php` | `fixers/add_lang_en_bot.py`       | Likely migrated. Verify parameter insertion rules and exclusions. |
| `MissingRefs.php` | `fixers/refs/fix_missing_refs.py` | Directly corresponding feature.                                   |
| `MvDots.php`      | `fixers/move_dots.py`             | Directly corresponding feature.                                   |
| `RemoveSpace.php` | `lang_bots/remove_space.py`       | Directly corresponding feature.                                   |

These four mappings provide strong structural evidence that the associated feature groups were considered in the Python rewrite. They do not prove that every rule, exception, or execution condition was ported.

For example, moving punctuation around citations is particularly sensitive to ordering and markup boundaries. The Python implementation should be tested against cases involving multiple citations, punctuation inside templates, and existing punctuation that must not be moved.

### 3.3 Infobox processing

PHP: `src/app/Fix/Infoboxes/` · Python: `infobox/`

| PHP file       | Python counterpart                            | Audit finding                                                 |
| -------------- | --------------------------------------------- | ------------------------------------------------------------- |
| `Infobox.php`  | `infobox/expend_infobox.py`                   | Possible counterpart; verify the scope of the original class. |
| `Infobox2.php` | `infobox/expend_infobox.py` or another module | No separate one-to-one counterpart is visible.                |

The Python project contains an infobox expansion module, but the PHP project contains two infobox files. This is a possible consolidation or omission, not proof that a feature is missing.

To resolve it, compare:

- Public methods and supported template names.
- Parameter extraction and insertion rules.
- Handling of nested templates and multiline parameters.
- Default values, aliases, and missing-field behavior.
- Error handling for malformed infoboxes.
- Whether the two PHP files represent distinct features or successive implementations of the same functionality.

If both PHP classes contain independent rules, the Python version must preserve both sets of behavior.

### 3.4 Language-specific bots

PHP: `src/app/Fix/LangBots/` · Python: `lang_bots/`

| Language / feature   | PHP implementation                           | Python implementation                           | Assessment                                              |
| -------------------- | -------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------- |
| Bulgarian            | `BgBots/FixBg.php`                           | `bg_bot.py`                                     | Direct counterpart                                      |
| Spanish main bot     | `EsBots/Es.php`                              | `es/es_bot.py`                                  | Direct counterpart                                      |
| Spanish months       | `EsBots/EsMonths.php`                        | `fixers/months.py` and possibly `es/es_data.py` | Responsibilities may be combined                        |
| Spanish references   | `EsBots/EsRefs.php`                          | `es/es_refs.py`                                 | Direct counterpart                                      |
| Spanish sections     | `EsBots/Section.php`                         | `es/es_section_bot.py`                          | Direct counterpart                                      |
| Polish infobox       | `PlBots/FixPlInfobox.php`                    | `pl_bot.py` and/or `infobox/`                   | Exact division of responsibility unverified             |
| Portuguese months    | `PtBots/FixPtMonths.php`                     | `fixers/months.py`                              | Possible consolidation                                  |
| Swahili              | `SwBot.php`                                  | `sw_bot.py`                                     | Direct counterpart                                      |
| Armenian             | No explicit counterpart in supplied PHP tree | `hy_bot.py`                                     | Python-only visible feature; verify whether intentional |
| Spanish data/helpers | No dedicated files in the same form          | `es/es_data.py`, `es/es_helpers.py`             | Python-specific organization                            |

The Armenian bot deserves special attention. `hy_bot.py` has no obvious matching file in the supplied PHP tree. It may be a new feature, a port of logic stored elsewhere in PHP, or an intentional expansion of the system.

Similarly, Python's Spanish data and helper modules may reflect a useful separation of concerns, but their functions should be mapped to the PHP Spanish implementation to identify any unported rules.

Required language-specific regression tests

For each language bot, verify:

1. All supported transformations and their exclusions.
2. Language-specific template aliases and parameter names.
3. Localized month names and abbreviations.
4. Unicode and capitalization behavior.
5. Preservation of links, references, templates, and comments.
6. Idempotency: running the fixer twice should not produce additional unintended changes.

A bot should not be marked complete simply because a same-named module exists.

### 3.5 Citation and category parsing

PHP: `src/app/Fix/Parse/` · Python: `parsers/` and `mdwiki/`

| PHP file                 | Python counterpart                          | Assessment                                                                                        |
| ------------------------ | ------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `Parse/Category.php`     | `parsers/category.py`, `mdwiki/category.py` | Two possible counterparts; determine whether both PHP and Python modules' responsibilities align. |
| `Parse/Citations.php`    | `parsers/citation.py`                       | Likely counterpart.                                                                               |
| `Parse/CitationsReg.php` | `parsers/citations_parser.py`               | Likely counterpart; regular-expression behavior requires comparison.                              |

The separate PHP files `Citations.php` and `CitationsReg.php` suggest that citation processing may involve distinct implementations or responsibilities. Python also has two citation-related modules, but their names alone do not establish equivalent behavior.

The category modules also deserve examination because Python contains category processing in both `parsers/` and `mdwiki/`. Confirm that they are not competing implementations with different normalization or filtering rules.

### 3.6 Wiki parsing subsystem

The PHP parser subsystem is one of the most important areas to audit before declaring the migration complete.

The PHP tree explicitly lists these data models:

| PHP data model     | What Python parity must preserve                           |
| ------------------ | ---------------------------------------------------------- |
| `Attribute.php`    | Attribute values, quoting, escaping, and normalization     |
| `Citation.php`     | Citation structure, attributes, and body representation    |
| `ExternalLink.php` | External-link boundaries and URL/text handling             |
| `InternalLink.php` | Target, display text, and link boundaries                  |
| `Parameters.php`   | Parameter names, values, duplicates, and formatting        |
| `Table.php`        | Table boundaries and structural handling                   |
| `Tag.php`          | Tag names, attributes, self-closing tags, and body content |
| `Template.php`     | Template boundaries, parameters, nesting, and formatting   |

The corresponding PHP parser files are:

- `ParserCategories.php`
- `ParserCitations.php`
- `ParserExternalLinks.php`
- `ParserInternalLinks.php`
- `ParserTags.php`
- `ParserTemplate.php`
- `ParserTemplates.php`

There are no direct equivalents for this full class collection visible in the Python tree.

Python does have `fixers/refs/wtp_mapping.py` and parser-related modules, and its README files may document an external parsing dependency. It is therefore not justified to conclude that these capabilities are absent. Instead, the migration must establish whether they are implemented in Python, delegated to a library, or omitted.

Critical compatibility issue: wiki markup is nested and context-sensitive. A regular-expression transformation that works for simple examples may fail when a template contains a reference, a tag contains a template, or a parameter contains an equals sign.

The replacement should be checked against nested templates, pipes and equals signs inside nested expressions, comments, literal tags, malformed markup, and multiline structures.

## 4. Core processing, runtime, and integration

The Python core contains:

- `core/fix_page.py`
- `core/fix_page_wrapper.py`
- `core/mapping.py`
- `core/settings.py`

The PHP application contains:

- `Index.php`
- `MdCat.php`
- `Run.php`
- `LanguageSettings.php`
- `Logger.php`
- `Csrf.php`
- `Wikibots/Wikitext.php`

The key migration question is not merely whether the same fixes exist, but whether they run under equivalent conditions.

### 4.1 Processing pipeline

The Python entry points should be compared with the PHP runtime to verify:

- Which fixers are enabled by default.
- The order in which fixers execute.
- Whether language-specific bots run conditionally.
- How input text, page titles, languages, and configuration are passed.
- Whether a fixer can prevent later fixers from executing.
- Whether exceptions are logged, propagated, or silently ignored.
- Whether the pipeline returns the same output format.
- Whether changes are applied once or through repeated passes.

The order is especially important. Suppose one fixer changes reference attributes and another removes duplicate references. If PHP performs normalization before duplicate detection but Python reverses the order, the two implementations can produce different results even if both contain equivalent algorithms.

### 4.2 Configuration and mappings

Compare `LanguageSettings.php` with `core/settings.py`, `core/mapping.py`, and `config.py`.

The audit should establish whether Python preserves:

- Supported language codes and aliases.
- Language-specific feature switches.
- Template and parameter mappings.
- Default values and fallback behavior.
- Site-specific exceptions.
- Configuration precedence.
- Behavior for unsupported or missing language settings.

A mapping mismatch can cause an apparently functioning fixer to operate on the wrong templates or skip a language entirely.

### 4.3 Logging and operational behavior

The PHP project has an explicit `Logger.php`, whereas the Python tree does not show an obvious dedicated logging module.

This does not prove logging is missing; Python may use the standard `logging` module or logging embedded in the core.

Verify that the Python application records enough information to diagnose:

- Processing failures.
- Skipped pages and skipped fixers.
- Unexpected or malformed markup.
- Before-and-after changes where appropriate.
- Configuration and language-selection errors.
- External service or API failures, if applicable.

If the PHP application exposes a web interface, its CSRF protection and request validation must also be assessed separately. These are application-security requirements, not wikitext transformation features, and they should not be considered automatically migrated merely because the Python processing engine works.

## 5. What is complete, partially complete, and remaining?

A reliable status report must distinguish structural evidence from verified implementation evidence. Based on the supplied trees, the following is the most defensible classification.

Structurally represented

Reference expansion, duplicate removal, missing-reference handling, general fixes, redirect handling, month processing, punctuation movement, language bots, Spanish references, and category/citation processing have apparent Python counterparts.

Partially verified / needs comparison

Infobox processing, the wiki parsing subsystem, category and citation parsing, configuration, language mappings, and the main processing pipeline need source-level parity checks.

No obvious dedicated counterpart

`AttrsUtils.php`, `TxtLib2.php`, the full PHP `WikiParse` class structure, `Logger.php`, `Csrf.php`, `Index.php`, `Run.php`, `bootstrap.php`, `index.php`, and `work.php` do not all have obvious one-to-one Python counterparts.

Not established

Test parity, output equivalence, edge-case coverage, deployment parity, performance, and production readiness cannot be determined from the directory trees.

### Recommended completion ledger

The following table can be used as a working migration checklist. Its statuses describe the evidence available now, not an assertion about code quality.

| Work item                     | Initial status       | Completion criterion                                             |
| ----------------------------- | -------------------- | ---------------------------------------------------------------- |
| General reference fixers      | Counterparts present | All PHP rules and edge cases reproduced                          |
| Duplicate-reference removal   | Counterpart present  | Equivalent reference identity and output                         |
| Missing-reference fixer       | Counterpart present  | Equivalent insertion and exclusion rules                         |
| Citation expansion            | Counterpart present  | Equivalent named, unnamed, and nested reference handling         |
| Language-specific bots        | Counterparts present | Per-language regression tests pass                               |
| Infobox expansion             | Uncertain            | Both PHP infobox implementations accounted for                   |
| Wiki markup parser            | Uncertain            | Every required PHP parser responsibility mapped                  |
| Attribute/text utilities      | Uncertain            | All required helper methods accounted for                        |
| Category and citation parsing | Uncertain            | Identical behavior for supported inputs                          |
| Processing order              | Unverified           | Equivalent pipeline and configuration behavior                   |
| Logging and error handling    | Unverified           | Operational failures are visible and handled appropriately       |
| Web entry points and security | Scope-dependent      | Required interface and security behavior preserved               |
| Automated regression suite    | Unverified           | Python passes a PHP-derived test corpus                          |
| Production readiness          | Unverified           | Functional, operational, and deployment acceptance criteria pass |

Important: There is insufficient evidence to assign an honest numerical completion percentage. Counting files would be misleading: one PHP parser class may represent more functionality than several small Python modules, and a single Python module may legitimately replace multiple PHP classes.

## 6. Behavioral differences that could affect output

Even where both implementations perform the same named task, differences in language semantics, parser libraries, and transformation strategy can cause divergent results.

### 6.1 PHP and Python string handling

Potential differences include:

- Unicode normalization and case handling.
- String indexing and character boundaries.
- Regular-expression syntax and replacement semantics.
- Greedy versus non-greedy matching.
- Treatment of newlines and carriage returns.
- Empty strings, null values, and missing parameters.
- Differences in truthiness and type conversion.

For example, a PHP expression that treats an empty string and a missing value similarly may behave differently when translated into Python if the Python code distinguishes `None`, `""`, and absent dictionary keys.

Required test: feed identical text into the equivalent PHP and Python methods and compare exact output, including whitespace and punctuation.

### 6.2 Regex parsing versus structured parsing

If PHP uses custom regular expressions while Python relies on a wikitext parsing library, the two implementations may recognize different markup boundaries.

A library-based parser may offer better nesting support but normalize or serialize markup differently. Conversely, a regex-based port may preserve formatting in simple cases but fail on nested constructs.

Test at least:

- Nested templates.
- Templates inside `<ref>` tags.
- References inside templates.
- Repeated parameter names.
- Comments containing apparent tags.
- `<nowiki>` and other literal-content regions.
- Multiline templates and tags.
- Malformed or incomplete markup.

The objective is not necessarily byte-for-byte preservation of every irrelevant formatting choice; it is preservation of the original transformation contract and avoidance of unintended edits.

### 6.3 Reference identity and duplicate detection

Reference processing is particularly high risk because apparently similar references are not always equivalent.

Check the handling of:

- Named versus unnamed references.
- Repeated references using the same name.
- References with different bodies but the same name.
- Attribute order and quotation style.
- Whitespace inside attributes.
- Self-closing references.
- Reuse of named references across a page.
- References with templates in their bodies.
- Duplicate definitions and conflicting definitions.

The Python implementation must not merge references merely because their normalized text looks similar if the PHP implementation distinguishes them.

### 6.4 Execution order and idempotency

A fixer can be correct in isolation but produce incorrect results in combination with other fixers.

Two essential properties should be measured:

1. Parity: PHP and Python produce equivalent results from the same input and configuration.
2. Idempotency: running the same pipeline twice does not introduce additional unintended changes.

For a transformation \\(F\\), idempotency means:

\\[ F(F(x)) = F(x) \\]

This property is not appropriate for every possible operation, but it is a valuable default expectation for cleanup and normalization bots.

### 6.5 Error handling and external dependencies

Inspect how each implementation handles invalid input, missing configuration, unsupported languages, parser failures, and external service errors.

Differences in exceptions, return values, retries, or logging may cause Python to skip a transformation that PHP performs, or to terminate a page-processing run that PHP would allow to continue.

## 7. PHP tests and validation checks not visibly represented in Python

This section addresses a critical distinction: the supplied trees show source modules, not the contents of test suites.

Neither tree includes an obvious `tests/`, `test/`, or dedicated test-fixture directory. That does not establish that either repository has no tests; tests could be embedded in source files, stored elsewhere, run through CI, or documented in the README files.

Consequently, it is not possible to name a specific PHP test that is definitively absent from Python without inspecting the source and repository metadata.

There are, however, several categories of checks that should be investigated in PHP and then explicitly ported or replaced with equivalent Python tests.

### 7.1 PHP checks to search for

| Area                    | PHP files to inspect                                                                                        | What to look for                                                      |
| ----------------------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Reference parsing       | `Parse/Citations.php`, `Parse/CitationsReg.php`, `WikiParse/ParserCitations.php`                            | Assertions, sample inputs, malformed-markup checks, parser validation |
| Template parsing        | `WikiParse/ParserTemplate.php`, `ParserTemplates.php`, `DataModel/Template.php`, `DataModel/Parameters.php` | Nested-template cases, parameter-boundary checks, validation methods  |
| Tags and attributes     | `WikiParse/ParserTags.php`, `DataModel/Tag.php`, `DataModel/Attribute.php`, `Bots/AttrsUtils.php`           | Attribute validation, quote handling, self-closing tags               |
| Duplicate references    | `Bots/RemoveDuplicateRefs.php`                                                                              | Duplicate detection rules, conflicting-name checks, safety guards     |
| Missing references      | `HelpsBots/MissingRefs.php`                                                                                 | Insertion conditions, exclusions, duplicate-prevention checks         |
| Language-specific rules | `LangBots/`                                                                                                 | Assertions, embedded fixtures, special-case checks                    |
| Infobox handling        | `Infoboxes/Infobox.php`, `Infobox2.php`                                                                     | Parameter validation, unsupported-template behavior                   |
| Pipeline execution      | `Run.php`, `Index.php`                                                                                      | Error checks, return values, configuration validation                 |
| Security and requests   | `Csrf.php`, `work.php`, `index.php`                                                                         | Request validation, CSRF checks, invalid-input rejection              |
| Diagnostics             | `Logger.php`                                                                                                | Error recording, warnings, processing-failure reporting               |

This is a search plan, not a claim that these files contain automated tests.

### 7.2 Test parity matrix

The following matrix identifies the tests that the Python replacement should have, regardless of whether they are currently present in PHP.

| Test category                      | PHP test status | Python test status | Migration action                                         |
| ---------------------------------- | --------------- | ------------------ | -------------------------------------------------------- |
| Unit tests for each fixer          | Not established | Not established    | Inspect both repositories and build a complete inventory |
| Parser edge-case tests             | Not established | Not established    | Compare parser test cases and add missing fixtures       |
| Duplicate-reference tests          | Not established | Not established    | Add named, unnamed, and conflicting-definition cases     |
| Missing-reference tests            | Not established | Not established    | Add insertion and exclusion cases                        |
| Language-specific regression tests | Not established | Not established    | Build separate suites for each supported language        |
| Infobox regression tests           | Not established | Not established    | Cover all original infobox behaviors                     |
| PHP-to-Python output comparison    | Not established | Not established    | Implement differential testing                           |
| Idempotency tests                  | Not established | Not established    | Run eligible fixers twice and compare results            |
| Malformed-input tests              | Not established | Not established    | Verify safe handling of incomplete markup                |
| Integration tests                  | Not established | Not established    | Exercise the full pipeline in production order           |
| Performance tests                  | Not established | Not established    | Benchmark representative page sizes                      |
| Web/security tests                 | Not established | Not established    | Port or replace them if web functionality is in scope    |

### 7.3 The most important missing deliverable: a differential test suite

Rather than trying to infer equivalence from file names, create a shared corpus of representative wikitext.

For every test input:

1. Run the original PHP implementation with a known configuration.
2. Run the Python implementation with the equivalent configuration.
3. Capture the output from each implementation.
4. Compare the results.
5. Record every mismatch.
6. Classify the mismatch as a bug, intentional change, or formatting-only difference.
7. Add a regression test for every resolved discrepancy.

A conceptual test case could look like this:

```
{
  "name": "duplicate_named_reference",
  "language": "en",
  "input": "Example wikitext containing repeated named references",
  "expected_output": "Output produced by the approved PHP behavior"
}
```

The expected output should be captured from the actual PHP implementation, not invented manually.

For comparison, normalize output only where normalization is explicitly allowed. Unrestricted whitespace normalization can conceal real regressions in wikitext.

### 7.4 Prioritize tests by risk

The first differential tests should cover:

1. Duplicate references and conflicting named references.
2. Missing-reference insertion.
3. Reference expansion and movement.
4. Nested templates and citation parsing.
5. Attribute parsing and self-closing tags.
6. Infobox parameter transformations.
7. Language-specific date and month conversions.
8. Punctuation movement around citations.
9. Full-pipeline execution order.
10. Malformed markup and failure handling.

These areas combine high structural complexity with a meaningful risk of unintended content changes.

## 8. Recommended migration plan

The migration should proceed in stages, with each stage producing verifiable evidence of equivalence.

Phase 1 — Inventory the PHP behavior

First priority

Extract the public methods, transformation rules, configuration options, and callers from every PHP module. Identify embedded examples, assertions, test scripts, and special cases. Produce a PHP-to-Python function mapping rather than relying on file names.

Phase 2 — Resolve missing and consolidated modules

Investigate `AttrsUtils.php`, `TxtLib2.php`, both PHP infobox classes, and the `WikiParse` subsystem. Determine which responsibilities were moved, delegated to a library, intentionally dropped, or not yet implemented.

Phase 3 — Establish differential testing

Create a shared fixture corpus and run equivalent PHP and Python transformations. Test individual fixers before testing their interactions in the complete pipeline.

Phase 4 — Verify pipeline parity

Compare enabled fixers, execution order, language selection, configuration defaults, return values, and error handling. Confirm that running the Python pipeline twice does not create unintended additional edits.

Phase 5 — Validate production readiness

Benchmark representative pages, review logs and failure recovery, verify deployment and interface requirements, and run the Python implementation in parallel with PHP before switching over.

### Suggested acceptance criteria

Before replacing PHP in production, require the following:

- Every in-scope PHP feature has an explicit Python counterpart or a documented decision that it is no longer required.
- Every relevant PHP transformation rule has a Python implementation or a documented, approved behavior change.
- All critical regression fixtures pass.
- No unexplained differences remain in high-risk reference, template, and infobox transformations.
- Supported language behavior is covered by language-specific tests.
- The full pipeline has been tested, not just individual modules.
- Failures are observable and do not silently corrupt or partially modify page content.
- Required application, logging, and security functionality is preserved or has an approved replacement.
- Any remaining gaps are documented and accepted before deployment.

A practical release gate is to require zero unexplained differences in the agreed regression corpus, with all intentional differences explicitly reviewed and approved.

## 9. Additional audit checklist

Use this checklist to track progress as the source code is inspected.

## Migration tracking

0 / 21 completed

### General fixers

Compare ExpendRefs and expend_refs.py

Compare RemoveDuplicateRefs and remove_duplicate_refs.py

Compare MissingRefs and fix_missing_refs.py

Compare mini fixes, redirects, months, and punctuation movement

Account for AttrsUtils.php and TxtLib2.php

### Parsing and data models

Map every WikiParse parser to Python code or a documented dependency

Compare template and parameter parsing

Compare tags, attributes, internal links, and external links

Compare citation and category parsing

Check malformed and nested wikitext

### Language and infobox support

Compare every language bot and its special cases

Verify Spanish data, helpers, sections, and references

Verify Bulgarian, Polish, Portuguese, Swahili, and Armenian behavior

Reconcile Infobox.php and Infobox2.php with Python

Compare localized dates, aliases, and template parameters

### Runtime and testing

Compare the PHP and Python processing pipelines

Verify settings, mapping, defaults, and execution order

Inspect embedded tests, CI, assertions, and fixtures

Build a PHP-to-Python differential test suite

Verify idempotency, logging, performance, and failure handling

Decide whether PHP web and security features are in scope

Copy checklistReset

## 10. Final conclusions

The Python repository appears to have been designed as a broad replacement for the PHP project, not merely as a port of its reference-handling code. Its structure covers general fixes, reference processing, language bots, infoboxes, and citation/category functionality.

Nevertheless, the available evidence supports structural coverage, not verified functional completion.

The most important outstanding questions are:

1. Parser parity: Has the Python implementation preserved the behavior of the PHP `WikiParse` subsystem, including templates, tags, attributes, links, and nested markup?
2. Unmapped utilities: Have the responsibilities of `AttrsUtils.php` and `TxtLib2.php` been incorporated elsewhere?
3. Infobox parity: Do the Python modules reproduce both PHP infobox implementations?
4. Pipeline parity: Do the Python core and wrapper execute the same transformations in the same order and under the same conditions?
5. Test parity: Which PHP assertions, test cases, embedded fixtures, and validation checks exist, and which are missing from Python?
6. Application parity: Does the replacement need to reproduce the PHP web interface, security controls, and operational functionality, or only the processing engine?

Recommended next step: perform a source-level audit of both repositories and construct a function-by-function mapping accompanied by a differential regression suite. This will establish what is genuinely complete, what remains to be implemented, and which differences are intentional.

Until that audit is complete, the Python project should be described as having broad structural coverage with unverified functional parity—not as a confirmed complete replacement for PHP.

# Scope Clarification: Web Application vs. Processing Engine

The PHP repository includes web-facing components for handling HTTP requests and application execution. These components are intentionally outside the scope of the Python migration.

The Python project is intended to replace the underlying processing and transformation logic, not the PHP web application. The existing PHP application is expected to retain responsibility for web requests and related application-level functionality.

Therefore, the absence of Python equivalents for index.php, work.php, bootstrap.php, Csrf.php, and other web-specific components must not be classified as an implementation gap.

The migration audit must focus exclusively on functional parity between the PHP and Python processing engines, including:

- Reference processing and transformation rules.
- Wikitext parsing and data models.
- General-purpose text fixes.
- Infobox processing.
- Language-specific bots.
- Category and citation parsing.
- Configuration and processing order relevant to the transformation engine.
- Error handling within the processing logic.
- Automated tests, regression coverage, and output equivalence.
  Acceptance criterion: The Python implementation is considered a successful replacement when it reproduces the required PHP processing behavior for all in-scope features. Web request handling, HTTP interfaces, CSRF protection, and other web application responsibilities are explicitly excluded from this assessment.
