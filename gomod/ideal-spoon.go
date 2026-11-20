package main

import (
	"fmt"

	"github.com/33Crypto/eco.wpr/gomod/ledgerid"
)

func main() {
	for i := 1; i <= 3; i++ {
		fmt.Println(ledgerid.Format(i))
	}
}
