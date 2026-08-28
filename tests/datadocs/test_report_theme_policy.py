"""Data Docs report theme policy tests."""

from __future__ import annotations

import warnings

from truthound.datadocs import HTMLReportBuilder, get_available_themes
from truthound.datadocs.builder import generate_html_report
from truthound.datadocs.styles import PRINT_CSS, get_complete_stylesheet
from truthound.datadocs.themes import get_theme as get_legacy_theme
from truthound.datadocs.themes.default import get_theme, list_themes


PROFILE = {
    "source": "sample.csv",
    "row_count": 120,
    "column_count": 3,
    "columns": [
        {
            "name": "id",
            "inferred_type": "integer",
            "null_ratio": 0,
            "unique_ratio": 1,
            "distinct_count": 120,
        },
        {
            "name": "region",
            "inferred_type": "string",
            "null_ratio": 0.04,
            "unique_ratio": 0.08,
            "distinct_count": 10,
        },
    ],
}


def test_public_theme_lists_expose_only_supported_report_themes() -> None:
    assert list_themes() == ["light", "dark", "minimal"]
    assert get_available_themes() == ["light", "dark", "minimal"]


def test_default_is_hidden_light_alias() -> None:
    assert get_theme("default").name == "light"
    assert get_legacy_theme("default").name == "light"


def test_deprecated_theme_aliases_warn_and_map_to_light() -> None:
    for name in ("professional", "modern"):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            theme = get_theme(name)

        assert theme.name == "light"
        assert any(item.category is DeprecationWarning for item in caught)

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            legacy = get_legacy_theme(name)

        assert legacy.name == "light"
        assert any(item.category is DeprecationWarning for item in caught)


def test_html_report_contains_a4_korean_report_styles() -> None:
    html = generate_html_report(PROFILE, title="Quality Report", theme="light")

    assert "@page" in html
    assert "size: A4 portrait" in html
    assert "width: 210mm" in html
    assert "Malgun Gothic" in html
    assert "맑은 고딕" in html
    assert "border-collapse: collapse" in html
    assert ".summary-box" in html
    assert ".report-caption" in html
    assert "page-break-inside: avoid" in html


def test_builder_accepts_legacy_theme_inputs_without_changing_public_list() -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        html = HTMLReportBuilder(theme="professional").build(PROFILE)

    assert "<!DOCTYPE html>" in html
    assert "width: 210mm" in html
    assert any(item.category is DeprecationWarning for item in caught)
    assert get_available_themes() == ["light", "dark", "minimal"]


def test_print_css_contains_pdf_break_controls() -> None:
    stylesheet = get_complete_stylesheet("", include_apexcharts=False)

    assert "@page" in PRINT_CSS
    assert "size: A4 portrait" in stylesheet
    assert "page-break-inside: avoid" in stylesheet
    assert "break-inside: avoid" in stylesheet
    assert "display: table-header-group" in stylesheet
