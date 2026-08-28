# truthound docs themes

List available report themes.

## Synopsis

```bash
truthound docs themes
```

## Description

The `docs themes` command displays the public Data Docs report themes. Truthound exposes three built-in themes:

| Theme | Description | Best For |
|-------|-------------|----------|
| `light` | Korean public/research A4 report style and default theme | Printed reports, formal reviews, research deliverables |
| `dark` | Dark report style with the same A4 information structure | Screen review in dark environments |
| `minimal` | Low-chroma formal A4 report style | Concise internal reports and monochrome printing |

`default` remains a hidden compatibility alias for `light`. `professional` and `modern` are deprecated aliases for `light` for one release; they are not listed as public themes.

## Examples

### List Themes

```bash
truthound docs themes
```

Output:

```text
Available report themes:

  light          - Korean public/research A4 report style (default)
  dark           - Dark report style with the same A4 structure
  minimal        - Low-chroma formal A4 report style
```

### Generate Reports

```bash
truthound docs generate profile.json -o report.html --theme light
truthound docs generate profile.json -o report-dark.html --theme dark
truthound docs generate profile.json -o report-minimal.html --theme minimal
```

## Exit Codes

| Code | Condition |
|------|-----------|
| 0 | Success |

## Related Commands

- [`docs generate`](generate.md) - Generate HTML or PDF reports with themes
