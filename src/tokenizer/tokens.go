package tokenizer

import "fmt"

type TokenKind int

const (
	EOF TokenKind = iota
	//////////////////
	// IDENTIFICADORES
	//////////////////
	LOWERID
	UPPERID

	//////////////////
	// CONSTANTES
	//////////////////
	NUMBER
	CHAR
	STRING

	//////////////////
	// DELIMITADORES
	//////////////////
	DEFEQ
	SEMICOLON
	LPAREN
	RPAREN
	LAMBDA
	PIPE
	ARROW

	//////////////////
	// OPERADORES LOGICOS
	//////////////////
	AND
	OR
	NOT

	//////////////////
	// COMPARACIONES
	//////////////////
	EQ
	NE
	GE
	LE
	GT
	LT

	//////////////////
	// OPERADORES ARITMETICOS
	//////////////////
	PLUS
	MINUS
	TIMES
	DIV
	MOD

	//////////////////
	// PALABRAS CLAVES
	//////////////////
	DEF
	IF
	THEN
	ELIF
	ELSE

	CASE

	LET
	IN
)

type Token struct {
	Kind  TokenKind
	Value string
}

func NewToken(kind TokenKind, value string) Token {
	return Token{
		kind,
		value,
	}
}

func (token Token) isAtomic() bool {
	return token.Kind == NUMBER || token.Kind == STRING || token.Kind == CHAR ||
		token.Kind == LOWERID || token.Kind == UPPERID
}

func (token Token) Print() {
	if token.isAtomic() {
		fmt.Printf("[%s] %s\n", StringifyTokenKind(token.Kind), token.Value)
	} else {
		fmt.Printf("[%s]\n", StringifyTokenKind(token.Kind))
	}
}

func StringifyTokenKind(tokenKind TokenKind) string {
	switch tokenKind {
	case EOF:
		return "eof"
	case LOWERID:
		return "lower_id"
	case UPPERID:
		return "upper_id"

	case NUMBER:
		return "number"
	case CHAR:
		return "char"
	case STRING:
		return "string"

	case DEFEQ:
		return "assign"
	case SEMICOLON:
		return "semicolon"
	case LPAREN:
		return "left_paren"
	case RPAREN:
		return "right_paren"
	case LAMBDA:
		return "lambda"
	case PIPE:
		return "pipe"
	case ARROW:
		return "arrow"

	case AND:
		return "and"
	case OR:
		return "or"
	case NOT:
		return "not"

	case EQ:
		return "equals"
	case NE:
		return "not_equals"
	case GE:
		return "greater_equals"
	case LE:
		return "less_equals"
	case GT:
		return "greater"
	case LT:
		return "less"

	case PLUS:
		return "plus"
	case MINUS:
		return "minus"
	case TIMES:
		return "times"
	case DIV:
		return "div"
	case MOD:
		return "rest"

	case DEF:
		return "definition"
	case IF:
		return "if"
	case THEN:
		return "then"
	case ELIF:
		return "elif"
	case ELSE:
		return "else"

	case CASE:
		return "case"

	case LET:
		return "let"
	case IN:
		return "in"

	default:
		return fmt.Sprintf("unknow token (%d)", tokenKind)
	}
}
