import { describe, expect, test } from "bun:test";
import { AssetRegistry } from "../src/registry";

describe("AssetRegistry", () => {
  test("register opens a protected record with a ledger ID", () => {
    const registry = new AssetRegistry();
    const record = registry.register({
      owner: "A. Owner",
      asset: "example.org",
      kind: "domain",
    });
    expect(record.id).toBe("ECO-0001");
    expect(record.status).toBe("protected");
    expect(registry.count()).toBe(1);
  });

  test("IDs increase in order", () => {
    const registry = new AssetRegistry();
    registry.register({ owner: "A", asset: "one", kind: "domain" });
    const second = registry.register({ owner: "A", asset: "two", kind: "domain" });
    expect(second.id).toBe("ECO-0002");
  });

  test("setStatus flags a record and keeps the note", () => {
    const registry = new AssetRegistry();
    const record = registry.register({ owner: "A", asset: "one", kind: "domain" });
    registry.setStatus(record.id, "flagged", "Needs review.");
    expect(registry.get(record.id)?.status).toBe("flagged");
    expect(registry.get(record.id)?.note).toBe("Needs review.");
  });

  test("setStatus on an unknown ID throws", () => {
    const registry = new AssetRegistry();
    expect(() => registry.setStatus("ECO-9999", "flagged")).toThrow();
  });

  test("byOwner returns only that owner's records", () => {
    const registry = new AssetRegistry();
    registry.register({ owner: "A", asset: "one", kind: "domain" });
    registry.register({ owner: "B", asset: "two", kind: "domain" });
    expect(registry.byOwner("A")).toHaveLength(1);
    expect(registry.byOwner("A")[0].asset).toBe("one");
  });

  test("save and load round-trip the ledger", () => {
    const registry = new AssetRegistry();
    registry.register({ owner: "A", asset: "one", kind: "domain" });
    const restored = AssetRegistry.load(registry.save());
    expect(restored.count()).toBe(1);
    const next = restored.register({ owner: "A", asset: "two", kind: "domain" });
    expect(next.id).toBe("ECO-0002");
  });
});
