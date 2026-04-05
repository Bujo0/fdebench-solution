---
name: ci-check
description: Run all CI pipeline checks locally and fix any errors that appear.
---

# CI Check and Fix

Run all CI pipeline checks locally and fix any errors that appear.

## Instructions

You should run the following checks in order, matching what runs in `.github/workflows/ci.yml`.

**Note**: The CI workflow file (`.github/workflows/ci.yml`) is the source of truth.

### 1. Pre-commit Checks
```bash
uvx pre-commit run --all-files
```

**Important**: Some hooks auto-fix files (e.g., `ruff-format`). If hooks modify files, **re-run pre-commit** until all hooks pass cleanly with no modifications.

### 2. TypeScript Checks
```bash
cd ts
pnpm install --frozen-lockfile
pnpm build-all
pnpm fix-eslint-all
pnpm test-all
```
