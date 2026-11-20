package ledgerid

import "testing"

func TestFormat(t *testing.T) {
	cases := map[int]string{1: "ECO-0001", 33: "ECO-0033", 10000: "ECO-10000"}
	for n, want := range cases {
		if got := Format(n); got != want {
			t.Errorf("Format(%d) = %q, want %q", n, got, want)
		}
	}
}

func TestFormatLoopIsUnique(t *testing.T) {
	seen := map[string]bool{}
	for i := 1; i <= 100; i++ {
		id := Format(i)
		if seen[id] {
			t.Fatalf("duplicate ID %s", id)
		}
		seen[id] = true
	}
}
