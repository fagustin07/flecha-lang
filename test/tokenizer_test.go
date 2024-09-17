package tokenizer_test

import (
	"testing"

	"github.com/fagustin07/flecha-lang/src/tokenizer"
)

func Test_TokenizerCanReceivedProgramsWithArithmeticExpressionsToGenerateTokens(t *testing.T) {
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

func Test_TokenizerIgnoreWhitespaces(t *testing.T) {
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
