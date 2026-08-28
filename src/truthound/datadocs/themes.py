"""Pre-defined themes for Data Docs reports."""

from __future__ import annotations

import warnings

from truthound.datadocs.base import (
    ReportTheme,
    ThemeColors,
    ThemeTypography,
    ThemeSpacing,
    ThemeConfig,
)


# =============================================================================
# Light Theme - Korean public/research report standard
# =============================================================================

LIGHT_THEME = ThemeConfig(
    name="light",
    colors=ThemeColors(
        background="#e9ecef",
        surface="#ffffff",
        text_primary="#1a1a1a",
        text_secondary="#555555",
        primary="#17365D",
        secondary="#1F4E79",
        accent="#4a7a2f",
        success="#2f6f3e",
        warning="#a15c00",
        error="#b42318",
        info="#1F4E79",
        border="#b9c2d0",
        shadow="rgba(0, 0, 0, 0.14)",
        chart_palette=(
            "#17365D", "#1F4E79", "#5B8DB8", "#4a7a2f",
            "#7aa05a", "#8fa0b6", "#a15c00", "#b42318",
            "#555555", "#2f5218"
        ),
    ),
    typography=ThemeTypography(
        font_family="'Malgun Gothic', '맑은 고딕', 'Dotum', '돋움', sans-serif",
        font_family_mono="'D2Coding', 'Cascadia Code', 'Consolas', monospace",
        font_size_base="10.8pt",
        font_size_sm="9.8pt",
        font_size_lg="11.5pt",
        font_size_xl="13pt",
        font_size_2xl="16pt",
        font_size_3xl="19pt",
        line_height_normal=1.7,
    ),
    spacing=ThemeSpacing(
        border_radius_sm="0",
        border_radius_md="2px",
        border_radius_lg="2px",
        border_radius_xl="2px",
        shadow_md="0 1px 10px rgba(0, 0, 0, 0.14)",
    ),
)


# =============================================================================
# Dark Theme - Modern and Elegant
# =============================================================================

DARK_THEME = ThemeConfig(
    name="dark",
    colors=ThemeColors(
        background="#111827",
        surface="#1f2937",
        text_primary="#f8fafc",
        text_secondary="#cbd5e1",
        primary="#93c5fd",
        secondary="#60a5fa",
        accent="#86efac",
        success="#4ade80",
        warning="#fbbf24",
        error="#f87171",
        info="#38bdf8",
        border="#475569",
        shadow="rgba(0, 0, 0, 0.25)",
        chart_palette=(
            "#93c5fd", "#60a5fa", "#38bdf8", "#86efac",
            "#4ade80", "#cbd5e1", "#fbbf24", "#f87171",
            "#94a3b8", "#bfdbfe"
        ),
    ),
    typography=ThemeTypography(
        font_family="'Malgun Gothic', '맑은 고딕', 'Dotum', '돋움', sans-serif",
        font_family_mono="'D2Coding', 'Cascadia Code', 'Consolas', monospace",
        font_size_base="10.8pt",
        font_size_sm="9.8pt",
        font_size_lg="11.5pt",
        font_size_xl="13pt",
        font_size_2xl="16pt",
        font_size_3xl="19pt",
        line_height_normal=1.7,
    ),
    spacing=ThemeSpacing(
        shadow_md="0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)",
        shadow_lg="0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2)",
    ),
)


# =============================================================================
# Minimal Theme - low-chroma formal report
# =============================================================================

MINIMAL_THEME = ThemeConfig(
    name="minimal",
    colors=ThemeColors(
        background="#ffffff",
        surface="#fafafa",
        text_primary="#171717",
        text_secondary="#737373",
        primary="#404040",
        secondary="#525252",
        accent="#262626",
        success="#525252",
        warning="#737373",
        error="#404040",
        info="#525252",
        border="#cfcfcf",
        shadow="rgba(0, 0, 0, 0.03)",
        chart_palette=(
            "#404040", "#525252", "#737373", "#a3a3a3",
            "#171717", "#d4d4d4", "#262626", "#e5e5e5",
            "#737373", "#a3a3a3"
        ),
    ),
    typography=ThemeTypography(
        font_family="'Malgun Gothic', '맑은 고딕', 'Dotum', '돋움', sans-serif",
        font_family_mono="'D2Coding', 'Consolas', monospace",
        font_size_base="10.5pt",
        font_size_sm="9.5pt",
        font_size_lg="11pt",
        font_size_xl="12.5pt",
        font_size_2xl="15pt",
        font_size_3xl="18pt",
        line_height_normal=1.65,
    ),
    spacing=ThemeSpacing(
        border_radius_sm="2px",
        border_radius_md="4px",
        border_radius_lg="6px",
        border_radius_xl="8px",
        shadow_sm="0 1px 2px rgba(0, 0, 0, 0.03)",
        shadow_md="0 2px 4px rgba(0, 0, 0, 0.05)",
    ),
)


# =============================================================================
# Theme Registry
# =============================================================================

THEMES: dict[ReportTheme, ThemeConfig] = {
    ReportTheme.LIGHT: LIGHT_THEME,
    ReportTheme.DARK: DARK_THEME,
    ReportTheme.MINIMAL: MINIMAL_THEME,
}

THEME_ALIASES = {"default": ReportTheme.LIGHT}
DEPRECATED_THEME_ALIASES = {
    "professional": ReportTheme.LIGHT,
    "modern": ReportTheme.LIGHT,
}


def get_theme(theme: ReportTheme | str) -> ThemeConfig:
    """Get a theme configuration by name or enum.

    Args:
        theme: Theme name or enum value

    Returns:
        ThemeConfig for the requested theme

    Raises:
        ValueError: If theme is not found
    """
    if isinstance(theme, str):
        if theme in THEME_ALIASES:
            theme = THEME_ALIASES[theme]
        elif theme in DEPRECATED_THEME_ALIASES:
            target = DEPRECATED_THEME_ALIASES[theme]
            warnings.warn(
                f"Theme '{theme}' is deprecated and maps to '{target.value}'. "
                f"Available public themes: {get_available_themes()}",
                DeprecationWarning,
                stacklevel=2,
            )
            theme = target
        else:
            try:
                theme = ReportTheme(theme)
            except ValueError:
                available = get_available_themes()
                raise ValueError(
                    f"Unknown theme '{theme}'. Available: {available}"
                )
    elif theme not in THEMES:
        try:
            theme = ReportTheme(theme.value)
        except ValueError:
            available = get_available_themes()
            raise ValueError(
                f"Unknown theme '{getattr(theme, 'value', theme)}'. Available: {available}"
            )

    if theme not in THEMES:
        raise ValueError(f"Theme '{theme.value}' not configured")

    return THEMES[theme]


def get_available_themes() -> list[str]:
    """Get list of available theme names."""
    return [t.value for t in THEMES.keys()]
