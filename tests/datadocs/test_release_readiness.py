"""Release-readiness checks for the Data Docs A4 report surface."""

from __future__ import annotations

import importlib
import tomllib
import warnings
from pathlib import Path

from truthound.datadocs import HTMLReportBuilder, ReportDocument, ReportTheme, get_available_themes
from truthound.datadocs.builder import generate_html_report
from truthound.datadocs.report_document import InterpretationRule, ResearchReportDocument
from truthound.datadocs.report_renderers import ReportDocumentRenderer
from truthound.datadocs.themes.default import get_theme, list_themes

from .fixtures import PUBLIC_REPORT_THEMES, sample_a4_report_profile


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_report_engine_modules_are_importable_from_datadocs_package() -> None:
    document_module = importlib.import_module("truthound.datadocs.report_document")
    renderer_module = importlib.import_module("truthound.datadocs.report_renderers")

    assert ReportDocument is ResearchReportDocument
    assert document_module.ResearchReportDocument is ResearchReportDocument
    assert document_module.ReportDocument is ReportDocument
    assert document_module.InterpretationRule is InterpretationRule
    assert renderer_module.ReportDocumentRenderer is ReportDocumentRenderer


def test_pyproject_package_discovery_includes_datadocs_report_engine_modules() -> None:
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"] == ["src/truthound"]
    assert (REPO_ROOT / "src" / "truthound" / "datadocs" / "report_document.py").is_file()
    assert (REPO_ROOT / "src" / "truthound" / "datadocs" / "report_renderers.py").is_file()


def test_release_theme_surface_keeps_public_list_and_alias_contract() -> None:
    assert get_available_themes() == list(PUBLIC_REPORT_THEMES)
    assert list_themes() == list(PUBLIC_REPORT_THEMES)

    assert get_theme("default").name == "light"
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        professional = get_theme("professional")
        modern = get_theme("modern")

    assert professional.name == "light"
    assert modern.name == "light"
    assert len(caught) == 2
    assert all("deprecated" in str(warning.message) for warning in caught)


def test_release_html_surface_uses_same_report_structure_for_public_themes() -> None:
    for theme in PUBLIC_REPORT_THEMES:
        html = generate_html_report(
            sample_a4_report_profile(),
            title="Truthound 데이터 품질 연구 보고서",
            subtitle=f"{theme} release-readiness fixture",
            theme=theme,
            language="ko",
        )
        assert "요약문" in html
        assert "제1장 분석 개요" in html
        assert "부록 E. 진단 기준 및 임계값" in html
        assert "[표 6] 진단 기준 및 임계값" in html
        assert "appendix.methodology" not in html
        assert "Low Cardinality" not in html


def test_release_pdf_ready_builder_keeps_svg_and_appendix_structure() -> None:
    html = HTMLReportBuilder(theme=ReportTheme.LIGHT, language="ko", _use_svg=True).build_for_pdf(
        sample_a4_report_profile(),
        title="Truthound 데이터 품질 연구 보고서",
        subtitle="release-readiness PDF-ready fixture",
    )

    assert "<svg" in html
    assert "apexcharts" not in html.lower()
    assert 'class="report-toc-professional"' in html
    assert "부록 E. 진단 기준 및 임계값" in html
    assert "target-counter(attr(data-target), page)" in html


def test_release_docs_surface_mentions_report_policy_without_private_engine_paths() -> None:
    docs = {
        "README.md": (REPO_ROOT / "README.md").read_text(encoding="utf-8"),
        "README.en.md": (REPO_ROOT / "README.en.md").read_text(encoding="utf-8"),
        "docs/guides/datadocs/html-reports.md": (
            REPO_ROOT / "docs" / "guides" / "datadocs" / "html-reports.md"
        ).read_text(encoding="utf-8"),
        "docs/locales/ko/guides/datadocs/html-reports.md": (
            REPO_ROOT / "docs" / "locales" / "ko" / "guides" / "datadocs" / "html-reports.md"
        ).read_text(encoding="utf-8"),
        "docs/guides/datadocs/pdf-export.md": (
            REPO_ROOT / "docs" / "guides" / "datadocs" / "pdf-export.md"
        ).read_text(encoding="utf-8"),
        "docs/locales/ko/guides/datadocs/pdf-export.md": (
            REPO_ROOT / "docs" / "locales" / "ko" / "guides" / "datadocs" / "pdf-export.md"
        ).read_text(encoding="utf-8"),
    }

    for text in docs.values():
        assert "Change Capsule" not in text
        assert "AGENTS.md" not in text

    assert "public themes are" in docs["README.en.md"]
    assert "`light`" in docs["README.en.md"]
    assert "`dark`" in docs["README.en.md"]
    assert "`minimal`" in docs["README.en.md"]
    assert "공개 테마는" in docs["README.md"]
    assert "`light`" in docs["README.md"]
    assert "`dark`" in docs["README.md"]
    assert "`minimal`" in docs["README.md"]
    assert "methodology appendix" in docs["docs/guides/datadocs/html-reports.md"]
    assert "ReportDocument" in docs["docs/guides/datadocs/html-reports.md"]
    assert "interpretation-rule" in docs["docs/guides/datadocs/html-reports.md"]
    assert "진단 기준 및 임계값 부록" in docs["docs/locales/ko/guides/datadocs/html-reports.md"]
    assert "ReportDocument" in docs["docs/locales/ko/guides/datadocs/html-reports.md"]
    assert "해석 rule" in docs["docs/locales/ko/guides/datadocs/html-reports.md"]
    assert "The PDF smoke also exports each public report theme" in docs[
        "docs/guides/datadocs/pdf-export.md"
    ]
    assert "PDF smoke가 공개 보고서 테마" in docs[
        "docs/locales/ko/guides/datadocs/pdf-export.md"
    ]
