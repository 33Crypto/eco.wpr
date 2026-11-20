package idmap

import "testing"

func TestBuildIsCaseSensitive(t *testing.T) {
	m := Build()
	if len(m) != 4 {
		t.Fatalf("got %d tokens, want 4", len(m))
	}
	if m["id"] == m["ID"] || m["ID"] == m["iD"] {
		t.Error("id, ID and iD must have distinct meanings")
	}
}

func TestMeaningUnknown(t *testing.T) {
	if _, ok := Meaning("LOCK"); ok {
		t.Error("LOCK is a command, not an identity token")
	}
	if _, ok := Meaning("iD"); !ok {
		t.Error("iD should be known")
	}
}
