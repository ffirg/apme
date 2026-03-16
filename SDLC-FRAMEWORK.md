# Spec-Driven Development Framework

## Executive Summary

This framework enables **AI-assisted software development** through structured specifications. By defining requirements, decisions, and architecture in a consistent format, both human developers and AI agents can collaborate effectively on complex projects.

### The Transformation

| Input | Process | Output |
|-------|---------|--------|
| **PRD Document** | **Structured Specs** | **Working Software** |
| Product vision | Phases, REQs, Tasks | Tested code |
| Goals & metrics | Decision records | Deployed features |
| *"What we want"* | *"How we'll build it"* | *"What we ship"* |

### Key Benefits

| Benefit | Description |
|---------|-------------|
| **Traceability** | Every line of code traces back to a requirement |
| **AI-Ready** | Specifications are optimized for AI agent consumption |
| **Decision Log** | All architectural choices are documented with rationale |
| **Progress Visibility** | Real-time status across phases, requirements, and tasks |
| **Reduced Ambiguity** | Questions are captured and resolved before coding |

---

## The Approach

> **"Specifications are the source of truth for both humans and AI agents."**

Traditional development often loses context between planning and implementation. Spec-Driven Development maintains a living documentation system that:

1. **Captures intent** — What are we building and why?
2. **Records decisions** — What choices did we make and why?
3. **Tracks progress** — Where are we and what's blocking us?
4. **Guides implementation** — What exactly should be built?

---

## The Information Hierarchy

| Level | Location | Contains | Purpose |
|-------|----------|----------|---------|
| 1 | `CLAUDE.md` | Project rules, constraints, key ADRs | Constitution |
| 2 | `.sdlc/context/` | Architecture, conventions, personas | Knowledge Base |
| 3 | `.sdlc/phases/` | PHASE-001, PHASE-002, ... | Delivery Roadmap |
| 4 | `.sdlc/specs/` | REQ-001/, REQ-002/, ... | Requirements |
| 5 | `.sdlc/specs/REQ-*/tasks/` | TASK-001, TASK-002, ... | Implementation |
| 6 | `src/` | Code + Tests | Deliverables |

**Flow:** Constitution → Context → Phases → Requirements → Tasks → Code

---

## Directory Structure

```
.sdlc/
├── context/           # Stable project knowledge
│   ├── architecture.md    # System design and topology
│   ├── conventions.md     # Coding standards
│   ├── workflow.md        # Process documentation
│   └── getting-started.md # Onboarding guide
├── phases/            # Delivery roadmap
│   └── PHASE-NNN-name/
│       └── phase.md
├── specs/             # Feature specifications
│   └── REQ-NNN-name/
│       ├── requirement.md # User stories, acceptance criteria
│       ├── design.md      # Technical approach
│       ├── contract.md    # API/interface definitions
│       └── tasks/         # Implementation units
├── adrs/              # Architecture Decision Records
│   └── ADR-NNN-title.md
├── decisions/         # Decision Requests
│   ├── open/          # Questions needing answers
│   └── closed/        # Resolved decisions
└── templates/         # Reusable document templates
```

---

## Artifact Types

### Requirements (REQ)

Define *what* to build with user stories and acceptance criteria. Each REQ lives in its own directory with supporting design docs and tasks.

### Tasks (TASK)

Define *how* to implement a requirement. Each task should be 1-2 hours of focused work with clear verification steps.

### Decision Requests (DR)

Capture questions that need answers. Tracked by priority:
- **Blocking** — Stops work entirely
- **High** — Affects upcoming work
- **Medium** — Should decide but doesn't block
- **Low** — Can wait

### Architecture Decision Records (ADR)

Document significant technical decisions with context, options considered, and rationale. Flow: Question (DR) → Decision made → Record (ADR)

---

