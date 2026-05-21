# Rust API guidelines — checklist map

Official index and checklist:

- About / navigation: https://rust-lang.github.io/api-guidelines/
- **Checklist (all C- IDs):** https://rust-lang.github.io/api-guidelines/checklist.html
- External RFC / std links roundup: https://rust-lang.github.io/api-guidelines/external-links.html

## Section index (deep links)

1. Naming — https://rust-lang.github.io/api-guidelines/naming.html  
   (`C-CASE`, `C-CONV`, `C-GETTER`, `C-ITER`, `C-ITER-TY`, `C-FEATURE`, `C-WORD-ORDER`)

2. Interoperability — https://rust-lang.github.io/api-guidelines/interoperability.html  
   (`C-COMMON-TRAITS`, `C-CONV-TRAITS`, `C-COLLECT`, `C-SERDE`, `C-SEND-SYNC`, `C-GOOD-ERR`, `C-NUM-FMT`, `C-RW-VALUE`)

3. Macros — https://rust-lang.github.io/api-guidelines/macros.html  
   (`C-EVOCATIVE`, `C-MACRO-ATTR`, `C-ANYWHERE`, `C-MACRO-VIS`, `C-MACRO-TY`)

4. Documentation — https://rust-lang.github.io/api-guidelines/documentation.html  
   (`C-CRATE-DOC`, `C-EXAMPLE`, `C-QUESTION-MARK`, `C-FAILURE`, `C-LINK`, `C-METADATA`, `C-RELNOTES`, `C-HIDDEN`)

5. Predictability — https://rust-lang.github.io/api-guidelines/predictability.html  
   (`C-SMART-PTR`, `C-CONV-SPECIFIC`, `C-METHOD`, `C-NO-OUT`, `C-OVERLOAD`, `C-DEREF`, `C-CTOR`)

6. Flexibility — https://rust-lang.github.io/api-guidelines/flexibility.html  
   (`C-INTERMEDIATE`, `C-CALLER-CONTROL`, `C-GENERIC`, `C-OBJECT`)

7. Type safety — https://rust-lang.github.io/api-guidelines/type-safety.html  
   (`C-NEWTYPE`, `C-CUSTOM-TYPE`, `C-BITFLAG`, `C-BUILDER`)

8. Dependability — https://rust-lang.github.io/api-guidelines/dependability.html  
   (`C-VALIDATE`, `C-DTOR-FAIL`, `C-DTOR-BLOCK`)

9. Debuggability — https://rust-lang.github.io/api-guidelines/debuggability.html  
   (`C-DEBUG`, `C-DEBUG-NONEMPTY`)

10. Future proofing — https://rust-lang.github.io/api-guidelines/future-proofing.html  
    (`C-SEALED`, `C-STRUCT-PRIVATE`, `C-NEWTYPE-HIDE`, `C-STRUCT-BOUNDS`)

11. Necessities — https://rust-lang.github.io/api-guidelines/necessities.html  
    (`C-STABLE`, `C-PERMISSIVE`)

## Fast review heuristic

Working top-down:

- **Naming + predictability:** Do names and constructors read like idiomatic Rust (std-like)?
- **Interoperability + type safety:** Do new types compose (`From`, `serde` feature gates, iterators, builders)?
- **Docs + debug:** Every public export documented with honest errors/panics/safety where needed?
- **Future-proofing + necessities:** semver story, licensing, leaking generic bounds unnecessarily?
