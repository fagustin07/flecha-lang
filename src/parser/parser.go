package parser

import (
	"fmt"
	"github.com/fagustin07/flecha-lang/src/ast"
	"github.com/fagustin07/flecha-lang/src/tokenizer"
)

type parser struct {
	tokens []tokenizer.Token
	pos    int
}

func createParser(tokens []tokenizer.Token) *parser {
	createTokenLookups()

	return &parser{
		tokens: tokens,
		pos:    0,
	}
}

func Parse(tokens []tokenizer.Token) ast.BlockStmt {
	Body := make([]ast.Stmt, 0)
	p := createParser(tokens)

	for p.hasTokens() {
		Body = append(Body, parseStmt(p))
	}
	return ast.BlockStmt{
		Body: Body,
	}
}

func (p *parser) currentToken() tokenizer.Token {
	return p.tokens[p.pos]
}

func (p *parser) advance() tokenizer.Token {
	tk := p.currentToken()
	p.pos++
	return tk
}

func (p *parser) hasTokens() bool {
	return p.pos < len(p.tokens) && p.currentTokenKind() != tokenizer.EOF
}

func (p *parser) nextToken() tokenizer.Token {
	return p.tokens[p.pos+1]
}

func (p *parser) previousToken() tokenizer.Token {
	return p.tokens[p.pos-1]
}

func (p *parser) currentTokenKind() tokenizer.TokenKind {
	return p.tokens[p.pos].Kind
}

func (p *parser) expectError(expectedKind tokenizer.TokenKind, err any) tokenizer.Token {
	token := p.currentToken()
	kind := token.Kind

	if kind != expectedKind {
		if err == nil {
			err = fmt.Sprintf("Expected %s but recieved %s instead\n", tokenizer.StringifyTokenKind(expectedKind), tokenizer.StringifyTokenKind(kind))
		}

		panic(err)
	}

	return p.advance()
}

func (p *parser) expect(expectedKind tokenizer.TokenKind) tokenizer.Token {
	return p.expectError(expectedKind, nil)
}
