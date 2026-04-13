"""Tests for SARIF 2.1.0 output generation."""

from __future__ import annotations

from typing import cast

from apme_engine.cli.sarif import violations_to_sarif

_SarifNode = dict[str, object]


def _violation(
    *,
    rule_id: str = "L003",
    severity: str = "low",
    message: str = "Use FQCN",
    file: str = "playbooks/site.yml",
    line: int | list[int] | None = 10,
) -> dict[str, str | int | list[int] | bool | None]:
    return {
        "rule_id": rule_id,
        "severity": severity,
        "message": message,
        "file": file,
        "line": line,
        "path": "",
        "remediation_class": "auto-fixable",
        "remediation_resolution": "unresolved",
        "scope": "task",
    }


def _run(doc: _SarifNode) -> _SarifNode:
    """Extract the first run from a SARIF document.

    Args:
        doc: SARIF document dict.

    Returns:
        The first run object.
    """
    runs = cast(list[_SarifNode], doc["runs"])
    return runs[0]


def _results(doc: _SarifNode) -> list[_SarifNode]:
    """Extract results from the first run.

    Args:
        doc: SARIF document dict.

    Returns:
        List of result objects.
    """
    return cast(list[_SarifNode], _run(doc)["results"])


def _rules(doc: _SarifNode) -> list[_SarifNode]:
    """Extract rule descriptors from the first run.

    Args:
        doc: SARIF document dict.

    Returns:
        List of reporting descriptor objects.
    """
    driver = cast(_SarifNode, cast(_SarifNode, _run(doc)["tool"])["driver"])
    return cast(list[_SarifNode], driver["rules"])


def _driver(doc: _SarifNode) -> _SarifNode:
    """Extract the tool driver from the first run.

    Args:
        doc: SARIF document dict.

    Returns:
        Driver object.
    """
    return cast(_SarifNode, cast(_SarifNode, _run(doc)["tool"])["driver"])


def _location(result: _SarifNode) -> _SarifNode:
    """Extract the first location from a result.

    Args:
        result: SARIF result object.

    Returns:
        First location object.
    """
    locs = cast(list[_SarifNode], result["locations"])
    return locs[0]


def _phys(result: _SarifNode) -> _SarifNode:
    """Extract physicalLocation from a result's first location.

    Args:
        result: SARIF result object.

    Returns:
        Physical location object.
    """
    return cast(_SarifNode, _location(result)["physicalLocation"])


class TestSarifStructure:
    """Basic SARIF document structure."""

    def test_empty_violations_produces_valid_sarif(self) -> None:
        """An empty violation list produces a valid SARIF with zero results."""
        doc = violations_to_sarif([])
        assert doc["version"] == "2.1.0"
        assert cast(str, doc["$schema"]).endswith("sarif-schema-2.1.0.json")
        runs = cast(list[_SarifNode], doc["runs"])
        assert len(runs) == 1
        assert _results(doc) == []
        assert _rules(doc) == []

    def test_single_violation(self) -> None:
        """One violation maps to one result and one rule descriptor."""
        doc = violations_to_sarif([_violation()])
        assert len(_results(doc)) == 1
        assert len(_rules(doc)) == 1

        result = _results(doc)[0]
        assert result["ruleId"] == "L003"
        assert cast(_SarifNode, result["message"])["text"] == "Use FQCN"

    def test_tool_version_included(self) -> None:
        """Tool version appears in the driver when provided."""
        doc = violations_to_sarif([], tool_version="1.2.3")
        driver = _driver(doc)
        assert driver["version"] == "1.2.3"
        assert driver["semanticVersion"] == "1.2.3"

    def test_tool_version_absent_when_not_provided(self) -> None:
        """Driver omits version fields when tool_version is None."""
        doc = violations_to_sarif([])
        driver = _driver(doc)
        assert "version" not in driver


class TestSeverityMapping:
    """APME severity labels map to SARIF levels."""

    def test_critical_maps_to_error(self) -> None:
        """Critical severity maps to SARIF 'error'."""
        doc = violations_to_sarif([_violation(severity="critical")])
        assert _results(doc)[0]["level"] == "error"

    def test_high_maps_to_error(self) -> None:
        """High severity maps to SARIF 'error'."""
        doc = violations_to_sarif([_violation(severity="high")])
        assert _results(doc)[0]["level"] == "error"

    def test_medium_maps_to_warning(self) -> None:
        """Medium severity maps to SARIF 'warning'."""
        doc = violations_to_sarif([_violation(severity="medium")])
        assert _results(doc)[0]["level"] == "warning"

    def test_low_maps_to_note(self) -> None:
        """Low severity maps to SARIF 'note'."""
        doc = violations_to_sarif([_violation(severity="low")])
        assert _results(doc)[0]["level"] == "note"

    def test_info_maps_to_note(self) -> None:
        """Info severity maps to SARIF 'note'."""
        doc = violations_to_sarif([_violation(severity="info")])
        assert _results(doc)[0]["level"] == "note"

    def test_unknown_severity_defaults_to_warning(self) -> None:
        """Unknown severity strings default to SARIF 'warning'."""
        doc = violations_to_sarif([_violation(severity="banana")])
        assert _results(doc)[0]["level"] == "warning"


