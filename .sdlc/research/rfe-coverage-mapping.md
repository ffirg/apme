# RFE Coverage Mapping

**Created:** 2026-03-25
**Purpose:** Track external RFEs and their coverage by APME capabilities

---

## Coverage Status Legend

| Status | Meaning |
|--------|---------|
| **Covered** | APME already provides this capability |
| **Roadmap** | Planned APME feature will address |
| **Candidate** | Could be an APME feature (needs REQ) |
| **Out of Scope** | Not appropriate for APME |

---

## Covered by APME (8 RFEs)

These RFEs request functionality that APME already provides.

### AAPRFE-2515: Deprecation Warning Search

| Field | Value |
|-------|-------|
| **Summary** | Enable Searching for jobs that include deprecation warnings |
| **Status** | Backlog |
| **APME Coverage** | **M002** (deprecated modules), **M004** (tombstoned modules), **L004** (OPA deprecated check) |
| **How APME Addresses** | APME's modernization rules detect deprecated modules at scan time. CLI `apme scan --json` outputs violations with rule IDs and metadata. Customers can filter by M002/M004 rules to identify content with deprecation issues before runtime. |
| **Gap** | APME is static analysis (pre-runtime). The RFE asks for runtime job search in Controller UI. APME provides the detection; surfacing in Controller would require integration. |
| **Action** | Link to APME; note static vs runtime distinction |

---

### AAPRFE-2472: Native Playbook Sanity Command

| Field | Value |
|-------|-------|
| **Summary** | Add native ansible sanity command for playbook validation |
| **Status** | Closed |
| **APME Coverage** | **L057** (syntax validation), **L058-L059** (argspec validation), **L002** (FQCN), plus 100+ lint rules |
| **How APME Addresses** | `apme scan` provides comprehensive playbook validation: YAML syntax, deprecated modules, undefined variables, module argument validation, best practices. This is exactly what the RFE requests. |
| **Gap** | None — APME is the implementation of this request |
| **Action** | Close with reference to APME |

---

### AAPRFE-2313: Linting Problems Noted in UI

| Field | Value |
|-------|-------|
| **Summary** | Rulebooks/playbooks with linting problems should be noted |
| **Status** | Closed |
| **APME Coverage** | Full ansible-lint rule coverage (L-series rules) |
| **How APME Addresses** | APME detects linting issues and provides structured output. Integration with Controller/EDA UI would surface these issues where the RFE requests. |
| **Gap** | APME provides detection; UI integration is a separate concern (see REQ-004 Enterprise Integration) |
| **Action** | Link to APME; track UI integration separately |

---

### AAPRFE-2374: var-naming Rule Collision

