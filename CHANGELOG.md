# Changelog

All notable changes to APME (Ansible Policy & Modernization Engine) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Policy library adapter framework for consuming external Rego policy libraries (DR-017)
- Extended OPA policy input schema for cross-node task/variable/role access (REQ-013)

## [0.1.0] - 2026-04-16

### Added

- Multi-validator static analysis engine with parallel fan-out
- Four validator backends: Native (Python), OPA (Rego), Ansible (runtime), Gitleaks (secrets)
- 100+ rules across L (lint), M (modernize), R (risk), P (policy), SEC (secrets) categories
- gRPC inter-service communication (ADR-001)
- Galaxy Proxy for collection-to-wheel conversion (PEP 503/427)
- Session-scoped venvs with multi ansible-core version support
- YAML formatter with `--diff`, `--apply`, `--check` modes
- Remediate pipeline with Tier 1 deterministic transforms
- AI-assisted remediation via Abbenay integration (opt-in)
- Web UI (React) with Gateway API for project management
- Dependency health scanning (collection health + Python CVE audit)
- Secret scanning with 800+ Gitleaks patterns
- Podman pod deployment model (9 containers)
- CLI with `check`, `format`, `remediate`, `health-check` commands

### Architecture

- Primary orchestrator with parse/annotate/fan-out/aggregate pipeline
- Unified `Validator` gRPC service contract for all backends
- Gateway with REST + SSE for UI integration
- SQLite persistence for projects, scans, and findings

[Unreleased]: https://github.com/ansible/apme/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ansible/apme/releases/tag/v0.1.0