class TestLocationMapping:
    """File paths and line numbers in SARIF locations."""

    def test_single_line(self) -> None:
        """Integer line becomes startLine in region."""
        doc = violations_to_sarif([_violation(line=42)])
        phys = _phys(_results(doc)[0])
        region = cast(_SarifNode, phys["region"])
        assert region["startLine"] == 42

    def test_line_range(self) -> None:
        """List [start, end] becomes startLine + endLine."""
        doc = violations_to_sarif([_violation(line=[10, 20])])
        region = cast(_SarifNode, _phys(_results(doc)[0])["region"])
        assert region["startLine"] == 10
        assert region["endLine"] == 20

    def test_no_line(self) -> None:
        """None line omits the region entirely."""
        doc = violations_to_sarif([_violation(line=None)])
        phys = _phys(_results(doc)[0])
        assert "region" not in phys

    def test_file_uri_strips_dot_slash(self) -> None:
        """Leading './' is stripped from file URIs."""
        doc = violations_to_sarif([_violation(file="./roles/main.yml")])
        phys = _phys(_results(doc)[0])
        artifact = cast(_SarifNode, phys["artifactLocation"])
        assert artifact["uri"] == "roles/main.yml"

    def test_srcroot_base_id(self) -> None:
        """Artifact location uses %SRCROOT% as uriBaseId."""
        doc = violations_to_sarif([_violation()])
        phys = _phys(_results(doc)[0])
        artifact = cast(_SarifNode, phys["artifactLocation"])
        assert artifact["uriBaseId"] == "%SRCROOT%"

    def test_empty_file_omits_artifact_location(self) -> None:
        """Empty file path produces physicalLocation without artifactLocation."""
        doc = violations_to_sarif([_violation(file="")])
        phys = _phys(_results(doc)[0])
        assert "artifactLocation" not in phys

    def test_dot_slash_only_omits_artifact_location(self) -> None:
        """File path of just './' is treated as empty."""
        doc = violations_to_sarif([_violation(file="./")])
        phys = _phys(_results(doc)[0])
        assert "artifactLocation" not in phys

    def test_line_range_clamps_zero_start(self) -> None:
        """Line range with start=0 is clamped to 1."""
        doc = violations_to_sarif([_violation(line=[0, 5])])
        region = cast(_SarifNode, _phys(_results(doc)[0])["region"])
        assert region["startLine"] == 1
        assert region["endLine"] == 5

    def test_line_range_clamps_negative(self) -> None:
        """Negative line values are clamped to 1."""
        doc = violations_to_sarif([_violation(line=[-3, -1])])
        region = cast(_SarifNode, _phys(_results(doc)[0])["region"])
        assert region["startLine"] == 1
        assert region["endLine"] == 1

    def test_line_range_end_less_than_start(self) -> None:
        """End < start is clamped so end >= start."""
        doc = violations_to_sarif([_violation(line=[10, 5])])
        region = cast(_SarifNode, _phys(_results(doc)[0])["region"])
        assert region["startLine"] == 10
        assert region["endLine"] == 10

    def test_zero_line_omits_region(self) -> None:
        """Line value of 0 omits the region."""
        doc = violations_to_sarif([_violation(line=0)])
        phys = _phys(_results(doc)[0])
        assert "region" not in phys


class TestRuleDeduplication:
    """Multiple violations with the same rule_id produce one rule descriptor."""

    def test_duplicate_rules_deduplicated(self) -> None:
        """Two violations with the same rule_id produce one rule entry."""
        doc = violations_to_sarif(
            [
                _violation(rule_id="L003", message="first"),
                _violation(rule_id="L003", message="second"),
            ]
        )
        assert len(_results(doc)) == 2
        assert len(_rules(doc)) == 1

    def test_different_rules_both_listed(self) -> None:
        """Violations with different rule_ids produce separate rule entries."""
        doc = violations_to_sarif(
            [
                _violation(rule_id="L003"),
                _violation(rule_id="M005"),
            ]
        )
        rule_ids = [r["id"] for r in _rules(doc)]
        assert "L003" in rule_ids
        assert "M005" in rule_ids


class TestRuleHelpText:
    """Rule ID prefixes map to descriptive help text."""

    def test_lint_prefix(self) -> None:
        """L-prefix rules get lint help text."""
        doc = violations_to_sarif([_violation(rule_id="L003")])
        rule = _rules(doc)[0]
        assert "Lint" in cast(str, cast(_SarifNode, rule["help"])["text"])

    def test_modernize_prefix(self) -> None:
        """M-prefix rules get modernization help text."""
        doc = violations_to_sarif([_violation(rule_id="M005")])
        rule = _rules(doc)[0]
        assert "Modernization" in cast(str, cast(_SarifNode, rule["help"])["text"])

    def test_security_prefix(self) -> None:
        """SEC-prefix rules get security help text."""
        doc = violations_to_sarif([_violation(rule_id="SEC:generic-api-key")])
        rule = _rules(doc)[0]
        assert "Security" in cast(str, cast(_SarifNode, rule["help"])["text"])

    def test_empty_message_falls_back_to_rule_id(self) -> None:
        """Empty message text falls back to rule_id for SARIF compliance."""
        doc = violations_to_sarif([_violation(rule_id="L003", message="")])
        result = _results(doc)[0]
        assert cast(_SarifNode, result["message"])["text"] == "L003"

    def test_help_uri_url_encodes_rule_id(self) -> None:
        """Rule IDs with special characters are URL-encoded in helpUri."""
        doc = violations_to_sarif([_violation(rule_id="SEC:generic-api-key")])
        rule = _rules(doc)[0]
        help_uri = cast(str, rule["helpUri"])
        assert "SEC%3Ageneric-api-key" in help_uri
        assert ":" not in help_uri.split("/rules/")[1]