| Field | Value |
|-------|-------|
| **Summary** | ansible-lint collision between var-naming[no-role-prefix] and var-naming[pattern] |
| **Status** | Backlog |
| **APME Coverage** | Inherits ansible-lint rules; APME contributes upstream fixes |
| **How APME Addresses** | This is an upstream ansible-lint issue ([#4142](https://github.com/ansible/ansible-lint/issues/4142)). APME inherits ansible-lint rules and will automatically get the fix when merged upstream. |
| **Gap** | Upstream issue — not an APME-specific feature |
| **Action** | Track upstream; APME inherits fix automatically |

---

### AAPRFE-2059: Skip YAML Rules in ansible-lint

| Field | Value |
|-------|-------|
| **Summary** | Allow ansible-lint to skip `yaml` rules while still fixing other rules |
| **Status** | Closed |
| **APME Coverage** | Rule exclusion configuration |
| **How APME Addresses** | APME supports rule exclusion via configuration. Users can skip specific rules while still running others. The OPA validator also supports per-rule configuration. |
| **Gap** | None — APME supports this |
| **Action** | Close with reference to APME configuration |

---

### AAPRFE-1628: Smart ansible-galaxy Version Decisions

| Field | Value |
|-------|-------|
| **Summary** | ansible-galaxy should make smart decisions regarding ansible-core and collection versions |
| **Status** | Release Pending |
| **APME Coverage** | **M005-M013** (migration rules), version compatibility analysis |
| **How APME Addresses** | APME's migration rules analyze `requires_ansible` constraints and detect version incompatibilities. The scan identifies collections that won't work with the target ansible-core version. |
| **Gap** | APME provides analysis/detection; ansible-galaxy handles installation. These are complementary. |
| **Action** | Link to APME for analysis capability |

---

### AAPRFE-1607: Deprecated Module Reports in Analytics

| Field | Value |
|-------|-------|
| **Summary** | Report in Automation Analytics showing deprecated module usage |
| **Status** | Closed |
| **APME Coverage** | **M002** (deprecated), **M004** (tombstoned), **L004** (OPA deprecated check) |
| **How APME Addresses** | APME detects deprecated modules with full metadata (module name, replacement, deprecation version). Output available via gRPC and CLI JSON. |
| **Gap** | Integration with Automation Analytics (runtime vs static distinction). See **DR-013** for integration approach. |
| **SDLC Artifacts** | REQ-011, DR-013 (created but may be reframed per review feedback) |
| **Action** | Already tracked; pending decision on scope |

---

### AAPRFE-2376: ansible-policy Rego Documentation

| Field | Value |
|-------|-------|
| **Summary** | Enhance ansible-policy docs with clearer Rego syntax mapping |
| **Status** | Closed |
| **APME Coverage** | OPA/Rego validator with documentation |
| **How APME Addresses** | APME includes a full OPA validator with Rego policy support. The `.sdlc/context/` directory contains design documentation for policy authoring. Example policies in the OPA bundle demonstrate Rego v1 syntax. |
| **Gap** | Documentation could be expanded with more examples |
| **Action** | Close; consider docs enhancement task |

---

## Aligned with APME Roadmap (6 RFEs)

These RFEs will be addressed by planned APME features (R505-R507 EE compatibility rules, M005-M013 migration rules).

### AAPRFE-2552: Collection Version Range for Cisco Gear

| Field | Value |
|-------|-------|
| **Summary** | Add version range to collections for cisco gear |
| **Status** | Backlog |
| **APME Roadmap** | **R505-R507** (EE compatibility checks), collection dependency analysis |
| **How APME Will Address** | APME's planned EE compatibility rules will analyze collection metadata including tested versions, `requires_ansible`, and platform compatibility. This enables validation of collection compatibility with specific network OS versions. |
| **Timeline** | Planned for Phase 3 (Enterprise Dashboard) |
| **Action** | Track; will be addressed by R505-R507 |

---

### AAPRFE-2551: Compatible OS Version Range

| Field | Value |
|-------|-------|
| **Summary** | Looking for a range of compatible OS versions |
| **Status** | Backlog |
| **APME Roadmap** | **R505** (EE base image compatibility) |
| **How APME Will Address** | Related to AAPRFE-2552. APME's EE compatibility analysis will include platform/OS version compatibility checking based on collection metadata and runtime requirements. |
| **Timeline** | Planned for Phase 3 (Enterprise Dashboard) |
| **Action** | Track; will be addressed by R505 |

---

### AAPRFE-2664: AAP 2.6 EEs on RHEL 10

| Field | Value |
|-------|-------|
| **Summary** | Provide AAP2.6 EEs (Supported and Minimal) based on RHEL 10 image |
| **Status** | Backlog |
| **APME Roadmap** | **R505** (EE base image compatibility), **R507** (Python version compatibility) |
| **How APME Will Address** | APME's EE validation rules will check base image compatibility, Python version requirements (3.12+), and collection compatibility with RHEL 10 ecosystem. This helps customers validate their content works with new EE images. |
| **Timeline** | Planned for Phase 3; depends on RHEL 10 EE availability |
| **Action** | Track; APME validates content compatibility with new EEs |

---

### AAPRFE-2580: Zero-CVE EE Base Images

| Field | Value |
|-------|-------|
| **Summary** | Base ee-supported-* images on zero-CVE images (Project Hummingbird) |
| **Status** | Backlog |
| **APME Roadmap** | **R506** (EE system package compatibility), security scanning integration |
| **How APME Will Address** | APME's EE analysis can validate that EE images meet security requirements. While APME doesn't build images, it can flag EE configurations that may introduce CVE risks (e.g., pinned vulnerable package versions). |
| **Timeline** | Planned for Phase 3 |
| **Action** | Track; APME provides content-level security analysis |

---

### AAPRFE-2739: Python 3.11 to 3.12 for EE

| Field | Value |
|-------|-------|
| **Summary** | Update python3.11 to python3.12 for execution environment in AAP 2.5/2.6 |
| **Status** | Closed |
| **APME Roadmap** | **R507** (EE Python package compatibility), Python version rules |
| **How APME Will Address** | APME's planned Python version compatibility rules will detect content that requires specific Python versions or uses syntax/libraries incompatible with Python 3.12. This helps validate playbooks work with upgraded EEs. |
| **Timeline** | In progress (M005-M013 partially cover this) |
| **Action** | Closed in Jira; APME validates content compatibility |

---

### AAPRFE-2070: DNF Module with Newer Python

| Field | Value |
|-------|-------|
| **Summary** | DNF module broken with newer python versions |
| **Status** | Release Pending |
| **APME Roadmap** | **M005-M013** (migration rules), Python/module compatibility |
| **How APME Will Address** | APME's migration rules detect module compatibility issues across ansible-core versions. The DNF module's Python version requirements are part of this analysis. APME can flag playbooks using `ansible.builtin.dnf` with incompatible Python configurations. |
| **Timeline** | In progress |
| **Action** | Release Pending in Jira; APME detects compatibility issues |

---

## Summary: Covered RFEs

| RFE | APME Rules | Status | Action |
|-----|-----------|--------|--------|
| AAPRFE-2515 | M002, M004, L004 | Covered | Link (note static vs runtime) |
| AAPRFE-2472 | L057, L058-L059, L002 | Covered | Close |
| AAPRFE-2313 | L-series (all) | Covered | Link (UI integration separate) |
| AAPRFE-2374 | (upstream) | Covered | Track upstream |
| AAPRFE-2059 | (config) | Covered | Close |
| AAPRFE-1628 | M005-M013 | Covered | Link |
| AAPRFE-1607 | M002, M004, L004 | Covered | REQ-011/DR-013 exist |
| AAPRFE-2376 | OPA validator | Covered | Close (docs task optional) |

## Summary: Roadmap RFEs

| RFE | APME Roadmap | Status | Timeline |
|-----|-------------|--------|----------|
| AAPRFE-2552 | R505-R507 | Roadmap | Phase 3 |
| AAPRFE-2551 | R505 | Roadmap | Phase 3 |
| AAPRFE-2664 | R505, R507 | Roadmap | Phase 3 |
| AAPRFE-2580 | R506 | Roadmap | Phase 3 |
| AAPRFE-2739 | R507 | Roadmap | In progress |
| AAPRFE-2070 | M005-M013 | Roadmap | In progress |

---

## APME Candidates (12 RFEs)

These RFEs were labeled as candidates but require research to determine if they fit APME's scope (static code analysis).

### Analysis Summary

| RFE | Summary | APME Fit | Recommendation |
|-----|---------|----------|----------------|
| AAPRFE-2642 | EDA rulebook validation | **Yes** | Create REQ (E-series rules) |
| AAPRFE-2545 | Expand OPA inputs | **Yes** | Create REQ (policy input schema) |
| AAPRFE-2258 | Policy permissive mode | **Yes** | Create REQ (warn-only mode) |
| AAPRFE-2218 | EE signing status | **Partial** | Track (R509 validation rule) |
| AAPRFE-1689 | EE image field validation | **Partial** | Track (R510, already Closed) |
| AAPRFE-2791 | Collection migration playbook | No | Content request, not analysis |
| AAPRFE-2627 | Monitor parsing tasks | No | Platform feature |
| AAPRFE-2432 | Front-end input validation | No | Platform UI feature |
| AAPRFE-2310 | Input sanitization in AAP | No | Platform security feature |
| AAPRFE-2233 | Strong password policy | No | Platform security feature |
| AAPRFE-2205 | Rulebook job_args by name | No | EDA/Controller API feature |
| AAPRFE-2175 | Versionless EE image | No | Container registry issue |

---

### Genuine APME Candidates (3 RFEs → New REQs)

#### AAPRFE-2642: EDA Rulebook Validation (HIGH PRIORITY)

| Field | Value |
|-------|-------|
| **Summary** | Improve visibility for rulebook validation failures in EDA |
| **Status** | Backlog |
| **APME Fit** | **Yes** — Static validation of rulebook content |
| **Proposed Feature** | New rule category: **E-series** (EDA rules) |
| **Proposed Rules** | E001: Rulebook YAML syntax, E002: Action reference validation, E003: Source plugin validation |
| **Why APME** | APME already validates playbooks; extending to rulebooks is natural. Structured output enables UI integration. |
| **Action** | **Create REQ-012: EDA Rulebook Validation** |

---

#### AAPRFE-2545: Expand OPA Policy Inputs (HIGH PRIORITY)

| Field | Value |
|-------|-------|
| **Summary** | Expand OPA inputs to include playbook content |
| **Status** | Backlog |
| **APME Fit** | **Yes** — APME already parses playbooks for OPA |
| **Proposed Feature** | Extended policy input schema with parsed playbook content |
| **Current State** | APME's OPA validator receives parsed AST. RFE asks for richer input (task list, module calls, variable refs). |
| **Why APME** | APME's tree parser already extracts this data; exposing it to OPA policies is straightforward. |
| **Action** | **Create REQ-013: Extended OPA Policy Input Schema** |

---

#### AAPRFE-2258: Policy Permissive Mode

| Field | Value |
|-------|-------|
| **Summary** | Add permissive/warn-only mode for policy enforcement |
| **Status** | Backlog |
| **APME Fit** | **Yes** — Policy execution mode is APME configuration |
| **Proposed Feature** | Warn-only mode that logs violations without blocking |
| **Use Case** | Gradual policy rollout (like SELinux permissive mode) |
| **Why APME** | APME already has severity levels; adding enforcement modes extends this naturally. |
| **Action** | **Create REQ-014: Policy Permissive Mode** |

---

### Borderline Candidates (2 RFEs → Track on Roadmap)

#### AAPRFE-2218: EE Image Signing Status

| Field | Value |
|-------|-------|
| **Summary** | Indicate signing status per EE image tag in Hub |
| **Status** | Backlog |
| **APME Fit** | **Partial** — Validation rule possible, UI is Hub concern |
| **Proposed Rule** | **R509**: EE signing verification (check if image ref is signed) |
| **Gap** | APME can validate EE references in playbooks; signing status requires registry API. |
| **Action** | Track as roadmap item (R509) |

---

#### AAPRFE-1689: EE Image Field Validation

| Field | Value |
|-------|-------|
| **Summary** | Validate EE image field on creation |
| **Status** | Closed |
| **APME Fit** | **Partial** — APME can validate EE references in content |
| **Proposed Rule** | **R510**: EE image reference validation |
| **Gap** | RFE is about Controller UI; APME validates content, not UI forms. |
| **Action** | Track as roadmap item (R510); already Closed |

---

### Out of Scope (7 RFEs)

These RFEs don't fit APME's mission (static code analysis). Keep in AAP backlog.

| RFE | Summary | Reason Out of Scope |
|-----|---------|---------------------|
| AAPRFE-2791 | Collection migration playbook for rhel_idm | Content request, not analysis tool |
| AAPRFE-2627 | Monitor parsing tasks from Dashboard | Platform operations feature |
| AAPRFE-2432 | Front-end input validation | Platform UI feature (OWASP compliance) |
| AAPRFE-2310 | Input sanitization in AAP | Platform security feature |
| AAPRFE-2233 | Strong password policy | Platform authentication feature |
| AAPRFE-2205 | Rulebook job_args by name | EDA/Controller API feature |
| AAPRFE-2175 | Versionless EE image missing | Container registry/catalog issue |

---

## Summary Tables

### Covered RFEs (8)

| RFE | APME Rules | Status | Action |
|-----|-----------|--------|--------|
| AAPRFE-2515 | M002, M004, L004 | Covered | Link (note static vs runtime) |
| AAPRFE-2472 | L057, L058-L059, L002 | Covered | Close |
| AAPRFE-2313 | L-series (all) | Covered | Link (UI integration separate) |
| AAPRFE-2374 | (upstream) | Covered | Track upstream |
| AAPRFE-2059 | (config) | Covered | Close |
| AAPRFE-1628 | M005-M013 | Covered | Link |
| AAPRFE-1607 | M002, M004, L004 | Covered | REQ-011/DR-013 exist |
| AAPRFE-2376 | OPA validator | Covered | Close (docs task optional) |

### Roadmap RFEs (6)

| RFE | APME Roadmap | Status | Timeline |
|-----|-------------|--------|----------|
| AAPRFE-2552 | R505-R507 | Roadmap | Phase 3 |
| AAPRFE-2551 | R505 | Roadmap | Phase 3 |
| AAPRFE-2664 | R505, R507 | Roadmap | Phase 3 |
| AAPRFE-2580 | R506 | Roadmap | Phase 3 |
| AAPRFE-2739 | R507 | Roadmap | In progress |
| AAPRFE-2070 | M005-M013 | Roadmap | In progress |

### Candidate RFEs (12)

| RFE | APME Fit | Action |
|-----|----------|--------|
| AAPRFE-2642 | Yes | **REQ-012** (EDA validation) ✅ Created |
| AAPRFE-2545 | Yes | **REQ-013** (OPA inputs) ✅ Created |
| AAPRFE-2258 | Yes | **REQ-014** (permissive mode) ✅ Created |
| AAPRFE-2218 | Partial | Track (R509) |
| AAPRFE-1689 | Partial | Track (R510, Closed) |
| AAPRFE-2791 | No | Out of scope |
| AAPRFE-2627 | No | Out of scope |
| AAPRFE-2432 | No | Out of scope |
| AAPRFE-2310 | No | Out of scope |
| AAPRFE-2233 | No | Out of scope |
| AAPRFE-2205 | No | Out of scope |
| AAPRFE-2175 | No | Out of scope |

---

## Change History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-25 | Phil (AI-assisted) | Initial mapping of 8 covered RFEs |
| 2026-03-25 | Phil (AI-assisted) | Added 6 roadmap RFEs (R505-R507, M005-M013) |
| 2026-03-25 | Phil (AI-assisted) | Analyzed 12 candidate RFEs; identified 3 for new REQs |
