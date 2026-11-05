# Branch Coverage Report

Executed evidence generated 2026-11-05T08:50:24+05:30. Source base: `bf35375`; the run manifest records any local source changes and SHA-256 hashes of the measured files. This reporting command does not push, start a server or open a browser.

**Branch coverage: 91.94% (114/124 measured branch destinations).**

Coverage.py measures alternative control-flow destinations, not merely the number of if statements. This report separates branch coverage from statement coverage and from Coverage.py combined display percentages. A high percentage does not prove every possible input or security state is correct.

| Production module | Covered destinations | Total destinations | Branch coverage | Sources of missing branches |
|---|---:|---:|---:|---|
| analytics.py | 14 | 14 | 100.00% | None |
| app.py | 51 | 56 | 91.07% | 91, 125, 160, 196, 230 |
| database.py | 2 | 2 | 100.00% | None |
| seed_data.py | 5 | 10 | 50.00% | 31, 34, 36 |
| services.py | 42 | 42 | 100.00% | None |
| ui.py | 0 | 0 | N/A (no branches) | None |

## Uncovered branch destinations

Pairs below are source-line and destination-line numbers from Coverage.py. Negative destinations represent function exits. These are retained explicitly rather than hidden by exclusions.

```json
{
  "app.py": [
    [
      91,
      93
    ],
    [
      125,
      126
    ],
    [
      160,
      161
    ],
    [
      196,
      -1
    ],
    [
      230,
      231
    ]
  ],
  "seed_data.py": [
    [
      31,
      32
    ],
    [
      34,
      35
    ],
    [
      34,
      36
    ],
    [
      36,
      -1
    ],
    [
      36,
      37
    ]
  ]
}
```

Reproduce with `python scripts/run_part3_checks.py`. Evidence: [annotated HTML](evidence/coverage-html/index.html), [raw JSON](evidence/coverage-data.json), [Cobertura XML](evidence/cobertura.xml). Manual visual acceptance, deployment availability and an actual browser load measurement remain separate.
