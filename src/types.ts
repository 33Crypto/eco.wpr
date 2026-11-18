// eco.wpr — core record types.
//
// An AssetRecord is one protected asset on the LOCK33 Organization
// ledger: who owns it, what it is, and where it stands.

export type AssetStatus = "protected" | "flagged" | "released";

export interface AssetRecord {
  /** Ledger ID, assigned by the registry: ECO-0001, ECO-0002, ... */
  id: string;
  /** Who the asset belongs to. */
  owner: string;
  /** What the asset is, in the owner's words. */
  asset: string;
  /** Kind of asset, e.g. "account", "domain", "device", "document". */
  kind: string;
  /** ISO timestamp of when the record was opened. */
  registeredAt: string;
  /** Current standing of the asset. New records start "protected". */
  status: AssetStatus;
  /** Free note — why it was flagged, released, or anything else worth keeping. */
  note: string;
}

export interface NewAsset {
  owner: string;
  asset: string;
  kind: string;
  note?: string;
}
