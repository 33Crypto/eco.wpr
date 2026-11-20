// Package ledgerid formats eco.wpr ledger IDs (ECO-0001, ECO-0002, ...).
package ledgerid

import "fmt"

// Format returns the ledger ID for the n-th record (1-based).
func Format(n int) string {
	return fmt.Sprintf("ECO-%04d", n)
}
