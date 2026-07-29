# AGENTS.md

Repository conventions for `harvester` (a Python/FastAPI lead-generation pipeline, with a
Vite/React frontend under `frontend/`).

## Commands

- Backend install: `python -m venv .venv && .venv/bin/pip install -e ".[dev]"`
- Lint: `ruff check .` (fix with `ruff check --fix .`)
- Format: `ruff format .` (check only with `ruff format --check .`)
- Tests: `pytest -q`
- Dependency audit: `pip-audit --skip-editable`
- Pre-commit hooks: `pre-commit install` (runs ruff lint/format on staged Python files,
  oxlint/prettier on staged frontend files automatically on `git commit`)
- Frontend: `cd frontend && npm ci`, then `npm run lint` (oxlint), `npm run build`
  (tsc + vite), `npx prettier --check "src/**/*.{ts,tsx,css}"`

CI (`.github/workflows/ci.yml`) runs all of the above on every push/PR, plus a Postgres+PostGIS
service container for the backend test suite and a Semgrep static-analysis scan.

## Code Review Rules

- **Do not merge a pull request that has open, unresolved Codex review threads**,
  regardless of CI status. Fix the underlying issue or dismiss the finding with a written
  justification, then mark the thread resolved, before merging.
- **Do not skip, disable, or weaken a test to get real work merged**, and do not bypass a
  failing or required check (`--no-verify`, admin-merge override, etc.) to land real
  feature/fix work. Fix the underlying issue instead.
- **No secrets, credentials, or tokens in diffs.** Flag anything that looks like an API
  key, password, or private token, including in workflow YAML, `.env` examples, or
  documentation.
- **Prefer existing conventions over new patterns.** This codebase already has established
  patterns for exception handling (log at the boundary, don't crash the pipeline — see
  `pyproject.toml`'s `[tool.ruff.lint]` comments for the reasoning), config (flat
  `pydantic_settings.BaseSettings` attributes in `config.py`), and migrations (staged
  nullable-then-backfill-then-not-null for any new required column on a table that may
  already have rows).

## Merge Policy

- **Every Codex review finding must be resolved before a pull request merges.** "Resolved"
  means either the underlying issue is fixed and the review thread marked resolved, or the
  finding is dismissed with a written justification (e.g. a false positive) and the thread
  marked resolved. A pull request with open, unaddressed Codex review threads must not
  merge, regardless of CI status. This applies to every severity level Codex reports, not
  only the highest-priority findings.
- **No test may be skipped, disabled, or weakened to get real work merged.** Do not mark a
  test skipped/xfail, comment it out, delete its assertions, or otherwise make it stop
  exercising the behavior it covers, in order to get a pull request to a passing state. If
  a test is failing, fix the underlying issue. Do not bypass a failing or required check
  with `--no-verify`, an admin-merge override, or similar, to land real feature/fix work —
  a pull request only merges once its own tests and checks are genuinely green.
