# Source Analysis

The style system was distilled from three user-supplied reference decks. The original decks and their rendered contact sheets are intentionally excluded from this repository.

## Corpus

| Reference | Slides analyzed | Confidence |
| --- | ---: | --- |
| McKinsey-labeled sample | 3 | Low to medium; use for typography, cover, whitespace, and compact synthesis patterns |
| Bain-labeled template library | 229 | High for analytical layouts, charts, tables, red emphasis, and density |
| BCG-labeled template library | 65 | High for strategy, process, portfolio, maps, timelines, and green emphasis |

## Extraction Method

- Verified source file identity for the PowerPoint references.
- Converted the legacy BCG `.ppt` to a working `.pptx` for analysis.
- Inspected complete rendered contact sheets.
- Counted slides, slide dimensions, font references, type sizes, and explicit colors in the OOXML packages.
- Compared recurring title, chart, table, process, map, and footer patterns.
- Retained reusable design grammar and removed logos, client information, source slide content, and proprietary binaries.

## Limitations

- These are empirical patterns from specific decks, not current official brand manuals.
- Template libraries often contain imported charts and legacy slides, so font counts include exceptions.
- The McKinsey-labeled sample is small and should not be treated as a complete design system.
- Exact firm branding can change; use the rules as informed consulting styles.

## Safe Reuse Boundary

Reusable:

- General layout grammar.
- Font pairings and restrained palette roles.
- Claim-title and proof-first conventions.
- Chart emphasis and table hierarchy.
- Generic slide archetypes.

Excluded:

- Logos and wordmarks.
- Proprietary source slides.
- Client names and data.
- Distinctive copied wording or charts.
- Original template binaries and rendered screenshots.
