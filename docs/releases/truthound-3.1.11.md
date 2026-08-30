# Truthound 3.1.11 Release Notes

## Highlights

Truthound 3.1.11 publishes the Korean A4 Data Docs report engine work under a
fresh package version after the 3.1.10 release slot was already occupied on
PyPI. The release keeps the validation runtime unchanged while making generated
HTML/PDF reports more suitable for public-sector and research-style data quality
reviews.

## Data Docs Reports

- Keeps the public report theme surface limited to `light`, `dark`, and
  `minimal`.
- Preserves `default` as a hidden alias for `light`, with `professional` and
  `modern` retained as deprecated compatibility aliases.
- Adds structured report document rendering for cover metadata, executive
  summary, non-table table of contents, numbered chapters, appendices, tables,
  figures, captions, methodology notes, and quality-dimension interpretation.
- Strengthens Korean report copy so built-in report chrome and labels render in
  Korean while user-provided titles, data source names, and column names remain
  unchanged.

## Validation and Packaging

- Adds release-readiness coverage for theme policy, Korean report structure,
  visual markers, PDF export smoke, sample bundle contracts, and package
  artifact contents.
- Verifies the new report engine modules are included in the built wheel and
  source distribution.
- Keeps `th.check()`, `ValidationRunResult`, profile, drift, anomaly, and data
  quality calculation semantics unchanged.

## Usage

```python
from truthound.datadocs import generate_html_report, export_to_pdf

generate_html_report(profile, title="데이터 품질 분석 보고서", theme="light", language="ko")
export_to_pdf(profile, "report-ko.pdf", title="데이터 품질 분석 보고서", language="ko")
```

Use `theme="dark"` for the same report structure on a dark palette, or
`theme="minimal"` for a monochrome, low-saturation report style.
