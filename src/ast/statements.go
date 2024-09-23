package ast

type BlockStmt struct {
	Body []Stmt
}

func (block BlockStmt) stmt() {

}

type ExprStmt struct {
	Expression Expr
}

func (s ExprStmt) stmt() {

}