// eco.wpr — storage and Pipeline wiring.
//
// lock33idsystem is the ecosystem's fail-safe store: when something
// fails, you reproduce from it. FileStore is that store's local stand-in
// — it keeps the whole ledger as one JSON file, so the ledger can
// always be rebuilt from the file alone.
//
// The LOCK33 Pipeline is the connective layer between the domains.
// PipeLog is its local stand-in: every change to the ledger is written
// as one pipe message (a JSON line) that anything downstream can read.

import { appendFileSync, existsSync, readFileSync, writeFileSync } from "node:fs";

export interface LedgerStore {
  /** The stored ledger JSON, or null when nothing is stored yet. */
  load(): string | null;
  /** Store the ledger JSON, replacing what was there. */
  save(data: string): void;
}

export class FileStore implements LedgerStore {
  constructor(private path: string) {}

  load(): string | null {
    if (!existsSync(this.path)) return null;
    return readFileSync(this.path, "utf8");
  }

  save(data: string): void {
    writeFileSync(this.path, data, "utf8");
  }
}

export interface PipeMessage {
  at: string;
  type: string;
  detail: string;
}

export class PipeLog {
  constructor(private path: string) {}

  /** Send one message down the pipe. */
  send(type: string, detail: string): void {
    const message: PipeMessage = {
      at: new Date().toISOString(),
      type,
      detail,
    };
    appendFileSync(this.path, JSON.stringify(message) + "\n", "utf8");
  }

  /** Every message sent so far, oldest first. */
  read(): PipeMessage[] {
    if (!existsSync(this.path)) return [];
    return readFileSync(this.path, "utf8")
      .split("\n")
      .filter((line) => line.trim() !== "")
      .map((line) => JSON.parse(line) as PipeMessage);
  }
}
