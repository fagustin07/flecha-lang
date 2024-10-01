from ply.yacc import yacc

from abstract_syntax_tree.expression import FlechaFactoryExpression
from lexer import Lexer


class Parser:
    tokens = Lexer.tokens

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NOT'),
        ('nonassoc', 'EQ', 'NE', 'GT', 'GE', 'LT', 'LE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES'),
        ('left', 'DIV', 'MOD'),
        ('right', 'UMINUS')
    )

    def __init__(self):
        self.__lexer = Lexer().build()
        self.__yacc = yacc(module=self)
        self.__factory = FlechaFactoryExpression()

    def p_program_empty(self, p):
        """program :"""
        p[0] = self.__factory.empty_program()

    def p_program(self, p):
        """program : program definition"""
        p[0] = self.__factory.program_with(p[1], p[2])

    def p_def(self, p):
        """definition : DEF LOWERID parameters DEFEQ expression"""
        p[0] = self.__factory.definition_from(p[2], p[3], p[5])

    def p_parameters_empty(self, p):
        """parameters :"""
        p[0] = []

    def p_parameters(self, p):
        """parameters : parameters LOWERID"""
        p[0] = p[1] + [p[2]]

    def p_expression(self, p):
        """expression :  externalExpr
                       | sequenceExpr"""
        p[0] = p[1]

    def p_sequence_expr(self, p):
        """sequenceExpr : externalExpr SEMICOLON expression"""
        p[0] = self.__factory.seq_expr_with_expressions(p[1], p[3])

    def p_external_expr(self, p):
        """externalExpr :  ifExpr
                          | letExpr
                          | lambdaExpr
                          | caseExpr
                          | internalExpr"""
        p[0] = p[1]

    def p_internal_expr(self, p):
        """internalExpr : applyExpr
                     | binaryExpr
                     | unaryExpr"""
        p[0] = p[1]

    def p_let_expr(self, p):
        """letExpr : LET LOWERID parameters DEFEQ internalExpr IN externalExpr"""
        p[0] = self.__factory.let_expression_from(p[2], p[3], p[5], p[7])

    def p_lambda_expr(self, p):
        """lambdaExpr : LAMBDA parameters ARROW externalExpr"""
        p[0] = self.__factory.expression_with_params(p[2], p[4])

    def p_apply_expr_base(self, p):
        """applyExpr : literalExpr"""
        p[0] = p[1]

    def p_apply_expr(self, p):
        """applyExpr : applyExpr literalExpr"""
        p[0] = self.__factory.apply_expr_from(p[1], p[2])

    def p_literal_expr(self, p):
        """literalExpr :   LOWERID
                        | UPPERID
                        | NUMBER
                        | CHAR
                        | STRING"""

        p[0] = self.__factory.literal_expr_from(p.slice[1].type, p[1])

    def p_literal_expr_paren(self, p):
        """literalExpr : LPAREN expression RPAREN"""
        p[0] = p[2]

    def p_binary_expr(self, p):
        """binaryExpr : internalExpr OR internalExpr
                    | internalExpr AND internalExpr
                    | internalExpr EQ internalExpr
                    | internalExpr NE internalExpr
                    | internalExpr GE internalExpr
                    | internalExpr LE internalExpr
                    | internalExpr GT internalExpr
                    | internalExpr LT internalExpr
                    | internalExpr PLUS internalExpr
                    | internalExpr MINUS internalExpr
                    | internalExpr TIMES internalExpr
                    | internalExpr DIV internalExpr
                    | internalExpr MOD internalExpr"""
        p[0] = self.__factory.binary_expr_from(p[1], p[2], p[3])

    def p_unary_expr(self, p):
        """unaryExpr : MINUS internalExpr %prec UMINUS
                     | NOT internalExpr"""
        p[0] = self.__factory.unary_expr_from(p[1], p[2])

    def p_case_expr(self, p):
        """caseExpr : CASE internalExpr caseBranches"""
        p[0] = self.__factory.case_expr_from(p[2], p[3])

    def p_case_branches_empty(self, p):
        """caseBranches :"""
        p[0] = self.__factory.empty_branches()

    def p_case_branches_case_branch(self, p):
        """caseBranches : caseBranches caseBranch"""
        p[0] = p[1].add_case(p[2])

    def p_case_branch(self, p):
        """caseBranch : PIPE UPPERID parameters ARROW internalExpr"""
        p[0] = self.__factory.case_branch_from(p[2], p[3], p[5])

    def p_if_expr(self, p):
        """ifExpr : IF internalExpr THEN internalExpr elseBranches"""
        p[0] = self.__factory.build_if(p[2], p[4], p[5])

    def p_else_branches_elif(self, p):
        """elseBranches : ELIF internalExpr THEN internalExpr elseBranches"""
        p[0] = self.__factory.build_else(self.__factory.build_if(p[2], p[4], p[5]))

    def p_else_branches_else(self, p):
        """elseBranches : ELSE internalExpr"""
        p[0] = self.__factory.build_else(p[2])

    def p_error(self, p):
        print(f'Syntax error: {p.value!r} | At line: {p.lineno}')

    def parse(self, input_program):
        output_program = self.__yacc.parse(input_program, lexer=self.__lexer)
        return output_program
