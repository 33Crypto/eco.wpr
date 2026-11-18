// eco.wpr — demo entry point.
//
// Opens a small ledger so you can see the recorder work:
//   bun run src/index.ts

import { AssetRegistry } from "./registry";

const registry = new AssetRegistry();

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

console.log(`eco.wpr ledger — ${registry.count()} record(s)`);
for (const record of registry.all()) {
  console.log(
    `${record.id}  ${record.status.padEnd(9)}  ${record.kind.padEnd(7)}  ${record.asset}  (${record.owner})`,
  );
}
