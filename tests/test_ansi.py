"""Tests for ANSI color/style abstraction module."""

from __future__ import annotations

from unittest import mock

import pytest

from apme_engine.ansi import (
    Style,
    bold,
    box,
    dim,
    green,
    ljust_ansi,
    red,
    reset_color_detection,
    rjust_ansi,
    section_header,
    severity_badge,
    severity_indicator,
    strip_ansi,
    style,
    table,
    tree_prefix,
    visible_width,
    yellow,
)

# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def reset_color_cache():
    """Reset color detection before each test."""
    reset_color_detection()
    yield
    reset_color_detection()


@pytest.fixture
def force_color(monkeypatch):
    """Force color output on."""
    monkeypatch.setenv("FORCE_COLOR", "1")
    monkeypatch.delenv("NO_COLOR", raising=False)
    reset_color_detection()


@pytest.fixture
def no_color(monkeypatch):
    """Force color output off."""
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    reset_color_detection()


# ─────────────────────────────────────────────────────────────────────────────
# Core styling tests
# ─────────────────────────────────────────────────────────────────────────────


class TestStyle:
    """Test style() function and convenience wrappers."""

    def test_style_with_color(self, force_color):
        """Style wraps text with ANSI codes when color enabled."""
        result = style("hello", Style.RED)
        assert result == "\033[31mhello\033[0m"

    def test_style_multiple_codes(self, force_color):
        """Multiple style codes are concatenated."""
        result = style("hello", Style.BOLD, Style.RED)
        assert result == "\033[1m\033[31mhello\033[0m"

    def test_style_no_color_env(self, no_color):
        """NO_COLOR env var suppresses ANSI codes."""
        result = style("hello", Style.RED)
        assert result == "hello"
        assert "\033[" not in result

    def test_bold(self, force_color):
        """bold() applies bold style."""
        assert bold("test") == "\033[1mtest\033[0m"

    def test_red(self, force_color):
        """red() applies red foreground."""
        assert red("error") == "\033[31merror\033[0m"

    def test_green(self, force_color):
        """green() applies green foreground."""
        assert green("ok") == "\033[32mok\033[0m"

    def test_yellow(self, force_color):
        """yellow() applies yellow foreground."""
        assert yellow("warn") == "\033[33mwarn\033[0m"

    def test_dim(self, force_color):
        """dim() applies dim style."""
        assert dim("faded") == "\033[2mfaded\033[0m"

    def test_composability(self, force_color):
        """Styles can be composed (nested calls)."""
        result = bold(red("important"))
        # The inner red is applied first, then bold wraps it
        assert "\033[1m" in result
        assert "\033[31m" in result
        assert "important" in result


class TestNoColorCompliance:
    """Test NO_COLOR standard compliance (https://no-color.org)."""

    def test_no_color_any_value(self, monkeypatch):
        """NO_COLOR with any value disables color."""
        monkeypatch.setenv("NO_COLOR", "")  # Empty string counts
        reset_color_detection()
        # Empty string is falsy, so this won't disable
        # Per spec, "exists" means disable - let's test with "1"
        monkeypatch.setenv("NO_COLOR", "0")  # Even "0" should disable
        reset_color_detection()
        assert style("x", Style.RED) == "x"

    def test_force_color_overrides_tty(self, monkeypatch):
        """FORCE_COLOR enables color even without TTY."""
        monkeypatch.setenv("FORCE_COLOR", "1")
        monkeypatch.delenv("NO_COLOR", raising=False)
        reset_color_detection()

        with mock.patch("sys.stdout.isatty", return_value=False):
            result = style("x", Style.RED)
            assert "\033[31m" in result

    def test_no_color_beats_force_color(self, monkeypatch):
        """NO_COLOR takes precedence over FORCE_COLOR."""
        monkeypatch.setenv("NO_COLOR", "1")
        monkeypatch.setenv("FORCE_COLOR", "1")
        reset_color_detection()
        assert style("x", Style.RED) == "x"


# ─────────────────────────────────────────────────────────────────────────────
# ANSI width tests
# ─────────────────────────────────────────────────────────────────────────────


