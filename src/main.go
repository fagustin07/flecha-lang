package main

import (
	"os"

	"github.com/fagustin07/flecha-lang/src/tokenizer"
)

func main() {
	bytes, _ := os.ReadFile("./inputs/02_ops.fcl")
	code := string(bytes)
	tokens := tokenizer.Exec(code)

	for _, token := range tokens {
		token.Print()
	}
}
