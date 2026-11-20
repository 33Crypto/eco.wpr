import { describe, expect, test } from "bun:test";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { AssetRegistry } from "../src/registry";
import { FileStore } from "../src/store";

const N = 100;

describe("loop", () => {
  test("registering in a loop yields sequential IDs and a matching count", () => {
    const registry = new AssetRegistry();
    for (let i = 1; i <= N; i++) {
      const record = registry.register({ owner: "A", asset: `asset-${i}`, kind: "domain" });
      expect(record.id).toBe(`ECO-${String(i).padStart(4, "0")}`);
      expect(registry.count()).toBe(i);
    }
  });

  test("a looped registry survives a reload from the store", () => {
    const path = join(mkdtempSync(join(tmpdir(), "eco-wpr-")), "ledger.json");
    const first = new AssetRegistry({ store: new FileStore(path) });
    for (let i = 1; i <= N; i++) {
      first.register({ owner: "A", asset: `asset-${i}`, kind: "domain" });
    }
    const second = new AssetRegistry({ store: new FileStore(path) });
    expect(second.count()).toBe(N);
    expect(second.all()[N - 1].asset).toBe(`asset-${N}`);
  });
});
