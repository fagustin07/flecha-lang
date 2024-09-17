package tokenizer

import (
	"fmt"
	"regexp"
)

type regexHandler func(tok *tokenizer, regex *regexp.Regexp)

type regexPattern struct {
	regex   *regexp.Regexp
	handler regexHandler
}

type tokenizer struct {
	patterns []regexPattern
	Tokens   []Token
	source   string
	pos      int
	line     int
}

func (tok *tokenizer) advanceN(n int) {
	tok.pos += n
}

func (tok *tokenizer) push(token Token) {
	tok.Tokens = append(tok.Tokens, token)
}

func (tok *tokenizer) remainder() string {
	return tok.source[tok.pos:]
}

func (tok *tokenizer) at_eof() bool {
	return tok.pos >= len(tok.source)
}

func Exec(source string) []Token {
	tok := initTokenizer(source)

	for !tok.at_eof() {
		matched := false
		for _, pattern := range tok.patterns {
			loc := pattern.regex.FindStringIndex(tok.remainder())

			if loc != nil && loc[0] == 0 {
				pattern.handler(tok, pattern.regex)
				matched = true
				break
			}
		}

		if !matched {
			panic(fmt.Sprintf("[TOKENIZER ERROR] Unrecognized token near '%v'", tok.remainder()))
		}
	}

	tok.push(NewToken(EOF, "EOF"))
	return tok.Tokens
}

func initTokenizer(source string) *tokenizer {
	return &tokenizer{
		pos:    0,
		line:   1,
		source: source,
		Tokens: make([]Token, 0),
		patterns: []regexPattern{
			// LITERALES
			{regexp.MustCompile(`[0-9]+`), numberHandler},
			{regexp.MustCompile(`"[^"]*"`), stringHandler},
			{regexp.MustCompile(`'[^']'`), charHandler},

			// PALABRAS QUE NO SON TOKENS
			{regexp.MustCompile(`--.*`), commentHandler},
			{regexp.MustCompile(`\s+`), ignoreHandler},

			// IDENTIFICADORES
			{regexp.MustCompile(`[a-z][_a-zA-Z0-9]*`), identifierHandler(LOWERID)},
			{regexp.MustCompile(`[A-Z][_a-zA-Z0-9]*`), identifierHandler(UPPERID)},

			// SIMBOLOS
			{regexp.MustCompile(`==`), defaultHandler(EQ, "==")},
			{regexp.MustCompile(`=`), defaultHandler(DEFEQ, "=")},
			{regexp.MustCompile(`;`), defaultHandler(SEMICOLON, ";")},
			{regexp.MustCompile(`\(`), defaultHandler(LPAREN, "(")},
			{regexp.MustCompile(`\)`), defaultHandler(RPAREN, ")")},
			{regexp.MustCompile(`\\`), defaultHandler(LAMBDA, "\\")},
			{regexp.MustCompile(`\|\|`), defaultHandler(OR, "||")},
			{regexp.MustCompile(`\|`), defaultHandler(PIPE, "|")},
			{regexp.MustCompile(`&&`), defaultHandler(AND, "&&")},
			{regexp.MustCompile(`!=`), defaultHandler(NE, "!=")},
			{regexp.MustCompile(`!`), defaultHandler(NOT, "!")},
			{regexp.MustCompile(`->`), defaultHandler(ARROW, "->")},
			{regexp.MustCompile(`>=`), defaultHandler(GE, ">=")},
			{regexp.MustCompile(`<=`), defaultHandler(LE, "<=")},
			{regexp.MustCompile(`>`), defaultHandler(GT, ">")},
			{regexp.MustCompile(`<`), defaultHandler(LT, "<")},
			{regexp.MustCompile(`\+`), defaultHandler(PLUS, "+")},
			{regexp.MustCompile(`-`), defaultHandler(MINUS, "-")},
			{regexp.MustCompile(`\*`), defaultHandler(TIMES, "*")},
			{regexp.MustCompile(`/`), defaultHandler(DIV, "/")},
			{regexp.MustCompile(`%`), defaultHandler(MOD, "%")},
		},
	}
}

func defaultHandler(kind TokenKind, value string) regexHandler {
	return func(tok *tokenizer, _ *regexp.Regexp) {
		tok.advanceN(len(value))
		tok.push(NewToken(kind, value))
	}
}

func numberHandler(tok *tokenizer, regex *regexp.Regexp) {
	match := regex.FindString(tok.remainder())
	tok.push(NewToken(NUMBER, match))
	tok.advanceN(len(match))
}

func ignoreHandler(tok *tokenizer, regex *regexp.Regexp) {
	match := regex.FindStringIndex(tok.remainder())
	tok.advanceN(match[1])
}

func identifierHandler(kind TokenKind) regexHandler {
	return func(tok *tokenizer, regex *regexp.Regexp) {
		match := regex.FindString(tok.remainder())
		tok.push(NewToken(kind, match))
		tok.advanceN(len(match))
	}
}

func charHandler(tok *tokenizer, regex *regexp.Regexp) {
	match := regex.FindString(tok.remainder())
	tok.push(NewToken(CHAR, match[1:len(match)-1]))
	tok.advanceN(len(match))
}

func stringHandler(tok *tokenizer, regex *regexp.Regexp) {
	match := regex.FindString(tok.remainder())
	tok.push(NewToken(STRING, match[1:len(match)-1]))
	tok.advanceN(len(match))
}

func commentHandler(tok *tokenizer, regex *regexp.Regexp) {
	match := regex.FindStringIndex(tok.remainder())
	if match != nil {
		tok.advanceN(match[1])
		tok.line++
	}
}
