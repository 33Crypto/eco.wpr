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
- `src/index.ts` — a small demo that opens a ledger and prints it
- `test/` — tests for the registry

## Status

First implementation (v0.1.0). The registry works in memory and saves
or loads the whole ledger as JSON. Storage through the LOCK33 Pipeline
and connection to lock33idsystem, the ecosystem's fail-safe store, are
the next steps.

## Help

Questions and requests go through the LOCK33 Pipeline — see the help
section of any LOCK33 site, starting at https://lock33.org.
