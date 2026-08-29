# HTML Reports

The Truthound Data Docs module transforms data profile results into self-contained HTML reports.

## Quick Start

```python
from truthound.datadocs import generate_html_report, HTMLReportBuilder

# Simple usage
html = generate_html_report(
    profile=profile_dict,
    title="Data Quality Report",
    theme="light",
    output_path="report.html",
)

# Korean public/research report labels
html = generate_html_report(
    profile=profile_dict,
    title="데이터 품질 분석 보고서",
    subtitle="한국 공공·연구용 A4 보고서",
    theme="light",
    language="ko",
    output_path="report-ko.html",
)

# Generate from file
from truthound.datadocs import generate_report_from_file

html = generate_report_from_file(
    profile_path="profile.json",
    output_path="report.html",
    title="My Report",
    theme="dark",
)
```

## HTMLReportBuilder

Use `HTMLReportBuilder` directly when fine-grained control is required.

### Basic Usage

```python
from truthound.datadocs import HTMLReportBuilder, ReportTheme

builder = HTMLReportBuilder(theme=ReportTheme.LIGHT)
html = builder.build(
    profile=profile_dict,
    title="My Data Report",
    subtitle="Q4 2025 Analysis",
    description="Customer dataset quality analysis",
)
builder.save(html, "report.html")
```

For localized reports, pass `language="ko"` to `HTMLReportBuilder` or
`generate_html_report`. This localizes the built-in table of contents, section
titles, metric labels, table headers, chart titles, footer text, and PDF cover
metadata. Framework-generated alert titles, alert messages, suggestions, and
recommendations are localized as report narrative rather than left as dashboard
phrases.

Truthound preserves source and technical identifiers by default. Column names,
validator ids such as `not_null`, inferred or physical type ids such as
`integer`, pattern ids such as `email`, and source sample values remain unchanged
so that the report can be traced back to the profile and validation model. The
surrounding labels and explanatory sentences are localized.

## Public/Research Report Structure

The A4 Data Docs output is structured as a public-sector and research-style
report rather than a dashboard dump. HTML and PDF share the same information
architecture:

- cover and metadata
- executive summary with purpose, data overview, key findings, risks, priority
  actions, and limitations
- non-table table of contents with leader dots in PDF output
- chapter-style body sections for analysis overview, data quality diagnostic
  results, column-level diagnostics, detected patterns and risk factors, and
  recommendations
- chapter lead paragraphs that connect the interpretation text to numbered
  tables, figures, and appendices
- stable report-object numbering for tables, figures, chapters, and appendices
- quality framework mapping that explains which profile signals support each
  data quality dimension and which dimensions require additional input
- appendices for metric definitions, formulae, execution metadata, and the full
  column profile
- a quality coverage appendix that separates measured dimensions from
  dimensions that require business rules, reference data, or freshness metadata
- a methodology appendix that records the alert thresholds used for high
  missing values, constant columns, low uniqueness, duplicate rows, and quality
  score interpretation limits

The quality framework mapping is an interpretation layer. It preserves the
existing Truthound profile and validation calculations and does not claim that
business accuracy, timeliness, or domain consistency were measured unless the
input profile provides those signals.

Alert thresholds are maintained from the same report policy source used by the
alert generator. That keeps the visible methodology appendix aligned with the
actual warning behavior in generated reports.

For advanced integrations, `ReportDocument` exposes the report architecture
adapter used by the HTML/PDF builders. It provides stable chapter, appendix,
quality-dimension, interpretation-rule, and report-object registry metadata
without changing `generate_html_report`, `HTMLReportBuilder`, or `export_to_pdf`.
Use this layer when an application needs to inspect report structure before
rendering, while keeping profile and validation calculations unchanged.

Generated appendices use reproducibility metadata such as package version,
Python version, platform, selected theme, language, source label, and a metadata
fingerprint. They do not embed raw input data in the fingerprint.
Report titles, subtitles, source labels, captions, and generated report-object
text are escaped before rendering, while explicit `custom_css` and `custom_js`
configuration remains available for trusted report customization.

The report body cross-references generated objects such as `Table 1`,
`Figure 2`, and `Appendix C` so that readers can move from interpretation to
supporting evidence. Repeating a table or figure number in narrative text is
intentional; the canonical object number remains attached to the table or figure
caption. Report object references are registered before rendering so generated
narrative does not point to an object that is absent from the report structure.

The sample bundle contract generates one Korean A4 HTML report for each public
theme: `light`, `dark`, and `minimal`. The sample smoke keeps the report title,
table/figure/appendix numbering, methodology appendix, Korean typography, and
localized alert narrative stable without checking in binary golden images.

### Detailed Configuration with ReportConfig

```python
from truthound.datadocs import (
    HTMLReportBuilder,
    ReportConfig,
    ReportTheme,
    SectionType,
)

config = ReportConfig(
    # Theme
    theme=ReportTheme.DARK,

    # Sections to include (in order)
    sections=[
        SectionType.OVERVIEW,
        SectionType.QUALITY,
        SectionType.COLUMNS,
        SectionType.PATTERNS,
        SectionType.DISTRIBUTION,
        SectionType.CORRELATIONS,
        SectionType.RECOMMENDATIONS,
        SectionType.ALERTS,
    ],

    # Layout options
    include_toc=True,
    include_header=True,
    include_footer=True,
    include_timestamp=True,
    include_download_button=True,
    embed_resources=True,
    minify_html=False,

    # Custom content
    custom_css="",
    custom_js="",
    logo_url=None,
    logo_base64=None,
    footer_text="Generated by Truthound",

    # Localization
    language="en",
    date_format="%Y-%m-%d %H:%M:%S",
    number_format=",.2f",
)

builder = HTMLReportBuilder(config=config)
html = builder.build(profile_dict)
```

