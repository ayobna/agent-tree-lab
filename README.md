# Agent Tree Lab

A small, deliberately broken Python project used as a sandbox for practicing
**nested Claude Code subagents**. The app itself (pagination, slugs, sessions,
listings) is intentionally simple — the point of this repository is the agent
tree that implements, checks, and reviews changes to it, not the app.

## Learning goal

Explore what happens when a single Claude Code session is decomposed into a
tree of narrowly scoped subagents — one agent per concern (implementation,
deterministic checks, correctness, security, test diagnosis) — instead of one
agent doing everything itself.

## Principle: evidence flows upward, not opinions

Every subagent in this tree is restricted to reporting concrete evidence:
exit codes, file:line references, concrete failing inputs, ruled-out
theories. None of them are allowed to just say "looks good" or "checks
passed" without the evidence backing it up. A parent agent only trusts what a
child hands back, not what the child claims about itself. This is enforced
by each agent's own instructions (see `.claude/agents/`), not by tooling.

## Project structure

```
.claude/agents/     Seven subagent definitions (see table below)
app/                 Small app under test
  __init__.py
  listing.py         Builds a page of {title, slug} items
  pagination.py      total_pages() / page_slice()
  session.py         Session/token creation with optional "remember me" TTL
  slug.py            Title -> URL-safe slug
issues/              Written briefs handed to code-implementer
  002-remember-me.md
  003-search-filter.md
tests/               pytest suite for app/
conftest.py
pyproject.toml       ruff + mypy configuration
README.md
```

## Subagents

| Agent | Responsibility | Tools |
|---|---|---|
| `code-implementer` | Makes one bounded code change from a brief and delegates verification instead of self-certifying. | Read, Write, Edit, Bash, Agent |
| `check-runner` | Runs ruff, mypy, and compileall exactly as instructed and reports exit codes. Does not fix or interpret anything. | Read, Bash |
| `test-runner` | Runs pytest and reports exact command, exit code, and pass/fail counts; spawns `failure-analyst` on failure. | Read, Bash, Agent |
| `failure-analyst` | Diagnoses failing tests from a clean context (only given failing test names and output) and reports root cause with file:line evidence. | Read, Grep, Glob |
| `independent-reviewer` | Reviews an issue and a diff without knowing how the diff was produced; forms an expectation first, then fans out to specialists. | Read, Grep, Glob, Agent |
| `correctness-reviewer` | Hunts logic errors, edge cases, and broken contracts; every finding names a concrete input and the wrong result. | Read, Grep, Glob |
| `security-reviewer` | Inspects security-sensitive code (tokens, sessions, secrets, auth, input handling) and reports concrete misuse scenarios. | Read, Grep, Glob |

## Demonstrated workflows

1. **Nested verification** — `code-implementer` makes a bounded change and
   is not allowed to declare success itself. It spawns `check-runner`
   (ruff, mypy, compileall) and reports the exact exit codes back, fixing
   and re-running the checks until they pass.

2. **Independent review with specialist fan-out** — `independent-reviewer`
   reads an issue and forms its own expectation of a correct change *before*
   reading the diff, then compares them. Depending on what the diff touches,
   it spawns `security-reviewer` (auth/sessions/tokens/secrets/input) and/or
   `correctness-reviewer` (logic/boundaries/edge cases), then merges their
   findings into one prioritized list.

3. **Conditional test-failure analysis** — `test-runner` runs the pytest
   suite. If everything passes it reports PASS and spawns nothing further.
   If tests fail, it spawns `failure-analyst` with only the failing test
   names and output, so the analyst reasons from a clean context and reports
   a root-cause diagnosis without ever touching the code.

## Setup (Windows, Git Bash)

Create and activate a virtual environment, then install the project's dev
dependencies (ruff, mypy, pytest) as declared in `pyproject.toml`:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install ruff mypy pytest
```

## Running the checks

Run these directly, or let `check-runner` / `test-runner` run them for you
inside a Claude Code session:

```bash
.venv/Scripts/python.exe -m ruff check .
.venv/Scripts/python.exe -m mypy app
.venv/Scripts/python.exe -m compileall -q app
.venv/Scripts/python.exe -m pytest -q
```

## Invoking the subagents in Claude Code

Inside a Claude Code session in this repository, ask for the top-level agent
that matches the workflow you want and let it spawn the rest of the tree:

```
Use the code-implementer subagent to work through issues/003-search-filter.md
Use the independent-reviewer subagent to review that diff against the issue
Use the test-runner subagent to run the suite and diagnose any failures
```

Each top-level agent (`code-implementer`, `independent-reviewer`,
`test-runner`) spawns its own children automatically per the rules in
`.claude/agents/`; you don't invoke the children directly.

### Example subagent tree

```
code-implementer
└── check-runner            (ruff, mypy, compileall)

independent-reviewer
├── security-reviewer        (spawned only if the diff touches auth/sessions/tokens)
└── correctness-reviewer     (spawned only if the diff touches logic/edge cases)

test-runner
└── failure-analyst          (spawned only on a failing test)
```

## Current test status

On `master`, as of this README:

| Check | Command | Result |
|---|---|---|
| Lint | `ruff check .` | Pass, no issues |
| Types | `mypy app` | Pass, no issues in 5 source files |
| Compile | `compileall -q app` | Pass |
| Tests | `pytest -q` | 14 passed |

## In-progress work

[PR #1](https://github.com/ayobna/agent-tree-lab/pull/1) is a draft adding an
optional search filter to `app.listing.list_page()` (see
`issues/003-search-filter.md`), built through the `code-implementer` /
`independent-reviewer` workflow described above. It is not yet merged; the
behavior it adds is not part of `master` and is not reflected in the test
status above.

## Limitations

This is an educational sandbox for practicing subagent decomposition, not
production code or a production agent framework:

- The app under test is intentionally minimal and not hardened for real use.
- The subagent contracts are enforced by prompt instructions, not by tooling
  or sandboxing, and can be violated by a model that doesn't follow them.
- There is no CI configured in this repository; the checks above are run
  manually or via the subagents themselves.
