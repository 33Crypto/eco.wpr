import { describe, expect, test } from "bun:test";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { AssetRegistry } from "../src/registry";
import { FileStore, PipeLog } from "../src/store";

function tempPath(name: string): string {
  return join(mkdtempSync(join(tmpdir(), "eco-wpr-")), name);
}

describe("wiring", () => {
  test("changes are saved to the store as they happen", () => {
    const store = new FileStore(tempPath("ledger.json"));
    const registry = new AssetRegistry({ store });
    registry.register({ owner: "A", asset: "one", kind: "domain" });
    const restored = AssetRegistry.load(store.load()!);
    expect(restored.count()).toBe(1);
    expect(restored.all()[0].asset).toBe("one");
  });

  test("a wired registry rebuilds itself from the store on open", () => {
    const path = tempPath("ledger.json");
    const first = new AssetRegistry({ store: new FileStore(path) });
    first.register({ owner: "A", asset: "one", kind: "domain" });
    const second = new AssetRegistry({ store: new FileStore(path) });
    expect(second.count()).toBe(1);
    const next = second.register({ owner: "A", asset: "two", kind: "domain" });
    expect(next.id).toBe("ECO-0002");
  });

  test("every change sends a message down the pipe", () => {
    const pipe = new PipeLog(tempPath("pipe.log"));
    const registry = new AssetRegistry({ pipe });
    const record = registry.register({ owner: "A", asset: "one", kind: "domain" });
    registry.setStatus(record.id, "flagged", "Check it.");
    const messages = pipe.read();
    expect(messages).toHaveLength(2);
    expect(messages[0].type).toBe("asset.registered");
    expect(messages[1].type).toBe("asset.status");
  });
});
