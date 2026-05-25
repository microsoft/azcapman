# Sprint retrospectives

## Sprint 1 (2026-02-13)

- What worked
  - Kept requirements, traceability, and output location aligned across PRD, RTM, and TODO.
  - Used a consistent slide pattern (speaker notes structure and per-slide sources) across all five decks.
  - Finished QA checks (slide count and sources) as a discrete task instead of spreading it across deck work.
- What didn't
  - Repeated formatting work across decks increased review time.
  - Late-cycle consistency checks found small wording and casing drift that would've been cheaper to catch earlier.
- Action items
  - Add a lightweight template checklist for each new deck (title casing, prohibited words, and speaker notes sections).
  - Run a mid-sprint consistency pass across decks before final QA.
  - Keep RTM and TODO statuses current as tasks complete.

Sources: [PRD.md](PRD.md), [RTM.md](RTM.md), [TODO.md](TODO.md), and [AGENTS.md](AGENTS.md).

## Sprint 4 (2026-03-12)

- What worked
  - Parallel Wave execution (6 SWE agents in Wave 1) delivered all independent artifacts in under 6 minutes.
  - Reusing existing skill and agent content as source material for SRE Agent adaptation kept domain accuracy high — red-team found zero content accuracy issues.
  - Red-team audit caught 8 minor findings including a subagent naming mismatch (underscore vs hyphen) and an undocumented schema field (`enable_skills`) that would have risked load failure in production.
  - Single-commit remediation of all 8 findings kept the fix cycle fast and traceable.
  - Microsoft Learn citation density was strong (213 URLs across 5 content files) — no broken or placeholder URLs.
- What didn't
  - One SWE agent (T-23, README-plugin.md update) ran for 14+ minutes on a trivial edit and never completed. PM had to take over manually. Root cause unclear — possibly model-level instability or task prompt complexity mismatch.
  - Knowledge doc agents (T-21, T-22) took 3-6 minutes each — longer than the 60-120 second target. These tasks were borderline too large (comprehensive reference docs). Consider splitting by topic section next time.
  - The `enable_skills` field was included in the subagent YAML based on researcher notes, but the field isn't in the documented SRE Agent schema. Research findings need a confidence rating for schema claims.
- Action items
  - Set a 3-minute timeout for SWE agents. If an agent exceeds it, kill and reassign immediately rather than waiting 14 minutes.
  - Split knowledge docs into smaller topic-focused files (one per major section) rather than monolithic reference docs.
  - Add a "confidence: high/medium/low" annotation to researcher findings that claim specific schema fields or API behaviors, so downstream SWE agents know what to verify.
  - Validate YAML against SRE Agent's actual schema validator (if available) before red-team audit — catch structural issues early.

Sources: [PRD.md](PRD.md), [RTM.md](RTM.md), [TODO.md](TODO.md), and [AGENTS.md](AGENTS.md).

## Sprint 5 (2026-03-13)

- What worked
  - Hard-forking azure-sre-agent-sandbox provided production-quality Bicep IaC and deployment scripts in a single wave, avoiding from-scratch infrastructure work.
  - Mandating "read AGENTS.md first" in every subagent prompt resulted in clean style compliance for both Markdown docs (setup guide and prompts guide passed red-team with zero style findings).
  - Parallel Wave 1 (5 agents) completed all independent tasks in under 3 minutes per agent.
  - Red-team caught two critical findings (missing SRE Agent validation, wrong Log Analytics role) that would have caused real operational issues.
- What didn't
  - Forked scripts carried upstream assumptions that don't apply here: dead `k8s/` path reference in `deploy.ps1`, `kubectl config delete-context` with literal glob, `Invoke-Expression` on user input. These are low-severity but indicate forked code needs a security-focused scrub pass.
  - The RBAC script assigned "Log Analytics Contributor" instead of "Reader"—a least-privilege violation inherited from the upstream sandbox (which demos remediation and needs write access). Our capacity management use case is read-focused, so the upstream default was wrong for us.
  - Traceability comments were missing from all Bicep module files. The SWE agent added attribution but not T-* tags. Future prompts should explicitly list "traceability comment required in EVERY file" not just the entry point.
- Action items
  - Add a security scrub task to future fork sprints: review all `Invoke-Expression`, dead path references, and over-permissioned role assignments.
  - In fork tasks, require traceability comments in every file, not just the primary entry point.
  - Consider removing the dead `k8s/` reference from `deploy.ps1` in a follow-up since we didn't fork the k8s manifests.

Sources: [PRD.md](PRD.md), [RTM.md](RTM.md), [TODO.md](TODO.md), and [AGENTS.md](AGENTS.md).
