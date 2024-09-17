package tokenizer_test

import (
	"testing"

	"github.com/fagustin07/flecha-lang/src/tokenizer"
)

func Test01_TokenizerCanReceivedProgramsWithArithmeticExpressionsToGenerateTokens(t *testing.T) {
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

	if !compareTokens(tokens, expectedTokens) {
		t.Errorf("Expected tokens: %v, got: %v", expectedTokens, tokens)
	}
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

	if !compareTokens(tokens, expectedTokens) {
		t.Errorf("Expected tokens: %v, got: %v", expectedTokens, tokens)
	}
}

func Test03_TokenizerIgnoreComments(t *testing.T) {
	source := `-- como estamos hoy aqui reunidos 1234 *** ///; >=`

	tokens := tokenizer.Exec(source)

	expectedTokens := []tokenizer.Token{
		{Kind: tokenizer.EOF, Value: "EOF"},
	}

	if !compareTokens(tokens, expectedTokens) {
		t.Errorf("Expected tokens: %v, got: %v", expectedTokens, tokens)
	}
}

func Test04_TokenizerIgnoreWhitespaces(t *testing.T) {
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

	if !compareTokens(tokens, expectedTokens) {
		t.Errorf("Expected tokens: %v, got: %v", expectedTokens, tokens)
	}
}

func Test05_TokenizerKnowsHowToRecognizeStringsAndChars(t *testing.T) {
	source := `"hola como estas"; '!'`
	tokens := tokenizer.Exec(source)

	expectedTokens := []tokenizer.Token{
		{Kind: tokenizer.STRING, Value: "hola como estas"},
		{Kind: tokenizer.SEMICOLON, Value: ";"},
		{Kind: tokenizer.CHAR, Value: "!"},
		{Kind: tokenizer.EOF, Value: "EOF"},
	}

	if !compareTokens(tokens, expectedTokens) {
		t.Errorf("Expected tokens: %v, got: %v", expectedTokens, tokens)
	}
}

func compareTokens(actual, expected []tokenizer.Token) bool {
	if len(actual) != len(expected) {
		return false
	}

	for i := range actual {
		if actual[i] != expected[i] {
			return false
		}
	}

	return true
}
