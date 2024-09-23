package parser

import (
	"github.com/fagustin07/flecha-lang/src/ast"
	"github.com/fagustin07/flecha-lang/src/tokenizer"
)

func parseStmt(p *parser) ast.Stmt {
	stmtFn, exists := stmtLu[p.currentTokenKind()]

	if exists {
		return stmtFn(p)
	}

	expr := parseExpr(p, defaultBp)

	p.expect(tokenizer.SEMICOLON)

	return ast.ExprStmt{
		Expression: expr,
	}
}
