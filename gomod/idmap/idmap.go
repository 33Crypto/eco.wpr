// Package idmap maps LOCK33iD identity tokens to their meanings.
// Tokens are case-sensitive.
package idmap

// Build returns a fresh map of identity token to meaning.
func Build() map[string]string {
	return map[string]string{
		"id":   "child's registered identification",
		"ID":   "common free-tier adult, machine, bot or error registration",
		"iD":   "paid VIP registration; reserved for human purchase and human-only use",
		"33iD": "paid VIP",
	}
}

// Meaning looks up a token's meaning.
func Meaning(token string) (string, bool) {
	m, ok := Build()[token]
	return m, ok
}
