package parser

import (
	"github.com/fagustin07/flecha-lang/src/ast"
	"github.com/fagustin07/flecha-lang/src/tokenizer"
)

type bindingPower int

const (
	defaultBp bindingPower = iota
	comma
	assignment
	logical
	relational
	additive
	multiplicative
	unary
	call
	member
	primary
)

type stmtHandler func(p *parser) ast.Stmt
type nudHandler func(p *parser) ast.Expr
type ledHandler func(p *parser, left ast.Expr, bp bindingPower) ast.Expr

type stmtLookup map[tokenizer.TokenKind]stmtHandler
type nudLookup map[tokenizer.TokenKind]nudHandler
type ledLookup map[tokenizer.TokenKind]ledHandler
type bpLookup map[tokenizer.TokenKind]bindingPower

var bpLu = bpLookup{}
var nudLu = nudLookup{}
var ledLu = ledLookup{}
var stmtLu = stmtLookup{}

func led(kind tokenizer.TokenKind, bp bindingPower, led_fn ledHandler) {
	bpLu[kind] = bp
	ledLu[kind] = led_fn
}

func nud(kind tokenizer.TokenKind, bp bindingPower, nud_fn nudHandler) {
	bpLu[kind] = primary
	nudLu[kind] = nud_fn
}

func stmt(kind tokenizer.TokenKind, stmtFn stmtHandler) {
	bpLu[kind] = defaultBp
	stmtLu[kind] = stmtFn
}

func createTokenLookups() {

	led(tokenizer.AND, logical, parseBinaryExpr)
	led(tokenizer.OR, logical, parseBinaryExpr)

	led(tokenizer.LT, relational, parseBinaryExpr)
	led(tokenizer.LE, relational, parseBinaryExpr)
	led(tokenizer.GT, relational, parseBinaryExpr)
	led(tokenizer.GE, relational, parseBinaryExpr)
	led(tokenizer.EQ, relational, parseBinaryExpr)
	led(tokenizer.NE, relational, parseBinaryExpr)

	led(tokenizer.PLUS, additive, parseBinaryExpr)
	led(tokenizer.MINUS, additive, parseBinaryExpr)
	led(tokenizer.DIV, multiplicative, parseBinaryExpr)
	led(tokenizer.TIMES, multiplicative, parseBinaryExpr)
	led(tokenizer.MOD, multiplicative, parseBinaryExpr)

	nud(tokenizer.NUMBER, primary, parsePrimaryExpr)
	nud(tokenizer.STRING, primary, parsePrimaryExpr)
	nud(tokenizer.LOWERID, primary, parsePrimaryExpr)
	nud(tokenizer.UPPERID, primary, parsePrimaryExpr)
	nud(tokenizer.CHAR, primary, parsePrimaryExpr)

}
