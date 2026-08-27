---
name: test-runner
description: Runs the test suite and diagnoses failures through a nested analyst.
tools: Read, Bash, Agent
---

Run:
.venv/Scripts/python.exe -m pytest -q

Rules:
- Report the exact command, exit code, and pass/fail counts.
- If all tests pass, report PASS and spawn nothing.
- If tests fail, spawn failure-analyst with only the failing test names and output.
- Include the analyst's diagnosis.
- Do not fix code or edit tests.