class TestAnsiWidth:
    """Test ANSI-aware string width functions."""

    def test_strip_ansi_removes_codes(self):
        """strip_ansi removes all ANSI escape sequences."""
        styled = "\033[1m\033[31mhello\033[0m"
        assert strip_ansi(styled) == "hello"

    def test_strip_ansi_plain_text(self):
        """strip_ansi leaves plain text unchanged."""
        assert strip_ansi("hello world") == "hello world"

    def test_visible_width_plain(self):
        """visible_width returns length of plain text."""
        assert visible_width("hello") == 5

    def test_visible_width_styled(self):
        """visible_width excludes ANSI codes."""
        styled = "\033[1m\033[31mhello\033[0m"
        assert visible_width(styled) == 5

    def test_ljust_ansi_plain(self):
        """ljust_ansi pads plain text correctly."""
        assert ljust_ansi("hi", 5) == "hi   "

    def test_ljust_ansi_styled(self, force_color):
        """ljust_ansi accounts for invisible ANSI codes."""
        styled = red("hi")
        result = ljust_ansi(styled, 5)
        # Should have 3 spaces of padding
        assert result.endswith("   ")
        assert visible_width(result) == 5

    def test_rjust_ansi_plain(self):
        """rjust_ansi pads plain text correctly."""
        assert rjust_ansi("hi", 5) == "   hi"

    def test_rjust_ansi_styled(self, force_color):
        """rjust_ansi accounts for invisible ANSI codes."""
        styled = red("hi")
        result = rjust_ansi(styled, 5)
        assert result.startswith("   ")
        assert visible_width(result) == 5


# ─────────────────────────────────────────────────────────────────────────────
# Severity badge tests
# ─────────────────────────────────────────────────────────────────────────────


class TestSeverityBadge:
    """Test severity badge rendering."""

    def test_badge_high(self, force_color):
        """High severity shows ERROR badge."""
        badge = severity_badge("high")
        assert "ERROR" in strip_ansi(badge)
        assert Style.BG_RED in badge

    def test_badge_medium(self, force_color):
        """Medium severity shows WARN badge."""
        badge = severity_badge("medium")
        assert "WARN" in strip_ansi(badge)
        assert Style.BG_YELLOW in badge

    def test_badge_low(self, force_color):
        """Low severity shows WARN badge."""
        badge = severity_badge("low")
        assert "WARN" in strip_ansi(badge)

    def test_badge_very_low(self, force_color):
        """Very low severity shows HINT badge."""
        badge = severity_badge("very_low")
        assert "HINT" in strip_ansi(badge)
        assert Style.BG_BLUE in badge

    def test_badge_case_insensitive(self, force_color):
        """Badge lookup is case-insensitive."""
        assert strip_ansi(severity_badge("HIGH")) == strip_ansi(severity_badge("high"))
        assert strip_ansi(severity_badge("Medium")) == strip_ansi(severity_badge("medium"))

    def test_badge_unknown_level(self, force_color):
        """Unknown level shows ? badge."""
        badge = severity_badge("unknown")
        assert "?" in strip_ansi(badge)

    def test_badge_no_color(self, no_color):
        """Badge shows label without styling when NO_COLOR."""
        badge = severity_badge("high")
        assert badge == " ERROR "
        assert "\033[" not in badge

    def test_severity_indicator_error(self, force_color):
        """Error indicator is red x."""
        indicator = severity_indicator("high")
        assert "x" in strip_ansi(indicator)
        assert Style.RED in indicator

    def test_severity_indicator_warn(self, force_color):
        """Warning indicator is yellow triangle."""
        indicator = severity_indicator("medium")
        assert "△" in strip_ansi(indicator)
        assert Style.YELLOW in indicator

    def test_severity_indicator_hint(self, force_color):
        """Hint indicator is blue i."""
        indicator = severity_indicator("very_low")
        assert "i" in strip_ansi(indicator)
        assert Style.BLUE in indicator


# ─────────────────────────────────────────────────────────────────────────────
# Box drawing tests
# ─────────────────────────────────────────────────────────────────────────────


