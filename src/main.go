package main

import (
	"github.com/fagustin07/flecha-lang/src/parser"
	"github.com/sanity-io/litter"
	"os"

	"github.com/fagustin07/flecha-lang/src/tokenizer"
)

func main() {
	bytes, _ := os.ReadFile("./inputs/02_ops.fcl")
	tokens := tokenizer.Exec(string(bytes))

	ast := parser.Parse(tokens)

	litter.Dump(ast)
}
