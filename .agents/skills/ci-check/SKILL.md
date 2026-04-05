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

## Fixing Errors

After running each check:
1. If errors occur, **read the error output carefully**
2. **Fix the errors** using appropriate tools (Edit, Write)
3. **Re-run the failing check** to confirm the fix
4. **Continue to the next check** only after the current one passes

**Critical**: After fixing errors, re-run **pre-commit** again before declaring success, since code fixes may trigger formatting or schema changes.

## Common Error Types

- **Pre-commit failures**: Usually formatting, trailing whitespace, import sorting, or out-of-sync OpenAPI schemas
  - Re-run after auto-fixes; fix lint errors manually
  - The `ruff-format` hook auto-formats; `ruff-check` lint errors require manual fixes
  - The `export-openapi-schemas` and `generate-openapi-sdks` hooks auto-generate files — just re-run
- **Pyright errors**: Type checking issues
  - Add missing type annotations
  - Fix type mismatches
  - Check for undefined variables (e.g., missing function parameters)
- **Pytest/test failures**: Test failures
  - First, analyze whether the failure indicates a bug in the code or an outdated test
  - If the fix is obvious (e.g., a typo, missing import you just added), fix it
  - If unclear whether the code or test is "correct", **ask the user** before making changes
- **ESLint errors**: TypeScript linting issues
  - Fix code style, unused imports, etc.
  - **Do not add `eslint-disable` comments** to suppress errors—fix the underlying issues instead
  - If a rule seems incorrect for the codebase, ask the user rather than disabling it
  - JSDoc errors (missing `@param`, incomplete sentences) are common — check all parameters are documented
- **Build errors**: TypeScript compilation failures
  - Fix type errors, missing imports

## Reporting

After all checks complete:
1. Summarize results (pass/fail for each check)
2. List any remaining issues that need manual attention
3. Confirm whether the code is ready for commit

## Usage Examples

- `/ci-check` - Run all CI checks
- You can manually specify which checks to run by asking (e.g., "run only Python checks")
