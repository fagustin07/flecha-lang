from ply.yacc import yacc

from src.lexer import Lexer


class Parser:
    tokens = Lexer.tokens

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NOT'),
        ('nonassoc', 'EQ', 'NE', 'GT', 'GE', 'LT', 'LE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIV', 'MOD'),
        ('right', 'UMINUS')
    )

    def __init__(self):
        self.__lexer = Lexer().build()
        self.__yacc = yacc(module=self)

    def p_program_empty(self, p):
        """program :"""
        p[0] = []

    def p_program(self, p):
        """program : program definition"""
        p[0] = p[1] + [p[2]]

    def p_def(self, p):
        """definition : DEF LOWERID parameters DEFEQ expression"""
        if len(p[3]) == 0:
            p[0] = ['Def', p[2], p[5]]
        else:
            p[0] = ['Def', p[2], p[3], p[5]]

    def p_parameters_empty(self, p):
        """parameters :"""
        p[0] = []

    def p_parameters(self, p):
        """parameters : parameters LOWERID"""
        p[0] = p[1] + [p[2]]

    def p_expression(self, p):
        """expression :  outerExpr
                       | sequenceExpr"""
        p[0] = p[1]

    def p_sequence_expr(self, p):
        """sequenceExpr : outerExpr SEMICOLON expression"""
        p[0] = ['LetExpr', '_', p[1], p[3]]

    def p_outer_expr(self, p):
        """outerExpr :  ifExpr
                      | letExpr
                      | lambdaExpr
                      | caseExpr
                      | innerExpr"""
        p[0] = p[1]

    def p_let_expr(self, p):
        """letExpr : LET LOWERID parameters DEFEQ innerExpr IN outerExpr"""
        p[0] = ['LetExpr', p[2], p[3], p[5], p[7]]

    def p_lambda_expr(self, p):
        """lambdaExpr : LAMBDA parameters ARROW outerExpr"""
        p[0] = ['ExprLambda', p[2], p[4]]

    def p_case_expr(self, p):
        """caseExpr : CASE innerExpr caseBranches"""
        p[0] = ['ExprCase', p[2]] + p[3]

    def p_case_branches_empty(self, p):
        """caseBranches :"""
        p[0] = []

    def p_case_branches_case_branch(self, p):
        """caseBranches : caseBranches caseBranch"""
        p[0] = p[1] + [p[2]]

    def p_case_branch(self, p):
        """caseBranch : PIPE UPPERID parameters ARROW innerExpr"""
        p[0] = ['CaseBranch', p[2], p[3], p[5]]

    def p_if_expr(self, p):
        """ifExpr : IF innerExpr THEN innerExpr elseBranches"""
        p[0] = ['ExprCase', p[2]] + p[4] + p[5]

    def p_else_branches_elif(self, p):
        """elseBranches : ELIF innerExpr THEN innerExpr elseBranches"""
        p[0] = ['CaseBranch', 'False', [], ['ExprCase', p[2], p[4]]] + p[5]

    def p_else_branches_else(self, p):
        """elseBranches : ELSE innerExpr"""
        p[0] = ['CaseBranch', 'False', [], p[2]]

    def p_inner_expr(self, p):
        """innerExpr : applyExpr
                     | binaryExpr
                     | unaryExpr"""
        p[0] = p[1]

    def p_apply_expr_base(self, p):
        """applyExpr : atomicExpr"""
        p[0] = p[1]

    def p_apply_expr(self, p):
        """applyExpr : applyExpr atomicExpr"""
        p[0] = ['ExprApply', p[1], p[2]]

    def p_atomic_expr(self, p):
        """atomicExpr :   LOWERID
                        | UPPERID
                        | NUMBER
                        | CHAR
                        | STRING"""

        match p.slice[1].type:
            case 'LOWERID':
                p[0] = ['ExprVar', p[1]]
            case 'UPPERID':
                p[0] = ['ExprConstructor', p[1]]
            case 'NUMBER':
                p[0] = ['ExprNumber', p[1]]
            case 'CHAR':
                p[0] = ['ExprChar', p[1]]
            case 'STRING':
                # TODO: Parsear lista de chars
                p[0] = ['ExprString', p[1]]
            case _:
                raise Exception(f"Unexpected token: {p[1]}")

    def p_atomic_expr_paren(self, p):
        """atomicExpr : LPAREN expression RPAREN"""
        p[0] = p[2]

    def p_binary_expr(self, p):
        """binaryExpr : innerExpr OR innerExpr
                    | innerExpr AND innerExpr
                    | innerExpr EQ innerExpr
                    | innerExpr NE innerExpr
                    | innerExpr GE innerExpr
                    | innerExpr LE innerExpr
                    | innerExpr GT innerExpr
                    | innerExpr LT innerExpr
                    | innerExpr PLUS innerExpr
                    | innerExpr MINUS innerExpr
                    | innerExpr TIMES innerExpr
                    | innerExpr DIV innerExpr
                    | innerExpr MOD innerExpr"""
        p[0] = [p[2], p[1], p[3]]

    def p_unary_expr(self, p):
        """unaryExpr : MINUS innerExpr %prec UMINUS
                     | NOT innerExpr"""
        p[0] = [p[1], p[2]]

    def p_error(self, p):
        print(f'Syntax error: {p.value!r} | At line: {p.lineno}')

    def parse(self, input_program):
        output_program = self.__yacc.parse(input_program, lexer=self.__lexer)
        return output_program
