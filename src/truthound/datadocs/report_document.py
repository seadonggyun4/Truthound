"""Research report document model helpers for Data Docs.

This module keeps the public/research report architecture separate from the
HTML builder orchestration. It is intentionally an interpretation layer: it
does not change profile, validation, or quality-score calculations.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import truthound
from truthound.datadocs.base import ReportSpec, SectionSpec, SectionType

Labeler = Callable[..., str]


@dataclass(frozen=True)
class AlertThresholds:
    """Shared thresholds for report alerts and methodology notes."""

    high_missing_warning_threshold: float = 0.5
    high_missing_error_threshold: float = 0.8
    low_uniqueness_threshold: float = 0.01
    low_uniqueness_min_rows: int = 100
    duplicate_warning_threshold: float = 0.1


ALERT_THRESHOLDS = AlertThresholds()


@dataclass(frozen=True)
class MethodologyThresholdRow:
    """One report methodology threshold row."""

    criterion: str
    threshold: str
    interpretation: str


@dataclass(frozen=True)
class QualityDimensionDefinition:
    """Definition for a report-level data quality dimension."""

    dimension_key: str
    dimension_default: str
    evidence_key: str
    evidence_default: str
    status_key: str
    status_default: str
    note_key: str
    note_default: str
    limitation_key: str
    limitation_default: str


QUALITY_DIMENSION_DEFINITIONS: tuple[QualityDimensionDefinition, ...] = (
    QualityDimensionDefinition(
        "quality.dimension.completeness",
        "Completeness",
        "quality.dimension.completeness.metric",
        "Missing value ratio",
        "quality.status.measured",
        "Measured",
        "quality.dimension.completeness.note",
        "Estimated from null ratios across profiled columns.",
        "quality.dimension.completeness.limitation",
        "Completeness describes observed null coverage; it does not prove semantic correctness.",
    ),
    QualityDimensionDefinition(
        "quality.dimension.uniqueness",
        "Uniqueness",
        "quality.dimension.uniqueness.metric",
        "Distinct and unique value ratios",
        "quality.status.measured",
        "Measured",
        "quality.dimension.uniqueness.note",
        "Estimated from distinct counts and unique ratios.",
        "quality.dimension.uniqueness.limitation",
        "Uniqueness can indicate duplicate risk but does not determine whether repeated values are valid.",
    ),
    QualityDimensionDefinition(
        "quality.dimension.validity",
        "Validity",
        "quality.dimension.validity.metric",
        "Detected pattern and inferred type signals",
        "quality.status.partial",
        "Partially measured",
        "quality.dimension.validity.note",
        "Requires explicit business rules for complete validation.",
        "quality.dimension.validity.limitation",
        "Pattern and type signals are evidence, not a substitute for complete domain validation rules.",
    ),
    QualityDimensionDefinition(
        "quality.dimension.accuracy",
        "Accuracy",
        "quality.dimension.accuracy.metric",
        "Domain truth comparison",
        "quality.status.not_measured",
        "Input required",
        "quality.dimension.accuracy.note",
        "Cannot be proven from a profile alone without reference data.",
        "quality.dimension.accuracy.limitation",
        "Accuracy requires authoritative reference data or domain review outside this profile report.",
    ),
    QualityDimensionDefinition(
        "quality.dimension.timeliness",
        "Timeliness",
        "quality.dimension.timeliness.metric",
        "Freshness and update SLA",
        "quality.status.not_measured",
        "Input required",
        "quality.dimension.timeliness.note",
        "Requires ingestion timestamps or freshness policy.",
        "quality.dimension.timeliness.limitation",
        "Timeliness requires source freshness metadata or an update policy not inferred from values alone.",
    ),
)


@dataclass(frozen=True)
class TocEntry:
    """One table-of-contents row."""

    target_id: str
    title: str


@dataclass(frozen=True)
class ChapterGroup:
    """A numbered report chapter and its existing rendered sections."""

    number: int
    title: str
    sections: list[SectionSpec]
    lead: str = ""


@dataclass(frozen=True)
class QualityDimensionRow:
    """One row in the quality framework interpretation table."""

    dimension: str
    evidence: str
    status: str
    note: str


@dataclass(frozen=True)
class SummaryItem:
    """One executive summary item."""

    label: str
    body: str


@dataclass(frozen=True)
class ReportObject:
    """Registered report object that may be captioned or referenced."""

    object_type: str
    identifier: str
    title: str
    label: str
    anchor: str


class ReportObjectRegistry:
    """Track report objects so narrative references point to real objects."""

    def __init__(self) -> None:
        self._objects: dict[tuple[str, str], ReportObject] = {}

    def register(
        self,
        object_type: str,
        identifier: int | str,
        title: str,
        label: str,
        anchor: str | None = None,
    ) -> ReportObject:
        key = (object_type, str(identifier))
        obj = ReportObject(
            object_type=object_type,
            identifier=str(identifier),
            title=title,
            label=label,
            anchor=anchor or f"{object_type}-{identifier}",
        )
        existing = self._objects.get(key)
        if existing and existing != obj:
            raise ValueError(f"Conflicting report object registration: {object_type} {identifier}")
        self._objects[key] = obj
        return obj

    def get(self, object_type: str, identifier: int | str) -> ReportObject:
        key = (object_type, str(identifier))
        try:
            return self._objects[key]
        except KeyError as error:
            raise KeyError(f"Report object is not registered: {object_type} {identifier}") from error

    def reference(self, object_type: str, identifier: int | str) -> str:
        return self.get(object_type, identifier).label

    def objects(self) -> tuple[ReportObject, ...]:
        return tuple(self._objects.values())


class CaptionRegistry:
    """Stable caption/chapter numbering for report objects."""

    def __init__(
        self,
        label: Labeler,
        *,
        language: str,
        registry: ReportObjectRegistry | None = None,
    ) -> None:
        self._label = label
        self._language = language
        self._registry = registry or ReportObjectRegistry()

    @property
    def is_korean(self) -> bool:
        return self._language.startswith("ko")

    def chapter(self, number: int, key: str, default: str) -> str:
        title = self._label(key, default)
        if self.is_korean:
            label = f"제{number}장 {title}"
        else:
            label = f"Chapter {number}. {title}"
        return self._registry.register("chapter", number, title, label, f"chapter-{number}").label

    def appendix(self, letter: str, key: str, default: str) -> str:
        title = self._label(key, default)
        if self.is_korean:
            label = f"부록 {letter}. {title}"
        else:
            label = f"Appendix {letter}. {title}"
        return self._registry.register("appendix", letter, title, label, f"appendix-{letter.lower()}").label

    def table(self, number: int, title: str) -> str:
        label = self._label(
            "report.table_caption",
            "Table {number}. {title}",
            number=number,
            title=title,
        )
        return self._registry.register("table", number, title, label, f"table-{number}").label

    def figure(self, number: int, title: str) -> str:
        label = self._label(
            "report.figure_caption",
            "Figure {number}. {title}",
            number=number,
            title=title,
        )
        return self._registry.register("figure", number, title, label, f"figure-{number}").label

    def reference(self, object_type: str, identifier: int | str) -> str:
        return self._registry.reference(object_type, identifier)


class ResearchReportDocument:
    """Build report-level structure, interpretation, and appendix HTML."""

    def __init__(
        self,
        label: Labeler,
        *,
        language: str,
        theme_name: str,
        framework_version: str | None = None,
    ) -> None:
        self._label = label
        self.language = language
        self.theme_name = theme_name
        self.framework_version = framework_version or truthound.__version__
        self.object_registry = ReportObjectRegistry()
        self.captions = CaptionRegistry(label, language=language, registry=self.object_registry)

    def label(self, key: str, default: str, **params: Any) -> str:
        """Return a localized label through the builder-provided catalog."""
        return self._label(key, default, **params)

    def chapter_groups(self, spec: ReportSpec) -> list[ChapterGroup]:
        """Group existing sections into public/research report chapters."""
        sections_by_type = {section.section_type: section for section in spec.sections}
        groups = [
            (
                1,
                "chapter.analysis_overview",
                "Analysis Overview",
                (SectionType.OVERVIEW,),
            ),
            (
                2,
                "chapter.quality_results",
                "Data Quality Diagnostic Results",
                (SectionType.QUALITY,),
            ),
            (
                3,
                "chapter.column_diagnostics",
                "Column-Level Diagnostics",
                (SectionType.COLUMNS,),
            ),
            (
                4,
                "chapter.risk_factors",
                "Detected Patterns and Risk Factors",
                (
                    SectionType.PATTERNS,
                    SectionType.DISTRIBUTION,
                    SectionType.CORRELATIONS,
                    SectionType.ALERTS,
                ),
            ),
            (
                5,
                "chapter.recommendations",
                "Recommendations",
                (SectionType.RECOMMENDATIONS,),
            ),
        ]
        chapter_groups: list[ChapterGroup] = []
        for number, key, default, section_types in groups:
            sections = [sections_by_type[t] for t in section_types if t in sections_by_type]
            if sections:
                chapter_groups.append(
                    ChapterGroup(
                        number,
                        self.captions.chapter(number, key, default),
                        sections,
                        self.chapter_lead(number),
                    )
                )
        return chapter_groups

    def chapter_lead(self, number: int) -> str:
        """Return localized chapter lead text with stable report-object references."""
        if number == 1:
            return self._label(
                "chapter.analysis_overview.lead",
                "This chapter summarizes the analyzed data scale and core profile metrics. Column-level structure is summarized in {column_table}, and the observed data type mix is shown in {type_figure}.",
                column_table=self.captions.table(1, self._label("table.column_summary", "Column Summary")),
                type_figure=self.captions.figure(1, self._label("chart.data_types", "Data Types Distribution")),
            )
        if number == 2:
            return self._label(
                "chapter.quality_results.lead",
                "This chapter interprets profile-driven quality signals. Missing-value patterns are shown in {missing_figure}, and the quality dimension mapping in {quality_table} distinguishes measured evidence from dimensions that require additional input.",
                missing_figure=self.captions.figure(2, self._label("chart.missing_values", "Top Columns by Missing Values")),
                quality_table=self.captions.table(2, self._label("quality.framework.table", "Quality dimension mapping")),
            )
        if number == 3:
            return self._label(
                "chapter.column_diagnostics.lead",
                "This chapter reviews each profiled column while preserving source column names and technical type identifiers. The full audit-oriented column profile is provided in {profile_appendix}.",
                profile_appendix=self.captions.appendix("C", "appendix.full_profile", "Full Column Profile"),
            )
        if number == 4:
            return self._label(
                "chapter.risk_factors.lead",
                "This chapter groups detected patterns, value distribution signals, correlations, and alerts as review evidence. Uniqueness distribution is shown in {uniqueness_figure}; business meaning should be confirmed with domain rules before final decisions.",
                uniqueness_figure=self.captions.figure(3, self._label("chart.uniqueness", "Top Columns by Uniqueness")),
            )
        if number == 5:
            return self._label(
                "chapter.recommendations.lead",
                "This chapter converts profile evidence into priority review actions. Metric definitions and reproducibility metadata are available in {metrics_appendix} and {repro_appendix}.",
                metrics_appendix=self.captions.appendix("A", "appendix.metrics", "Metric Definitions and Formulae"),
                repro_appendix=self.captions.appendix("B", "appendix.reproducibility", "Execution Environment and Reproducibility"),
            )
        return ""

    def toc_entries(self, chapter_groups: list[ChapterGroup]) -> list[TocEntry]:
        """Build the shared HTML/PDF table-of-contents entries."""
        return [
            TocEntry("executive-summary", self._label("report.executive_summary", "Executive Summary")),
            *[
                TocEntry(f"chapter-{chapter.number}", chapter.title)
                for chapter in chapter_groups
            ],
            TocEntry(
                "appendix-a",
                self.captions.appendix("A", "appendix.metrics", "Metric Definitions and Formulae"),
            ),
            TocEntry(
                "appendix-b",
                self.captions.appendix(
                    "B",
                    "appendix.reproducibility",
                    "Execution Environment and Reproducibility",
                ),
            ),
            TocEntry(
                "appendix-c",
                self.captions.appendix("C", "appendix.full_profile", "Full Column Profile"),
            ),
            TocEntry(
                "appendix-d",
                self.captions.appendix(
                    "D",
                    "appendix.quality_coverage",
                    "Quality Dimension Coverage and Limitations",
                ),
            ),
            TocEntry(
                "appendix-e",
                self.captions.appendix(
                    "E",
                    "appendix.methodology",
                    "Diagnostic Criteria and Thresholds",
                ),
            ),
        ]

    def summary_items(self, spec: ReportSpec) -> list[SummaryItem]:
        """Create the executive summary using profile metadata only."""
        metrics = self._overview_metrics(spec.profile_data)
        score = float(metrics.get("quality_score", 100))
        rows = spec.profile_data.get("row_count", 0)
        columns_count = spec.profile_data.get(
            "column_count",
            len(spec.profile_data.get("columns", [])),
        )
        duplicate_ratio = spec.profile_data.get("duplicate_row_ratio", 0)
        high_missing, _low_uniqueness = self.risk_columns(spec)
        primary_risk = (
            self._label(
                "summary.risk.missing",
                "{count} columns require missing-value review.",
                count=len(high_missing),
            )
            if high_missing
            else self._label(
                "summary.risk.none",
                "No high-priority structural risk was detected from the available profile.",
            )
        )
        priority_action = (
            self._label(
                "summary.action.missing",
                "Review collection and imputation rules for high-missing columns.",
            )
            if high_missing
            else self._label(
                "summary.action.validators",
                "Maintain suggested validation rules for monitored columns.",
            )
        )

        return [
            SummaryItem(
                self._label("summary.purpose", "Purpose"),
                self._label(
                    "summary.purpose.text",
                    "Assess the dataset profile and summarize actionable data quality risks.",
                ),
            ),
            SummaryItem(
                self._label("summary.data_overview", "Data Overview"),
                self._label(
                    "summary.data_overview.text",
                    "The analyzed dataset contains {rows:,} rows and {columns} columns.",
                    rows=rows,
                    columns=columns_count,
                ),
            ),
            SummaryItem(
                self._label("summary.key_findings", "Key Findings"),
                self._label(
                    "summary.key_findings.text",
                    "The overall quality score is {score:.1f}% ({grade}); duplicate rows account for {duplicate_ratio:.2%}.",
                    score=score,
                    grade=self.quality_grade(score),
                    duplicate_ratio=duplicate_ratio,
                ),
            ),
            SummaryItem(self._label("summary.risks", "Risks"), primary_risk),
            SummaryItem(self._label("summary.priority_actions", "Priority Actions"), priority_action),
            SummaryItem(
                self._label("summary.limitations", "Limitations"),
                self._label(
                    "summary.limitations.text",
                    "This report is based on the supplied profile metadata and does not prove business accuracy without domain validation.",
                ),
            ),
        ]

    def quality_rows(self) -> list[QualityDimensionRow]:
        """Return quality dimension mapping rows without changing calculations."""
        return [
            QualityDimensionRow(
                self._label(definition.dimension_key, definition.dimension_default),
                self._label(definition.evidence_key, definition.evidence_default),
                self._label(definition.status_key, definition.status_default),
                self._label(definition.note_key, definition.note_default),
            )
            for definition in QUALITY_DIMENSION_DEFINITIONS
        ]

    def quality_coverage_rows(self) -> list[tuple[str, str, str]]:
        """Return quality-dimension coverage rows for the audit appendix."""
        return [
            (
                self._label(definition.dimension_key, definition.dimension_default),
                self._label(definition.status_key, definition.status_default),
                self._label(definition.limitation_key, definition.limitation_default),
            )
            for definition in QUALITY_DIMENSION_DEFINITIONS
        ]

    def methodology_threshold_rows(self) -> list[MethodologyThresholdRow]:
        """Return threshold notes from the same source used by alert generation."""
        thresholds = ALERT_THRESHOLDS
        return [
            MethodologyThresholdRow(
                self._label("methodology.high_missing", "High missing values"),
                f"> {thresholds.high_missing_warning_threshold:.0%}; >= {thresholds.high_missing_error_threshold:.0%}",
                self._label(
                    "methodology.high_missing.note",
                    "Columns above the warning threshold are flagged for missing-value review; columns at or above the error threshold are treated as higher severity.",
                ),
            ),
            MethodologyThresholdRow(
                self._label("methodology.constant_column", "Constant column"),
                self._label("methodology.constant_column.threshold", "1 distinct value"),
                self._label(
                    "methodology.constant_column.note",
                    "Columns marked constant by the supplied profile are flagged as potentially low-information fields.",
                ),
            ),
            MethodologyThresholdRow(
                self._label("methodology.low_uniqueness", "Low uniqueness"),
                self._label(
                    "methodology.low_uniqueness.threshold",
                    "< {uniqueness}; rows > {rows}",
                    uniqueness=f"{thresholds.low_uniqueness_threshold:.0%}",
                    rows=f"{thresholds.low_uniqueness_min_rows:,}",
                ),
                self._label(
                    "methodology.low_uniqueness.note",
                    "Columns below the uniqueness threshold are flagged only when the profiled row count is above the minimum row count.",
                ),
            ),
            MethodologyThresholdRow(
                self._label("methodology.duplicate_rows", "Duplicate rows"),
                f"> {thresholds.duplicate_warning_threshold:.0%}",
                self._label(
                    "methodology.duplicate_rows.note",
                    "Datasets above the duplicate-row threshold are flagged for source loading and deduplication review.",
                ),
            ),
            MethodologyThresholdRow(
                self._label("methodology.quality_score_limit", "Quality score limitation"),
                self._label("methodology.quality_score_limit.threshold", "Profile-derived"),
                self._label(
                    "methodology.quality_score_limit.note",
                    "The quality score summarizes profile metadata and does not prove business accuracy, timeliness, or fitness for use.",
                ),
            ),
        ]

    def risk_columns(self, spec: ReportSpec) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Identify simple profile-driven risk groups for report narrative."""
        columns = spec.profile_data.get("columns", [])
        high_missing = [c for c in columns if c.get("null_ratio", 0) >= 0.05]
        low_uniqueness = [
            c
            for c in columns
            if c.get("unique_ratio", 1) <= 0.01 and spec.profile_data.get("row_count", 0) > 100
        ]
        return high_missing, low_uniqueness

    def quality_grade(self, score: float) -> str:
        """Map a numeric score to a localized qualitative grade."""
        if score >= 90:
            return self._label("quality.excellent", "Excellent")
        if score >= 80:
            return self._label("quality.good", "Good")
        if score >= 60:
            return self._label("quality.fair", "Fair")
        if score >= 40:
            return self._label("quality.poor", "Poor")
        return self._label("quality.critical", "Critical")

    def input_fingerprint(self, spec: ReportSpec) -> str:
        """Return a non-raw-data fingerprint from stable metadata."""
        columns = spec.profile_data.get("columns", [])
        source = spec.metadata.data_source or self._label("common.unknown", "Unknown")
        fingerprint_source = json.dumps(
            {
                "source": source,
                "rows": spec.profile_data.get("row_count", 0),
                "columns": spec.profile_data.get("column_count", len(columns)),
                "theme": self.theme_name,
                "language": spec.config.language,
            },
            sort_keys=True,
            default=str,
        )
        return hashlib.sha256(fingerprint_source.encode("utf-8")).hexdigest()[:16]

    @staticmethod
    def _overview_metrics(profile_data: dict[str, Any]) -> dict[str, Any]:
        columns = profile_data.get("columns", [])
        metrics = {
            "row_count": profile_data.get("row_count", 0),
            "column_count": profile_data.get("column_count", 0),
            "memory_bytes": profile_data.get("estimated_memory_bytes", 0),
        }
        duplicate_count = profile_data.get("duplicate_row_count", 0)
        if duplicate_count > 0:
            metrics["duplicate_rows"] = duplicate_count
            metrics["duplicate_ratio"] = profile_data.get("duplicate_row_ratio", 0)
        null_cells = sum(col.get("null_count", 0) for col in columns)
        if null_cells > 0:
            metrics["null_cells"] = null_cells
        if not columns:
            metrics["quality_score"] = 100.0
            return metrics

        avg_null_ratio = sum(c.get("null_ratio", 0) for c in columns) / len(columns)
        completeness_score = (1 - avg_null_ratio) * 100
        uniqueness_scores = [
            50 if c.get("is_constant", False) else min(c.get("unique_ratio", 0) * 100, 100)
            for c in columns
        ]
        uniqueness_score = sum(uniqueness_scores) / len(uniqueness_scores)
        validity_score = 100
        for col in columns:
            inferred = col.get("inferred_type", "unknown")
            if inferred in ("unknown", "string") and col.get("detected_patterns"):
                validity_score = max(validity_score - 5, 50)
        metrics["quality_score"] = round(
            completeness_score * 0.4 + uniqueness_score * 0.3 + validity_score * 0.3,
            1,
        )
        return metrics
