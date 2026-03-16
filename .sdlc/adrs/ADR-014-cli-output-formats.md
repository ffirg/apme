# ADR-014: CLI Output Formats

## Status

Accepted

## Date

2026-03-13

## Reviewed

2026-03-16

## Context

The APME CLI needs to present scan results to users in multiple contexts:

1. **Interactive terminal use** — developers running scans locally
2. **CI/CD pipelines** — automated checks in Jenkins, GitHub Actions, GitLab CI
3. **Reporting** — shareable artifacts for reviews, audits, documentation
4. **Automation** — programmatic consumption by other tools

Each context has different requirements for format, interactivity, and portability.

**Constraints**:
- Zero new dependencies strongly preferred
- Must work offline (no external services)
- Container-friendly (minimal image size)
- Fast startup time for CLI tool

**Research**: See `.sdlc/research/cli-reporting-options.md` and architect's analysis in `ansi_style_abstraction_*.plan.md`.

## Decision

**We will provide four output formats via CLI flags, using an internal zero-dependency ANSI module for terminal styling and HTML export.**

### Rich vs Internal ANSI: Trade-off

| Approach | Size | Complexity | Control |
|----------|------|------------|---------|
| Rich + deps | ~1.6 MB (rich + pygments + markdown-it-py + mdurl) | 30K+ lines, 95% unused | Rich's opinions on layout |
| Internal ANSI | ~150-200 lines | Single file, fully typed | Pixel-perfect badges |

**Decision**: Build internally. The feature surface is tiny (8 colors, badges, boxes, tables, tree chars). Rich would add 1.6MB of dependencies for features we'd never use (syntax highlighting, markdown rendering, Jupyter integration).

### Output Formats

| Format | Flag | Use Case |
|--------|------|----------|
| ANSI terminal | `--format rich` (default) | Interactive developer use |
| JSON | `--format json` / `--json` | Automation, tool integration |
| JUnit XML | `--format junit` / `--junit FILE` | CI/CD test reporting |
| HTML | `--format html` / `--html FILE` | Shareable reports |

### CLI Interface

```bash
# Default: ANSI-styled terminal output
apme scan .

# JSON to stdout
apme scan . --json
apme scan . --format json

# JSON to file
apme scan . --format json --output results.json

# JUnit XML (file required)
apme scan . --junit results.xml
apme scan . --format junit --output results.xml

# HTML report (file required)
apme scan . --html report.html
apme scan . --format html --output report.html
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No errors (warnings/hints OK) |
| 1 | Errors found |
| 2 | Scan failed (invalid input, service unavailable) |

## Implementation

### Module: `src/apme_engine/ansi.py`

Zero-dependency ANSI styling abstraction (~150-200 lines):

```python
# TTY/NO_COLOR detection (https://no-color.org)
def _use_color() -> bool: ...

# Style constants (ANSI SGR codes)
class Style:
    RESET, BOLD, DIM, UNDERLINE, REVERSE = ...
    RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, GRAY = ...
    BG_RED, BG_YELLOW, BG_BLUE, BG_GREEN = ...

# Core functions
def style(text: str, *styles: str) -> str: ...
def bold(text: str) -> str: ...
def red(text: str) -> str: ...
# ... etc

# Higher-level helpers
def severity_badge(level: str) -> str: ...  # ERROR/WARN/HINT badges
def box(text: str, title: str = "") -> str: ...  # Unicode box drawing
def table(headers, rows, col_widths) -> str: ...  # Simple columnar
TREE_LAST, TREE_MID, TREE_PIPE = ...  # Tree connectors
```

### Key Design Decisions

- **Pure functions** — no class instantiation, composable
- **NO_COLOR / FORCE_COLOR** — follows no-color.org spec
- **Severity mapping**:
  - `very_high`/`high` → `ERROR` (red background)
  - `medium`/`low` → `WARN` (yellow background)
  - `very_low`/`none` → `HINT` (blue background)
- **Box drawing** — Unicode chars (work everywhere), not ANSI
- **ANSI-aware width** — strip codes before measuring for alignment

### Changes to `cli.py`

New function `_render_scan_results()` replaces inline print() calls:

1. **Summary box** — scan status (PASSED/FAILED), counts, scan time
2. **Issues table** — Rule, Severity (badge), Message, Location
3. **Issues by file** — tree-grouped with severity indicators (`x`, `△`, `i`)

### Scope Boundaries

- Does NOT add any dependencies
- Does NOT change JSON output (`--json` flag unchanged)
- Does NOT change violation data model or validator logic
- Does NOT change the ARI engine CLI (`engine/cli/`)

## Alternatives Considered

### Alternative 1: Rich Library

**Description**: Use Rich for terminal styling and `Console.save_html()` for HTML export.

**Pros**:
- Full-featured library
- HTML export built-in

**Cons**:
- 1.6 MB dependency chain (rich + pygments + markdown-it-py + mdurl)
- 30K+ lines for features we won't use (syntax highlighting, markdown)
- Stringly-typed markup (`"[bold red]text[/]"`) vs typed functions
- Import overhead (pygments loads eagerly)
- Rich's layout opinions may not match exact design

**Why not chosen**: Massive overkill. We need ~150 lines of code, not 30K+ lines of library.

### Alternative 2: Textual TUI Dashboard

**Description**: Interactive terminal UI with navigation, filtering, drill-down.

**Pros**: Rich interactivity, runs in terminal

**Cons**: Additional ~2MB dependency, overkill for most use cases

**Why not chosen**: Can be added as optional v2 feature if demand exists.

### Alternative 3: Custom Jinja2 HTML Templates

**Description**: Use Jinja2 for semantic HTML with custom CSS/JS.

**Pros**: Full control, interactive features

**Cons**: Template maintenance, adds Jinja2 dependency

**Why not chosen**: For v1, simple ANSI-to-HTML conversion is sufficient.

## Consequences

### Positive

- Zero new dependencies
- Fast startup (no pygments import)
- Fully typed API (`bold(red("text"))` vs `"[bold red]text[/]"`)
- Pixel-perfect control over badge rendering
- Small container image footprint
- NO_COLOR compliance in 5 lines

### Negative

- Must maintain ~150-200 lines of ANSI code
- HTML output is ANSI-to-HTML conversion (not semantic)
- No syntax highlighting (acceptable for our use case)

### Neutral

- HTML reports require explicit `--html FILE` flag
- JSON output goes to stdout by default

## Related Decisions

- ADR-001: gRPC communication (CLI receives ScanResponse)
- ADR-013: Structured diagnostics (diagnostics in JSON with `-v`)

## References

- Architect's analysis: `ansi_style_abstraction_*.plan.md`
- no-color.org standard
- `.sdlc/research/cli-reporting-options.md`

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-13 | Claude | Initial proposal (Rich-based) |
| 2026-03-16 | Claude | Revised to internal ANSI module per architect analysis |
