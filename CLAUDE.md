# CLAUDE.md

Repository conventions for `harvester` are documented in `AGENTS.md` at the repository
root — read it before working in this repo. It covers commands, code-review rules, and
merge policy.

In particular: **do not merge a pull request that has open, unresolved Codex review
threads**, regardless of CI status. Fix the underlying issue or dismiss the finding with a
written justification, then mark the thread resolved, before merging.

**Do not skip, disable, or weaken a test to get real work merged**, and do not bypass a
failing or required check (`--no-verify`, admin-merge override, etc.) to land real
feature/fix work. Fix the underlying issue instead.
