"""Reusable Data Docs fixtures for report rendering tests."""

from __future__ import annotations

from typing import Any


PUBLIC_REPORT_THEMES = ("light", "dark", "minimal")


def sample_a4_report_profile() -> dict[str, Any]:
    """Return a deterministic profile that exercises report layout surfaces."""
    return {
        "source": "sample-quality-profile.csv",
        "row_count": 2480,
        "column_count": 6,
        "estimated_memory_bytes": 126_976,
        "duplicate_row_count": 12,
        "duplicate_row_ratio": 0.0048,
        "columns": [
            {
                "name": "farm_id",
                "physical_type": "int64",
                "inferred_type": "integer",
                "null_count": 0,
                "null_ratio": 0.0,
                "distinct_count": 2480,
                "unique_ratio": 1.0,
                "detected_patterns": [],
                "suggested_validators": ["not_null", "unique"],
            },
            {
                "name": "region",
                "physical_type": "string",
                "inferred_type": "string",
                "null_count": 18,
                "null_ratio": 0.0073,
                "distinct_count": 17,
                "unique_ratio": 0.0069,
                "detected_patterns": [],
                "suggested_validators": ["not_null", "allowed_values"],
            },
            {
                "name": "reported_revenue",
                "physical_type": "float64",
                "inferred_type": "numeric",
                "null_count": 94,
                "null_ratio": 0.0379,
                "distinct_count": 2210,
                "unique_ratio": 0.8911,
                "detected_patterns": [],
                "suggested_validators": ["range"],
            },
            {
                "name": "contact_email",
                "physical_type": "string",
                "inferred_type": "email",
                "null_count": 126,
                "null_ratio": 0.0508,
                "distinct_count": 2354,
                "unique_ratio": 0.9492,
                "detected_patterns": [
                    {
                        "pattern": "email",
                        "regex": r"^[^@]+@[^@]+\\.[^@]+$",
                        "match_ratio": 0.9492,
                        "sample_matches": ["user@example.test"],
                    }
                ],
                "suggested_validators": ["email"],
            },
            {
                "name": "registered_at",
                "physical_type": "datetime",
                "inferred_type": "datetime",
                "null_count": 7,
                "null_ratio": 0.0028,
                "distinct_count": 180,
                "unique_ratio": 0.0726,
                "detected_patterns": [],
                "suggested_validators": ["not_null"],
            },
            {
                "name": "status",
                "physical_type": "string",
                "inferred_type": "categorical",
                "null_count": 0,
                "null_ratio": 0.0,
                "distinct_count": 4,
                "unique_ratio": 0.0016,
                "detected_patterns": [],
                "suggested_validators": ["allowed_values"],
            },
        ],
        "correlations": [
            {
                "column1": "reported_revenue",
                "column2": "status",
                "correlation": 0.41,
            }
        ],
    }
