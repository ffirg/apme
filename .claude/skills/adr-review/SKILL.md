---
name: adr-review
description: >-
  Review and accept/reject Architecture Decision Records. Use when reviewing
  proposed ADRs, "accept ADR-014", "review the proposed ADRs", or when
  `/sdlc-status` shows Proposed ADRs. Do NOT use for creating ADRs (use
  adr-new instead) or checking if work needs an ADR (use adr-check instead).
argument-hint: "[ADR-NNN] [--accept] [--reject]"
user-invocable: true
disable-model-invocation: true
metadata:
  author: APME Team
  version: 1.0.0
---

# ADR Review

Review and update status of Architecture Decision Records.

## Arguments

If `$ARGUMENTS` is provided, parse for:
- `ADR-NNN` -> review that specific ADR
- `--accept` -> accept without prompts (quick mode)
- `--reject` -> reject and prompt for reason

If no argument, list Proposed ADRs and prompt for selection.

## Usage

```
/adr-review                 # List Proposed ADRs, select one
/adr-review ADR-014         # Review specific ADR
/adr-review ADR-014 --accept  # Quick accept
/adr-review ADR-014 --reject  # Reject with reason
```

## Behavior

### 1. List Proposed ADRs

Scan `.sdlc/adrs/ADR-*.md` for Status: Proposed and present:

```
Found N ADRs pending review:

| ADR | Title | Date |
|-----|-------|------|
| ADR-014 | CLI Output Formats | 2026-03 |
...

Which ADR to review? (number or "all" for batch review)
```

**Empty state:** "No ADRs pending review. All decisions finalized!"

### 2. Present ADR Summary

Read the selected ADR file and present:
- **Title**: ADR title
- **Context**: Why this decision was needed (2-3 sentences)
- **Decision**: What was decided
- **Consequences**: Key positive/negative outcomes
- **Alternatives**: Brief list of rejected options

### 3. Facilitate Review

```
Decision for ADR-NNN: [Title]

1. Accept - Finalize this architectural decision
2. Reject - Decline with rationale
3. Request Changes - Keep Proposed, note feedback
4. Supersede - Replace with different ADR
S. Skip - Review later
```

**On Accept:**
- Update Status: Proposed -> Accepted
- Record acceptance date
- Optionally record reviewer notes

**On Reject:**
- Ask for rejection reason
- Update Status: Proposed -> Rejected
- Record rejection rationale in ADR

**On Request Changes:**
- Ask for feedback/changes needed
- Keep Status: Proposed
- Add feedback to ADR as review comments

**On Supersede:**
- Ask which ADR supersedes this one
- Update Status: Proposed -> Superseded
- Add "Superseded by ADR-NNN" reference

### 4. Update ADR File

Update the ADR file in place:
- `Status:` -> new status
- Add `Reviewed:` date (for Accepted/Rejected)
- Add `Reviewer Notes:` section if provided
- For Rejected: add `Rejection Reason:` section
- For Superseded: add `Superseded By:` reference

Preserve existing file format - only update relevant sections.

### 5. Update README Index

Edit `.sdlc/adrs/README.md`:
- Update status in Index table
- If Superseded, move to Archived section

### 6. Summary & Continue

```
Done! ADR-014 accepted.
- Status: Proposed -> Accepted
- README updated

Review another ADR? (Y/n or ADR number)
```

**If "Y" or number:** Loop back to step 2/1
**If "n":** Show remaining count: "N ADRs still pending review"

## Quick Mode

With `--accept` flag:
1. Show ADR title and decision summary
2. Update status to Accepted
3. Skip prompts

With `--reject` flag:
1. Show ADR title and decision summary
2. Prompt for rejection reason (required)
3. Update status to Rejected

## Batch Mode

With "all" selection:
1. Present each Proposed ADR in sequence
2. For each, show summary and ask Accept/Reject/Skip
3. At end, summarize: "Accepted N, Rejected M, Skipped K"

## Status Transitions

| From | To | Trigger |
|------|-----|---------|
| Proposed | Accepted | Review approval |
| Proposed | Rejected | Review rejection |
| Proposed | Superseded | Replaced by another ADR |
| Accepted | Superseded | Later decision replaces |
| Accepted | Deprecated | No longer applies |

## Edge Cases

| Situation | Handling |
|-----------|----------|
| ADR already Accepted | Show current status, ask if re-review needed |
| ADR already Rejected | Show rejection reason, ask if reconsider |
| ADR not found | Error with suggestion to check number |
| No Proposed ADRs | "All ADRs finalized!" message |
| Superseding ADR doesn't exist | Warn and ask to create it first |

## File Changes

For accepted ADR-014:
```markdown
## Status

Accepted

## Reviewed

2026-03-13
```

For rejected ADR-014:
```markdown
## Status

Rejected

## Reviewed

2026-03-13

## Rejection Reason

[User-provided rationale]
```
