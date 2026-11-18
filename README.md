# eco.wpr

LOCK33 Organization repository based on humanities' need for an authority to protect assets.

## What this is

eco.wpr is the LOCK33 Organization's asset protection recorder. It keeps
a ledger of assets — domains, accounts, devices, documents — with who
owns each one and where it stands: **protected**, **flagged** for review,
or **released**.

Every record gets a ledger ID (`ECO-0001`, `ECO-0002`, ...) when it is
opened, so any asset on the ledger can be referred to by that ID.

## Run it

Requires [Bun](https://bun.sh) (or any runtime that runs TypeScript).

```sh
bun run src/index.ts   # demo ledger
bun test               # test suite
```

## Layout

- `src/types.ts` — the AssetRecord shape
- `src/registry.ts` — the recorder: register, flag, release, look up, save/load
- `src/store.ts` — the wiring: fail-safe store and Pipeline log
- `src/index.ts` — a demo that opens a wired ledger and prints it
- `test/` — tests for the registry and the wiring

## Wiring

The registry can be wired two ways, following the ecosystem's design:

- **Fail-safe store** — lock33idsystem's role is the ecosystem's stored
  record: when something fails, you reproduce from it. `FileStore`
  stands in for it locally, keeping the whole ledger as one JSON file.
  Every change is saved as it happens, and a registry opened on a
  store that already holds a ledger rebuilds itself from that file.
- **LOCK33 Pipeline** — the connective layer between the domains.
  `PipeLog` stands in for it locally: every change to the ledger is
  written as one pipe message (a JSON line) that anything downstream
  can read.

Neither the Pipeline nor lock33idsystem has a live service yet, so
these are local stand-ins that follow the same pattern — when the
real services exist, the wiring points at them instead of files.

## Status

v0.2.0 — recorder working, wired to the local fail-safe store and
pipe log, 9 tests passing.

## Help

Questions and requests go through the LOCK33 Pipeline — see the help
section of any LOCK33 site, starting at https://lock33.org.