## The Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SDLC WORKFLOW                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   1. ASSESS        2. UNBLOCK       3. SPECIFY       4. EXECUTE    │
│   ───────────      ───────────      ───────────      ───────────   │
│   /sdlc-status ──> /dr-review  ──>  /req-new    ──>  /task-new     │
│   (current state)  (blockers)       (new feature)    (break down)  │
│                                                            │       │
│                         ^                                  v       │
│                         │    <──────────────────────   Implement   │
│                         │    architectural decision?       │       │
│                    /adr-new  <─────────────────────────────┘       │
│                         │                                          │
│                         v                                          │
│                    /dr-new (if question arises)                    │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Step 1: Assess (`/sdlc-status`)
Check current state — requirements, blockers, recent activity.

### Step 2: Unblock (`/dr-review`)
Resolve blocking DRs before creating new work.

### Step 3: Specify (`/req-new`)
Define features with user stories and acceptance criteria.

### Step 4: Execute (`/task-new`)
Break requirements into actionable tasks, then implement.

---

## Skills Reference

| Skill | Purpose | Arguments |
|-------|---------|-----------|
| `/sdlc-status` | Show project status, progress, and blockers | `[phase or requirement]` |
| `/workflow` | Get workflow guidance for spec-driven development | `[next\|blockers\|start\|resume\|decision\|import]` |
| `/prd-import` | Import a PRD and create SDLC artifacts | `[path/to/prd.pdf or URL]` |
| `/phase-new` | Create a delivery phase for grouping requirements | `[Phase Name]` |
| `/req-new` | Create a Requirement spec | `[Feature Name] [--phase PHASE-NNN] [--minimal]` |
| `/task-new` | Create implementation tasks for a requirement | `[REQ-NNN] [Task Name] [--from-criteria] [--batch]` |
| `/dr-new` | Create a Decision Request | `[Question] [--priority blocking\|high\|medium\|low]` |
| `/dr-review` | Resolve open Decision Requests | `[DR-NNN] [--quick]` |
| `/adr-new` | Create an Architecture Decision Record | `[Decision Title] [--from-dr DR-NNN] [--status accepted]` |
| `/adr-review` | Review and accept/reject ADRs | `[ADR-NNN] [--accept] [--reject]` |
| `/adr-check` | Check if current work requires an ADR | `[description] [--from-task TASK-NNN]` |
| `/sdlc-report` | Generate this SDLC Framework report | `[--output PATH]` |

---

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Spec-First** | Write specifications before code. No implementation without a REQ. |
| **Traceable** | Every artifact links: Phase → REQ → Task → Code → Test |
| **Question-Driven** | Ambiguity is captured as DRs, not left to assumption |
| **Decision-Logged** | Architectural choices recorded with context and rationale |
| **AI-Optimized** | Consistent formats enable AI agents to read and write specs |

---

## Quick Start

### New Projects
```
/prd-import /path/to/prd.pdf    # Import PRD, create artifacts
/sdlc-status                     # Review generated structure
/task-new REQ-001                # Start implementing
```

### Existing Projects
```
/sdlc-status                     # See current state
/workflow next                   # Get recommended action
/dr-review                       # Address blockers
```

### During Work
```
/dr-new                          # Have a question? Capture it
/adr-new                         # Made a decision? Document it
/adr-check                       # Unsure if ADR needed? Check
/adr-review                      # Review proposed ADRs
```

---

## Current Project Status

| Metric | Value |
|--------|-------|
| Phases | 4 defined |
| Requirements | 4 specified |
| ADRs | 14 (13 accepted, 1 proposed) |
| Open DRs | 10 |
| Closed DRs | 2 |
| Current Phase | PHASE-001: CLI Scanner |

Run `/sdlc-status` for live dashboard.

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [CLAUDE.md](/CLAUDE.md) | Project constitution — rules and constraints |
| [.sdlc/context/workflow.md](/.sdlc/context/workflow.md) | Detailed workflow guide |
| [.sdlc/context/getting-started.md](/.sdlc/context/getting-started.md) | Onboarding guide |
| [.sdlc/adrs/README.md](/.sdlc/adrs/README.md) | Architecture decisions index |
| [.sdlc/decisions/README.md](/.sdlc/decisions/README.md) | Decision requests index |

---

*Generated by `/sdlc-report` on 2026-03-13*
