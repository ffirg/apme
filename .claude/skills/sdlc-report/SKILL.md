---
name: sdlc-report
description: >-
  Generate the SDLC Framework executive summary report. Use after making
  changes to skills, workflow, or directory structure. Produces
  SDLC-FRAMEWORK.md with current skills, artifact types, and workflow.
  Do NOT use for checking status (use sdlc-status instead).
argument-hint: "[--output PATH]"
user-invocable: true
disable-model-invocation: true
metadata:
  author: APME Team
  version: 1.0.0
---

# SDLC Report

Generate the SDLC Framework executive summary document.

## Arguments

If `$ARGUMENTS` is provided, parse for:
- `--output PATH` → write to custom path (default: `SDLC-FRAMEWORK.md` in project root)

## Usage

```
/sdlc-report                           # Generate report to project root
/sdlc-report --output docs/framework.md  # Custom output path
```

## Behavior

### 1. Gather Current State

Scan the project to collect current information:

**Skills** — Read `.claude/skills/*/SKILL.md`:
- Extract skill name, description, argument-hint
- Build skills reference table

**Directory Structure** — Verify `.sdlc/` directories exist:
- `context/`, `phases/`, `specs/`, `adrs/`, `decisions/`, `templates/`
- Note any missing directories

**Artifact Counts** — Count current artifacts:
- Phases in `.sdlc/phases/`
- REQs in `.sdlc/specs/`
- ADRs in `.sdlc/adrs/`
- Open/closed DRs in `.sdlc/decisions/`

### 2. Generate Report Sections

Build the report with these sections:

#### Executive Summary
Static content explaining the framework's purpose and benefits.

#### The Transformation
Table: Input (PRD) → Process (Specs) → Output (Software)

#### Key Benefits
- Traceability
- AI-Ready
- Decision Log
- Progress Visibility
- Reduced Ambiguity

#### Information Hierarchy
Table showing the 6 levels from CLAUDE.md down to src/

#### Directory Structure
```
.sdlc/
├── context/
├── phases/
├── specs/
├── adrs/
├── decisions/
└── templates/
```
Include subdirectory details.

#### Artifact Types
Explain REQ, TASK, DR, ADR with their purposes.

#### The Workflow
ASCII diagram showing Assess → Unblock → Specify → Execute cycle.

#### Skills Reference
**Dynamic table** built from scanned skills:

| Skill | Purpose | Arguments |
|-------|---------|-----------|
| `/skill-name` | From description | From argument-hint |

Sort skills by category:
1. Status/Navigation: sdlc-status, workflow
2. Planning: phase-new, req-new, task-new
3. Decisions: dr-new, dr-review, adr-new, adr-review, adr-check
4. Reporting: sdlc-report

#### Core Principles
Static content on Spec-First, Traceable, Question-Driven, Decision-Logged, AI-Optimized.

#### Quick Start
Command examples for new projects, existing projects, during work.

#### Related Documentation
Links to CLAUDE.md, workflow.md, getting-started.md, etc.

### 3. Write Output

Write the generated markdown to the output path.

### 4. Summary

```
Generated SDLC Framework report:
- Output: SDLC-FRAMEWORK.md
- Skills documented: 11
- Artifact counts: 4 phases, 4 REQs, 14 ADRs, 10 DRs

Review the report? (Y/n)
```

If yes, display the first 50 lines.

## Template Structure

The report follows this structure:

```markdown
# Spec-Driven Development Framework

## Executive Summary
[Static intro + transformation table + benefits table]

## The Approach
[Philosophy quote + 4 numbered points]

## The Information Hierarchy
[6-level table]

## Directory Structure
[Tree diagram with descriptions]

## Artifact Types
[REQ, TASK, DR, ADR explanations]

## The Workflow
[ASCII diagram + step descriptions]

## Skills Reference
[Dynamic table from scanned skills]

## Core Principles
[5-principle table]

## Quick Start
[Command examples]

## Related Documentation
[Links table]
```

## Dynamic Content

These sections are dynamically generated:

| Section | Source |
|---------|--------|
| Skills Reference | `.claude/skills/*/SKILL.md` |
| Artifact counts (optional) | `.sdlc/phases/`, `specs/`, `adrs/`, `decisions/` |

## Static Content

These sections use fixed content:
- Executive Summary
- The Approach
- Information Hierarchy
- Directory Structure
- Artifact Types
- Workflow diagram
- Core Principles
- Quick Start
- Related Documentation

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Skill missing SKILL.md | Skip with warning |
| Skill missing description | Use name as fallback |
| Output path doesn't exist | Create parent directories |
| Output file exists | Overwrite (this is a generated file) |

## When to Run

Run `/sdlc-report` after:
- Adding or modifying skills
- Changing workflow process
- Updating directory structure
- Before sharing framework documentation
- After major SDLC updates