## ProfileDataConverter

`ProfileDataConverter` transforms TableProfile data into report-ready structures.

```python
from truthound.datadocs.builder import ProfileDataConverter

converter = ProfileDataConverter(profile_dict)

# Extract overview metrics
metrics = converter.get_overview_metrics()
# {
#     "row_count": 10000,
#     "column_count": 15,
#     "memory_bytes": 1234567,
#     "duplicate_rows": 123,
#     "null_cells": 456,
#     "quality_score": 85.5,
# }

# Column data
columns = converter.get_column_data()

# Generate chart specs
type_chart = converter.get_type_distribution()  # ChartSpec
null_chart = converter.get_null_distribution()  # ChartSpec
unique_chart = converter.get_uniqueness_distribution()  # ChartSpec

# Extract patterns
patterns = converter.get_patterns()

# Extract correlations
correlations = converter.get_correlations()  # list[tuple[str, str, float]]

# Generate alerts
alerts = converter.get_alerts()  # list[AlertSpec]

# Generate recommendations
recommendations = converter.get_recommendations()  # list[str]
```

## Convenience Functions

### generate_html_report

```python
from truthound.datadocs import generate_html_report

html = generate_html_report(
    profile=profile_dict,        # TableProfile dict or object
    title="Data Quality Report", # Report title
    subtitle="",                 # Subtitle
    theme="light",        # Theme name or ReportTheme
    output_path="report.html",   # Save path (optional)
)
```

### generate_report_from_file

```python
from truthound.datadocs import generate_report_from_file

html = generate_report_from_file(
    profile_path="profile.json",  # Profile JSON file path
    output_path="report.html",    # Output path (default: <input>.html)
    title="My Report",
    theme="dark",
)
```

### export_report

```python
from truthound.datadocs import export_report

# HTML export
export_report(profile_dict, "report.html", format="html")

# PDF export (requires WeasyPrint)
export_report(profile_dict, "report.pdf", format="pdf")
```

## Complete Workflow Example

```python
import truthound as th
from truthound.datadocs import generate_html_report

# 1. Load data
df = th.load("data.csv")

# 2. Generate profile
from truthound.profiler import DataProfiler
profiler = DataProfiler()
profile = profiler.profile(df)

# 3. Generate HTML report
html = generate_html_report(
    profile=profile.to_dict(),
    title="Customer Data Quality Report",
    subtitle="Q4 2025 Analysis",
    theme="light",
    output_path="customer_report.html",
)

print(f"Report generated: {len(html):,} bytes")
```

## CLI Usage

```bash
# Basic usage
truthound docs generate profile.json -o report.html

# Custom title and dark theme
truthound docs generate profile.json -o report.html \
    --title "Q4 Data Quality Report" \
    --subtitle "Customer Dataset" \
    --theme dark

# PDF export
truthound docs generate profile.json -o report.pdf --format pdf
```

## Customization

### Custom CSS

```python
config = ReportConfig(
    custom_css="""
    .report-title {
        color: #ff6b6b;
    }
    .metric-card {
        border: 2px solid #4ecdc4;
    }
    """,
)
```

### Custom JavaScript

```python
config = ReportConfig(
    custom_js="""
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Report loaded!');
    });
    """,
)
```

### Adding a Logo

```python
# Add logo via URL
config = ReportConfig(logo_url="https://example.com/logo.png")

# Add logo via Base64 (offline support)
import base64
with open("logo.png", "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode()

config = ReportConfig(logo_base64=f"data:image/png;base64,{logo_b64}")
```

## API Reference

### ReportConfig

```python
@dataclass
class ReportConfig:
    theme: ReportTheme = ReportTheme.LIGHT
    custom_theme: ThemeConfig | None = None
    chart_library: ChartLibrary = ChartLibrary.APEXCHARTS
    sections: list[SectionType] = [
        SectionType.OVERVIEW,
        SectionType.QUALITY,
        SectionType.COLUMNS,
        SectionType.PATTERNS,
        SectionType.DISTRIBUTION,
        SectionType.CORRELATIONS,
        SectionType.RECOMMENDATIONS,
        SectionType.ALERTS,
    ]
    include_toc: bool = True
    include_header: bool = True
    include_footer: bool = True
    include_timestamp: bool = True
    include_download_button: bool = True
    embed_resources: bool = True
    minify_html: bool = False
    custom_css: str = ""
    custom_js: str = ""
    logo_url: str | None = None
    logo_base64: str | None = None
    footer_text: str = "Generated by Truthound"
    language: str = "en"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    number_format: str = ",.2f"
```

### ReportMetadata

```python
@dataclass
class ReportMetadata:
    title: str
    subtitle: str = ""
    description: str = ""
    data_source: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    author: str = ""
    version: str = ""
```

## See Also

- [Themes](themes.md) - Theme customization
- [Charts](charts.md) - Chart rendering
- [Sections](sections.md) - Section configuration
- [PDF Export](pdf-export.md) - PDF export
