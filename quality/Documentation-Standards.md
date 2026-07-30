# Documentation Standards

## API Documentation

Every public API must have:

1. **Purpose**: What it does (one sentence).
2. **Signature**: TypeScript signature with types.
3. **Description**: What it does (one paragraph).
4. **Parameters**: Each parameter documented.
5. **Return value**: Documented with type.
6. **Examples**: At least one working example.
7. **Errors**: All possible errors listed.
8. **Version**: When it was introduced.

## File Documentation

Every source file should have:

```typescript
/**
 * Plugin Manager
 *
 * Handles plugin discovery, loading, activation, and lifecycle.
 * Plugins are loaded from the plugin directory and sandboxed.
 *
 * @module plugin-manager
 * @since 0.1
 */
```

## Function Documentation

```typescript
/**
 * Executes Scilab code.
 *
 * Sends the code to the Scilab runtime and waits for the result.
 * The code is evaluated asynchronously. If the execution takes
 * longer than the timeout, it is interrupted.
 *
 * @param code - The Scilab code to execute
 * @param options - Execution options
 * @returns The execution result including output and variables
 * @throws {RuntimeNotReady} If the runtime is not ready
 * @throws {ExecutionTimeout} If execution exceeds the timeout
 *
 * @example
 * ```typescript
 * const result = await runtime.execute('x = sin(0:0.1:10)');
 * console.log(result.variables.x); // { type: "matrix", rows: 101, cols: 1 }
 * ```
 *
 * @since 0.1
 */
async function execute(code: string, options?: ExecuteOptions): Promise<ExecuteResult>
```

## README Files

Every directory should have a README:

```markdown
# Directory Name

Brief description of what this directory contains.

## Contents

- `file1.ts` — Description
- `file2.ts` — Description

## Usage

How to use these files.
```

## Changelog

Every version change must be documented:

```markdown
## [1.0.0] - 2025-01-15

### Added
- New feature X

### Changed
- Feature Y behavior

### Fixed
- Bug in Z

### Removed
- Deprecated feature W
```

## Rules

- All documentation in English.
- Use present tense.
- Be concise.
- Include code examples.
- Keep documentation up to date with code changes.
