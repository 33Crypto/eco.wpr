// eco.wpr — the asset protection registry.
//
// The registry is the recorder: it opens a record for each asset,
// tracks its standing, and answers lookups. Records are kept in
// memory; save()/load() move them in and out as plain JSON so the
// ledger can be stored anywhere.

import type { AssetRecord, AssetStatus, NewAsset } from "./types";

export class AssetRegistry {
  private records: AssetRecord[] = [];
  private nextNumber = 1;

  /** Open a protection record for an asset. Returns the new record. */
  register(input: NewAsset): AssetRecord {
    const record: AssetRecord = {
      id: `ECO-${String(this.nextNumber).padStart(4, "0")}`,
      owner: input.owner,
      asset: input.asset,
      kind: input.kind,
      registeredAt: new Date().toISOString(),
      status: "protected",
      note: input.note ?? "",
    };
    this.nextNumber += 1;
    this.records.push(record);
    return record;
  }

  /** Change a record's standing, with a note saying why. */
  setStatus(id: string, status: AssetStatus, note = ""): AssetRecord {
    const record = this.get(id);
    if (!record) {
      throw new Error(`No asset record with id ${id}`);
    }
    record.status = status;
    if (note) record.note = note;
    return record;
  }

  /** Look up one record by its ledger ID. */
  get(id: string): AssetRecord | undefined {
    return this.records.find((r) => r.id === id);
  }

  /** Every record belonging to one owner. */
  byOwner(owner: string): AssetRecord[] {
    return this.records.filter((r) => r.owner === owner);
  }

  /** Every record, in the order they were opened. */
  all(): AssetRecord[] {
    return [...this.records];
  }

  /** How many records the ledger holds. */
  count(): number {
    return this.records.length;
  }

  /** The whole ledger as JSON text, ready to store. */
  save(): string {
    return JSON.stringify(
      { nextNumber: this.nextNumber, records: this.records },
      null,
      2,
    );
  }

  /** Rebuild a registry from save() output. */
  static load(json: string): AssetRegistry {
    const data = JSON.parse(json) as {
      nextNumber: number;
      records: AssetRecord[];
    };
    const registry = new AssetRegistry();
    registry.nextNumber = data.nextNumber;
    registry.records = data.records;
    return registry;
  }
}
