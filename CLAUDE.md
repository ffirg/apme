# APME - Ansible Policy & Modernization Engine

## Project Constitution

This document is the authoritative source of truth for AI agents. All development must align with these principles.

## General Rules

- When working with multiple repositories/projects, always confirm the correct working directory before making changes or creating files. Use `pwd` and `git remote -v` to verify.
- Before starting work, ask clarifying questions about scope rather than assuming. Do not begin executing until the user confirms the approach.
- Never commit to git without explicit user approval.

## Project Context

Primary languages and file types: Markdown documentation, Shell/Bash scripts, Python scripts, JavaScript. Most work involves documentation systems (.sdlc/), automation scripts, and JIRA/AAP infrastructure tooling.

## Overview

APME is a multi-service system that automates policy enforcement and modernization of Ansible content for AAP 2.5+. Services: Primary Orchestrator, Native/OPA/Ansible/Gitleaks Validators, Remediation Engine, CLI.

## Architecture

```
┌──────────────────────────────── apme-pod ─────────────────────────────┐
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Primary  │  │  Native  │  │   OPA    │  │ Ansible  │  │ Gitleaks │ │
│  │  :50051  │  │  :50055  │  │  :50054  │  │  :50053  │  │  :50056  │ │
│  └────┬─────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│  ┌────┴─────────────────────────────────────┐                         │
│  │         Cache Maintainer :50052          │                         │
│  └──────────────────────────────────────────┘                         │
└────────────────────────────────────────────────────────────────────────┘
```

Full details: [architecture.md](/.sdlc/context/architecture.md) | [deployment.md](/.sdlc/context/deployment.md)

## Project Structure

The `.sdlc/` directory structure:
- `context/` — Project context docs (architecture, deployment, conventions)
- `specs/` — Requirement specifications (REQ-NNN directories with tasks)
- `decisions/` — Decision requests (open/, closed/)
- `adrs/` — Architecture Decision Records

Do not confuse these directories.

## Key ADRs

| ADR | Decision |
|-----|----------|
| [ADR-001](/.sdlc/adrs/ADR-001-grpc-communication.md) | gRPC for all inter-service communication |
| [ADR-003](/.sdlc/adrs/ADR-003-vendor-ari-engine.md) | Vendored ARI engine (NOT a pip dependency) |
| [ADR-007](/.sdlc/adrs/ADR-007-async-grpc-servers.md) | Async gRPC (grpc.aio) for all servers |
| [ADR-008](/.sdlc/adrs/ADR-008-rule-id-conventions.md) | Rule IDs: L=Lint, M=Modernize, R=Risk, P=Policy, SEC=Secrets |
| [ADR-009](/.sdlc/adrs/ADR-009-remediation-engine.md) | Validators are read-only; remediation is separate |

Full list: `.sdlc/adrs/README.md`

## Spec-Driven Development

All features follow: **Spec First → DR for Questions → ADR for Decisions → Traceability**

| Skill | Purpose |
|-------|---------|
| `/sdlc-status` | Dashboard: REQ/DR/ADR status and blockers |
| `/req-new` | Create requirement spec |
| `/task-new` | Create implementation task |
| `/dr-new` | Capture blocking question |
| `/dr-review` | Resolve blocking DRs |
| `/adr-new` | Document architectural decision |
| `/adr-review` | Accept/reject proposed ADRs |

Full workflow: [workflow.md](/.sdlc/context/workflow.md) | Getting started: [getting-started.md](/.sdlc/context/getting-started.md)

## Agent Constraints

- **Follow ADRs** — no deviation without a new ADR
- **Validators are read-only** — detection only, no file modification
- **Use gRPC** — all inter-service communication
- **Async servers** — grpc.aio, not synchronous
- **Rule IDs** — L/M/R/P/SEC convention per ADR-008
- Do NOT modify files outside task scope
- Do NOT add features not in requirements
- Ask for clarification if specs are ambiguous

## Tool Usage

- When fetching web content, prefer `curl` over WebFetch for authenticated or API-based requests.
- If a URL returns 403/blocked, immediately pivot to alternative sources rather than retrying.

## Architectural Change Detection

**IMPORTANT**: Before completing any task, check if the work involves architectural changes. If yes, an ADR is required.

### Triggers for ADR

Raise an ADR (`/adr-new`) when work involves:

| Category | Examples |
|----------|----------|
| **New dependencies** | Adding packages to pyproject.toml, new container images |
| **API/Protocol changes** | New proto messages, changed gRPC contracts, new endpoints |
| **Data format changes** | New output formats, schema changes, serialization changes |
| **Service topology** | New containers, changed ports, new communication paths |
| **Security boundaries** | Auth changes, new trust boundaries, secret handling |
| **Storage/Persistence** | Database choices, caching strategies, file formats |
| **CLI interface** | New commands, changed flags, output format options |
| **Integration patterns** | How APME connects to external systems (AAP, Galaxy, etc.) |

### Self-Check Prompt

At task completion, ask yourself:
```
Does this work change HOW the system works (not just WHAT it does)?
- Yes → Create ADR before marking task complete
- No  → Proceed with task completion
```

### Quick ADR Check

If uncertain, use `/adr-check` to evaluate if current work needs an ADR.

## Quality Gates

Before completing any task:
- [ ] All unit tests pass
- [ ] Code follows style guidelines ([conventions.md](/.sdlc/context/conventions.md))
- [ ] gRPC changes regenerated (`scripts/gen_grpc.sh`)
- [ ] TASK verification steps completed

## Security

See [SECURITY.md](/SECURITY.md) for comprehensive guidelines.

**Quick reminders:** Pre-commit hooks enforce gitleaks/bandit. Never commit `.env`. Containers run non-root. Log `[REDACTED]` not secrets.

## Container Rebuild Rules

Rebuild required after modifying: `src/**/*.py`, `validators/**/*.py`, `proto/**/*.proto`, `pyproject.toml`, `Containerfile*`

**Workflow:** `stop` → `build` → `start`

**No rebuild:** `docs/*.md`, `.sdlc/**/*.md`

## Release Process

**Update:** `pyproject.toml` version, `CHANGELOG.md`, container tags

**Checklist:** Tests pass → Security audit green → CHANGELOG updated → Version bumped → Tag `vX.Y.Z` → Images pushed

## References

- [architecture.md](/.sdlc/context/architecture.md) — Container topology, ports, concurrency
- [deployment.md](/.sdlc/context/deployment.md) — Podman pod setup
- [conventions.md](/.sdlc/context/conventions.md) — Coding standards
- [SECURITY.md](/SECURITY.md) — Security policy
- [CONTRIBUTING.md](/CONTRIBUTING.md) — Development workflow
