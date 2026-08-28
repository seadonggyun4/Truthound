# Truthound 3.1.8 Release Notes

## Highlights

Truthound 3.1.8 upgrades Data Docs reports into Korean public-sector and
research-style A4 documents. HTML and PDF-ready output now share a report
layout system with A4 page sizing, Korean font stacks, compact tables, summary
boxes, captions, and print break controls.

This release also narrows the public built-in theme surface to `light`, `dark`,
and `minimal`. The `light` theme is the default A4 report style, `dark` keeps
the same report structure on a low-luminance palette, and `minimal` provides a
monochrome or low-saturation document style.

## Theme compatibility

The public theme list now exposes only:

- `light`
- `dark`
- `minimal`

`default` remains a hidden compatibility alias for `light`. `professional` and
`modern` are retained for one release as deprecated aliases for `light` and
emit warnings when used. Custom YAML, JSON, and dictionary theme loading is
unchanged.

## A4 report output

The Data Docs renderer now includes a shared A4 report stylesheet for browser
HTML and PDF-ready HTML:

- A4 portrait page shell using millimeter and point units
- Korean-first font stack with `맑은 고딕`, `Malgun Gothic`, `돋움`, and
  `sans-serif`
- navy report headings and table headers
- collapsed report tables with compact cell padding
- reusable summary boxes and figure captions
- `@page`, page-break, table, figure, and summary break controls for print/PDF

The validation runtime, `th.check()` result model, profiler, drift, anomaly,
and data quality calculation semantics are unchanged.

## Visual and PDF smoke coverage

Data Docs now has deterministic visual smoke fixtures for all public themes.
The tests verify stable structural markers instead of binary golden images, so
layout regressions are caught without introducing fragile image snapshots.

When WeasyPrint and its system libraries are available, the PDF smoke test
creates a real PDF and verifies the PDF header, minimum file size, and text
extraction. If Poppler is available, the first page can also be rendered to a
PNG smoke artifact.

CI environments that must enforce non-skipped PDF coverage can set:

```bash
TRUTHOUND_DATADOCS_REQUIRE_PDF_SMOKE=1
TRUTHOUND_DATADOCS_REQUIRE_PDF_RENDER=1
```

## Consumer upgrade gate

Consumers should install the published 3.1.8 wheel, verify
`truthound.__version__`, regenerate representative Data Docs HTML/PDF reports,
and confirm the public theme list contains only `light`, `dark`, and `minimal`.
Source checkouts or unpublished wheels are not consumer certification evidence.
