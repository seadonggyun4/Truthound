"""Theme system for Data Docs report generation.

This module provides a comprehensive theming system for customizing
report appearance, including white-labeling for enterprise use.

Available public themes:
- LightTheme: Korean public/research A4 report theme
- DarkTheme: Dark report theme with the same structure
- MinimalTheme: Low-chroma formal report theme

Features:
- CSS custom properties for easy customization
- Logo and branding support
- YAML/JSON configuration loading
- Theme inheritance and composition
"""

from truthound.datadocs.themes.base import (
    Theme,
    BaseTheme,
    ThemeConfig,
    ThemeColors,
    ThemeTypography,
    ThemeSpacing,
    ThemeAssets,
)
from truthound.datadocs.themes.default import (
    DefaultTheme,
    LightTheme,
    DarkTheme,
    MinimalTheme,
    ModernTheme,
    ProfessionalTheme,
)
from truthound.datadocs.themes.enterprise import (
    EnterpriseTheme,
    EnterpriseThemeConfig,
    BrandingConfig,
)
from truthound.datadocs.themes.loader import (
    ThemeLoader,
    load_theme_from_yaml,
    load_theme_from_json,
    load_theme_from_dict,
)
from truthound.datadocs.themes.default import (
    BUILT_IN_THEMES,
    get_theme,
    list_themes,
)

# Backwards compatibility aliases
LIGHT_THEME = LightTheme()
DARK_THEME = DarkTheme()
MINIMAL_THEME = MinimalTheme()
THEMES = BUILT_IN_THEMES


def get_available_themes() -> list[str]:
    """Get list of available theme names."""
    return list_themes()


__all__ = [
    # Base
    "Theme",
    "BaseTheme",
    "ThemeConfig",
    "ThemeColors",
    "ThemeTypography",
    "ThemeSpacing",
    "ThemeAssets",
    # Default themes
    "DefaultTheme",
    "LightTheme",
    "DarkTheme",
    "MinimalTheme",
    # Enterprise
    "EnterpriseTheme",
    "EnterpriseThemeConfig",
    "BrandingConfig",
    # Loader
    "ThemeLoader",
    "load_theme_from_yaml",
    "load_theme_from_json",
    "load_theme_from_dict",
    # Backwards compatibility
    "LIGHT_THEME",
    "DARK_THEME",
    "MINIMAL_THEME",
    "THEMES",
    "get_theme",
    "get_available_themes",
]