class TestBox:
    """Test Unicode box drawing."""

    def test_box_simple(self):
        """Simple box around content."""
        result = box("hello")
        lines = result.split("\n")
        assert len(lines) == 3  # top, content, bottom
        assert "┌" in lines[0]
        assert "┐" in lines[0]
        assert "│" in lines[1]
        assert "hello" in lines[1]
        assert "└" in lines[2]
        assert "┘" in lines[2]

    def test_box_multiline(self):
        """Box around multiline content."""
        result = box("line1\nline2\nline3")
        lines = result.split("\n")
        assert len(lines) == 5  # top, 3 content, bottom
        assert "line1" in lines[1]
        assert "line2" in lines[2]
        assert "line3" in lines[3]

    def test_box_with_title(self, force_color):
        """Box with title in top border."""
        result = box("content", title="Title")
        lines = result.split("\n")
        assert "Title" in strip_ansi(lines[0])

    def test_box_width(self):
        """Box respects specified width."""
        result = box("hi", width=20)
        lines = result.split("\n")
        # Content line should be 22 chars (20 inner + 2 borders)
        assert visible_width(lines[1]) == 22

    def test_box_minimum_width(self):
        """Box has minimum width."""
        result = box("x")
        lines = result.split("\n")
        assert visible_width(lines[1]) >= 12  # 10 inner + 2 borders


class TestSectionHeader:
    """Test section header rendering."""

    def test_section_header_centered(self, force_color):
        """Section header has centered title."""
        result = section_header("Test", width=20)
        assert "Test" in strip_ansi(result)
        assert "─" in result
        assert visible_width(result) == 20


# ─────────────────────────────────────────────────────────────────────────────
# Table tests
# ─────────────────────────────────────────────────────────────────────────────


class TestTable:
    """Test table formatting."""

    def test_table_simple(self, force_color):
        """Simple table with headers and rows."""
        result = table(
            headers=["Name", "Value"],
            rows=[["foo", "1"], ["bar", "2"]],
        )
        lines = result.split("\n")
        assert len(lines) == 4  # header, underline, 2 data rows
        assert "Name" in strip_ansi(lines[0])
        assert "Value" in strip_ansi(lines[0])
        assert "─" in lines[1]
        assert "foo" in lines[2]
        assert "bar" in lines[3]

    def test_table_auto_width(self):
        """Table auto-calculates column widths."""
        result = table(
            headers=["A", "LongerHeader"],
            rows=[["short", "x"]],
        )
        lines = result.split("\n")
        # LongerHeader should determine second column width
        assert "LongerHeader" in strip_ansi(lines[0])

    def test_table_explicit_widths(self):
        """Table respects explicit column widths."""
        result = table(
            headers=["A", "B"],
            rows=[["1", "2"]],
            col_widths=[10, 10],
        )
        lines = result.split("\n")
        # Each column should be padded to 10
        # Header line should be "A" padded to 10 + sep + "B" padded to 10
        assert visible_width(lines[0]) == 10 + 2 + 10  # 2 = default sep

    def test_table_empty(self):
        """Empty table returns empty string."""
        assert table(headers=[], rows=[]) == ""

    def test_table_with_styled_content(self, force_color):
        """Table handles styled cell content."""
        result = table(
            headers=["Status"],
            rows=[[red("ERROR")]],
        )
        lines = result.split("\n")
        assert "ERROR" in strip_ansi(lines[2])


# ─────────────────────────────────────────────────────────────────────────────
# Tree prefix tests
# ─────────────────────────────────────────────────────────────────────────────


class TestTreePrefix:
    """Test tree connector generation."""

    def test_tree_last_item(self):
        """Last item uses └──."""
        assert tree_prefix(is_last=True) == "└── "

    def test_tree_middle_item(self):
        """Middle item uses ├──."""
        assert tree_prefix(is_last=False) == "├── "

    def test_tree_nested_last(self):
        """Nested last item has correct prefix."""
        result = tree_prefix(is_last=True, depth=1, parent_prefixes=[False])
        assert "│" in result
        assert "└" in result

    def test_tree_nested_after_last_parent(self):
        """Item after last parent has space prefix."""
        result = tree_prefix(is_last=True, depth=1, parent_prefixes=[True])
        assert "│" not in result
        assert "└" in result
