package parser

import (
	"fmt"
	"github.com/fagustin07/flecha-lang/src/ast"
	"github.com/fagustin07/flecha-lang/src/tokenizer"
	"strconv"
)

func parseExpr(p *parser, bp bindingPower) ast.Expr {
	tokenKind := p.currentTokenKind()

	nudFn, exists := nudLu[tokenKind]

	if !exists {
		panic(fmt.Sprintf("NUD Handler expected for token %s\n", tokenizer.StringifyTokenKind(tokenKind)))
	}

	left := nudFn(p)

	for bpLu[p.currentTokenKind()] > bp {
		tokenKind = p.currentTokenKind()
		ledFn, exists := ledLu[tokenKind]

		if !exists {
			panic(fmt.Sprintf("NUD Handler expected for token %s\n", tokenizer.StringifyTokenKind(tokenKind)))
		}

		left = ledFn(p, left, bp)
	}

	return left
}
func parseBinaryExpr(p *parser, left ast.Expr, bp bindingPower) ast.Expr {
	operatorToken := p.advance()
	right := parseExpr(p, bp)

	return ast.BinaryExpr{
		Left:  left,
		Op:    operatorToken,
		Right: right,
	}
}

func parsePrimaryExpr(p *parser) ast.Expr {
	switch p.currentTokenKind() {
	case tokenizer.NUMBER:
		number, _ := strconv.Atoi(p.advance().Value)
		return ast.NumberExpr{
			Value: number,
		}
	case tokenizer.STRING:
		return ast.StringExpr{
			Value: p.advance().Value,
		}
	case tokenizer.CHAR:
		return ast.CharExpr{
			Value: p.advance().Value,
		}
	case tokenizer.LOWERID:
		return ast.SymbolExpr{
			Value: p.advance().Value,
		}
	case tokenizer.UPPERID:
		return ast.SymbolExpr{
			Value: p.advance().Value,
		}
	default:
		panic(fmt.Sprintf("Cannot create primary_expr from %s\n", tokenizer.StringifyTokenKind(p.currentTokenKind())))
	}
}
