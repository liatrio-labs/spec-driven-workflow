# 01-audit-ai-techniques-deep-dive-page.md

## Executive Summary

- Overall Status: PASS
- Required Gate Failures: 0
- Flagged Risks: 0

## Gate Overview

| Gate | Status | Why it failed (<=10 words) | Exact fix target |
| --- | --- | --- | --- |
| Requirement-to-test traceability | PASS | - | - |
| Proof artifact verifiability | PASS | - | - |
| Repository standards consistency | PASS | - | - |
| Open question resolution | PASS | - | - |
| Regression-risk blind spots | PASS | - | - |
| Non-goal leakage | PASS | - | - |

## Standards Evidence Table (Required)

| Source File | Read | Standards Extracted | Conflicts |
| --- | --- | --- | --- |
| `AGENTS.md` | not found | - | none |
| `README.md` | yes | Use four-step workflow order; docs artifacts live in `docs/specs/`; docs site is static HTML with shared assets | none |
| `CONTRIBUTING.md` | yes | Keep changes small and focused; run `pre-commit`; follow Conventional Commits and keep docs consistent with `README.md` | none |
| `.github/pull_request_template.md` | yes | PRs use `Why/What Changed/Additional Notes`; link spec/task IDs; run tests and hooks before review | none |
| `.pre-commit-config.yaml` | yes | Pre-commit, pre-push, and commit-msg hooks are active; markdownlint fixes markdown; gitleaks scans committed content for secrets | none |
| `.github/workflows/ci.yml` | yes | CI runs `pre-commit run --all-files`; Python 3.12 is the documented runner baseline; workflow expects clean lint output | none |
| `.github/workflows/pr-title-lint.yml` | yes | PR titles must follow Conventional Commits; lowercase imperative subject is enforced; optional scopes are allowed | none |
| `package.json` | not found | - | none |
