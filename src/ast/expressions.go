package ast

import "github.com/fagustin07/flecha-lang/src/tokenizer"

// LITERALES

type NumberExpr struct {
	Value int
}

func (expr NumberExpr) expr() {

}

type StringExpr struct {
	Value string
}

func (expr StringExpr) expr() {

}

type SymbolExpr struct {
	Value string
}

func (expr SymbolExpr) expr() {

}

type CharExpr struct {
	Value string
}

func (expr CharExpr) expr() {

}

// EXPRESIONES

type BinaryExpr struct {
	Left  Expr
	Op    tokenizer.Token
	Right Expr
}

func (expr BinaryExpr) expr() {

}
