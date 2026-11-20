# eco.wpr test report

Branch: `ideal-spoon` (PR #2)

| Suite | Result |
|---|---|
| Bun (TypeScript) | 12 passed, 0 failed, 221 `expect()` calls, 3 files |
| Go (`gomod/ledgerid`) | 2 passed, 0 failed |

## Changes covered

- `test/loop.test.ts`: loop tests (100 sequential registrations, reload from the store).
- `test/registry.test.ts`: `get` returns `undefined` for an unknown ID.
- `gomod/`: Go module with `ledgerid.Format` and its tests.

## Reproduce

```
bun test
cd gomod && go test ./...
```
