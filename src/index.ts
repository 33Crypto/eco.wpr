// eco.wpr — demo entry point.
//
// Opens the ledger wired to the fail-safe store and the Pipeline log:
//   bun run src/index.ts
//
// First run opens two records and stores them. Run it again and the
// ledger is rebuilt from the store — the fail-safe doing its job.

import { mkdirSync } from "node:fs";
import { AssetRegistry } from "./registry";
import { FileStore, PipeLog } from "./store";

mkdirSync("data", { recursive: true });
const store = new FileStore("data/ledger.json");
const pipe = new PipeLog("data/pipe.log");

const registry = new AssetRegistry({ store, pipe });

if (registry.count() === 0) {
  registry.register({
    owner: "LOCK33 Organization",
    asset: "lock33.org",
    kind: "domain",
    note: "Organization home domain.",
  });
  registry.register({
    owner: "LOCK33 Organization",
    asset: "iquest.lock33.org",
    kind: "domain",
    note: "iQuest learning platform.",
  });
  console.log("Opened a new ledger and stored it.");
} else {
  console.log("Ledger rebuilt from the fail-safe store.");
}

console.log(`eco.wpr ledger — ${registry.count()} record(s)`);
for (const record of registry.all()) {
  console.log(
    `${record.id}  ${record.status.padEnd(9)}  ${record.kind.padEnd(7)}  ${record.asset}  (${record.owner})`,
  );
}
console.log(`Pipe messages so far: ${pipe.read().length}`);
