package tokenizer_test

import (
	"testing"

	"github.com/fagustin07/flecha-lang/src/tokenizer"
	"github.com/stretchr/testify/assert"
)

func Test01_TokenizerRecognizeArithmeticOperations(t *testing.T) {
	source := `123+ (456*789);`

	tokens := tokenizer.Exec(source)

	expectedTokens := []tokenizer.Token{
		{Kind: tokenizer.NUMBER, Value: "123"},
		{Kind: tokenizer.PLUS, Value: "+"},
		{Kind: tokenizer.LPAREN, Value: "("},
		{Kind: tokenizer.NUMBER, Value: "456"},
		{Kind: tokenizer.TIMES, Value: "*"},
		{Kind: tokenizer.NUMBER, Value: "789"},
		{Kind: tokenizer.RPAREN, Value: ")"},
		{Kind: tokenizer.SEMICOLON, Value: ";"},
		{Kind: tokenizer.EOF, Value: "EOF"},
	}

	assert.Equal(t, expectedTokens, tokens)
}

func Test02_TokenizerRecognizeIdentifiers(t *testing.T) {
	source := `hola; Hola`

	tokens := tokenizer.Exec(source)

	expectedTokens := []tokenizer.Token{
		{Kind: tokenizer.LOWERID, Value: "hola"},
		{Kind: tokenizer.SEMICOLON, Value: ";"},
		{Kind: tokenizer.UPPERID, Value: "Hola"},
		{Kind: tokenizer.EOF, Value: "EOF"},
	}

	assert.Equal(t, expectedTokens, tokens)
}

func Test03_TokenizerIgnoreComments(t *testing.T) {
	source := `-- como estamos hoy aqui reunidos 1234 *** ///; >=`

	tokens := tokenizer.Exec(source)

	expectedTokens := []tokenizer.Token{
		{Kind: tokenizer.EOF, Value: "EOF"},
	}

	assert.Equal(t, expectedTokens, tokens)
}

func Test04_TokenizerIgnoresEveryWhitespaceKind(t *testing.T) {
	source := "\r123 +	 456  * \n  \t789 ;"

	tokens := tokenizer.Exec(source)

	expectedTokens := []tokenizer.Token{
		{Kind: tokenizer.NUMBER, Value: "123"},
		{Kind: tokenizer.PLUS, Value: "+"},
		{Kind: tokenizer.NUMBER, Value: "456"},
		{Kind: tokenizer.TIMES, Value: "*"},
		{Kind: tokenizer.NUMBER, Value: "789"},
		{Kind: tokenizer.SEMICOLON, Value: ";"},
		{Kind: tokenizer.EOF, Value: "EOF"},
	}

	assert.Equal(t, expectedTokens, tokens)
}

func Test05_TokenizerRecognizeStringsAndChars(t *testing.T) {
	source := `"hola como estas"; '!'`
	tokens := tokenizer.Exec(source)

	expectedTokens := []tokenizer.Token{
		{Kind: tokenizer.STRING, Value: "hola como estas"},
		{Kind: tokenizer.SEMICOLON, Value: ";"},
		{Kind: tokenizer.CHAR, Value: "!"},
		{Kind: tokenizer.EOF, Value: "EOF"},
	}

	assert.Equal(t, expectedTokens, tokens)
}
