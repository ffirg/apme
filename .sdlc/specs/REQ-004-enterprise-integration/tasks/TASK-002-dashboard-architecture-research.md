# TASK-002: Dashboard Architecture Research

## Parent Requirement

REQ-004: Enterprise Integration

## Status

Pending

## Description

Research and document architecture decisions for the enterprise dashboard. Evaluate tech stack options, deployment models, and integration patterns. Produce recommendations that resolve DR-003 (Dashboard Architecture) and inform DR-008 (Data Persistence).

## Prerequisites

- [ ] None (research task, can run in parallel with TASK-001)

## Implementation Notes

1. **Define evaluation criteria**
   - Deployment simplicity (single binary vs. multi-service)
   - Integration with existing gRPC architecture
   - Authentication/authorization needs
   - Scalability requirements
   - Development team familiarity

2. **Evaluate frontend options**
   - **Vue 3 + Vite**: Modern, lightweight, good DX
   - **React**: Large ecosystem, team familiarity
   - **HTMX + server templates**: Minimal JS, simpler deployment
   - **Streamlit**: Python-native, rapid prototyping

3. **Evaluate backend/API options**
   - **FastAPI**: Python, async, OpenAPI auto-docs
   - **Extend Primary gRPC**: Add REST gateway
   - **Separate service**: Dedicated dashboard backend

4. **Evaluate data persistence options** (feeds DR-008)
   - **SQLite**: Simple, file-based, good for single-node
   - **PostgreSQL**: Scalable, enterprise-ready
   - **No persistence**: Stateless, scan-on-demand only

5. **Evaluate deployment models**
   - Add to existing Podman pod
   - Separate container/service
   - Embedded in CLI (local dashboard)

6. **Document trade-offs**
   - Complexity vs. features
   - Development velocity vs. long-term maintainability
   - Enterprise requirements vs. OSS simplicity

## Deliverables

| Deliverable | Description |
|-------------|-------------|
| Architecture options doc | Comparison matrix of evaluated options |
| Recommended stack | Proposed tech stack with rationale |
| DR-003 resolution | Input to close Dashboard Architecture DR |
| DR-008 input | Recommendation for data persistence |
| ADR draft | Draft ADR for dashboard architecture |

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `.sdlc/research/dashboard-architecture.md` | Create | Research findings |
| `.sdlc/adrs/ADR-014-dashboard-architecture.md` | Create | Architecture decision |

## Verification

Before marking complete:

- [ ] Multiple frontend options evaluated with pros/cons
- [ ] Multiple backend options evaluated with pros/cons
- [ ] Persistence options documented (for DR-008)
- [ ] Deployment model recommended
- [ ] DR-003 can be resolved with findings
- [ ] ADR drafted or created

## Acceptance Criteria Reference

From REQ-004:
- [ ] Web Dashboard: aggregated metrics displayed
- [ ] Architecture supports "errors resolved" and "hours saved" metrics

## Related Artifacts

- DR-003: Dashboard Architecture (Medium priority)
- DR-008: Scan Result Persistence (Blocking)
- ADR-001: gRPC Communication (existing pattern)
- ADR-004: Podman Pod Deployment (deployment context)

## Notes

This is a foundational research task. The dashboard is Phase 3 work, but early architecture decisions will influence DR-003 and DR-008 resolution. Consider both MVP (simple, OSS-friendly) and enterprise (scalable, multi-tenant) scenarios.

---

## Completion Checklist

- [ ] Research complete
- [ ] Deliverables produced
- [ ] Status updated to Complete
- [ ] Committed with message: `Implements TASK-002: Dashboard architecture research`
