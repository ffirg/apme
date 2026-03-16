---
name: adr-check
description: >-
  Check if current work requires an Architecture Decision Record.
  Use after completing research, at task completion, when adding dependencies,
  changing APIs, or when uncertain if work is architectural. Evaluates changes
  against ADR triggers and recommends action. Do NOT use for creating ADRs
  (use adr-new instead).
argument-hint: "[description of work] or [--from-task TASK-NNN]"
user-invocable: true
disable-model-invocation: false
metadata:
  author: APME Team
  version: 1.0.0
---

# ADR Check

Evaluate if current work requires an Architecture Decision Record.

## Arguments

- `$ARGUMENTS` — Description of the work being evaluated
- `--from-task TASK-NNN` — Evaluate a specific task's changes

## Usage

```
/adr-check                              # Check current conversation context
/adr-check "Added Rich output formats"  # Check specific work
/adr-check --from-task TASK-001         # Check task deliverables
```

## Behavior

### 1. Gather Context

**From conversation**: Review recent messages for:
- Files modified
- Dependencies added
- Patterns introduced
- Decisions made

**From task**: If `--from-task TASK-NNN`:
- Read the task file
- Check deliverables section
- Review files created/modified

**From description**: Parse the provided description for architectural signals.

### 2. Check Against ADR Triggers

Evaluate against these categories:

| Category | ADR Trigger Signals |
|----------|---------------------|
| **Dependencies** | New entries in pyproject.toml, new imports, new container images |
| **API/Protocol** | Proto file changes, new RPC methods, changed message types |
| **Data Formats** | New serialization formats, schema changes, output format options |
| **Service Topology** | New containers, port changes, new service communication |
| **Security** | Auth mechanisms, trust boundaries, secret handling changes |
| **Storage** | Database choices, caching strategies, persistence patterns |
| **CLI Interface** | New commands, new flags, output format conventions |
| **Integration** | External system connections, webhook patterns, plugin interfaces |

### 3. Score the Changes

For each category, assign:
- **0** = No change
- **1** = Minor change (follows existing patterns)
- **2** = Significant change (new pattern or approach)
- **3** = Major change (fundamental shift)

### 4. Make Recommendation

| Total Score | Recommendation |
|-------------|----------------|
| 0-2 | No ADR needed |
| 3-5 | ADR recommended (document the decision) |
| 6+ | ADR required (significant architectural impact) |

### 5. Output Result

```markdown
## ADR Check Result

**Work evaluated**: [description or task reference]

### Changes Detected

| Category | Score | Details |
|----------|-------|---------|
| Dependencies | 0 | No new dependencies |
| Data Formats | 2 | New JSON output schema, HTML export |
| CLI Interface | 2 | New --format, --json, --html flags |
| ... | ... | ... |

**Total Score**: 4/24

### Recommendation

**ADR Recommended**

This work introduces new CLI output format conventions that should be
documented for consistency across the project.

### Suggested ADR

Title: CLI Output Formats
Category: CLI Interface / Data Formats
Key decisions:
- Four output formats (rich, json, junit, html)
- Flag conventions (--format, shortcuts)
- Exit code semantics

Create ADR? → `/adr-new "CLI Output Formats"`
```

## Quick Mode

If obviously architectural (proto changes, new containers, new deps):
```
ADR Required: This work modifies [proto files / adds dependencies / etc.]
Create ADR? → /adr-new "[suggested title]"
```

If obviously not architectural (docs, tests, bugfixes):
```
No ADR Needed: This work is [documentation / test / bugfix] only.
```

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Mixed architectural + non-architectural | Focus on architectural parts |
| Unclear if architectural | Default to "recommended" with explanation |
| Already has ADR | Note existing ADR, check if update needed |
| Research task | Check if research concluded with a decision |

## Integration

This skill is referenced in CLAUDE.md under "Architectural Change Detection".
Agents should run `/adr-check` at task completion when uncertain.
