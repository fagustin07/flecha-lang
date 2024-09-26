from typing import Sequence

from src.abstract_syntax_tree.ast import AstKind, AstLeaf, AstNode, AstSequence


class FlechaFactoryExpression:

    def empty_program(self):
        return Program()

    def program_with(self, prog, def_expr):
        prog: Program = prog
        prog.add_node(def_expr)
        return prog

    def definition_from(self, lower_id, params, expr):
        return Def(lower_id, self.expression_with_params(params, expr))

    def empty_params(self):
        return []

    def let_expression_from(self, param_name, params, let_param_def, let_context):
        args = self.expression_with_params(params, let_param_def)
        return ExprLet(param_name, args, let_context)

    def charlist_from_string(self, desired_string: str):
        if not desired_string:
            return LiteralConstructorExpr(self.empty_list_constructor())
        return (
            ExprApply(
                ExprApply(
                    LiteralConstructorExpr(self.concat_list_constructor()),
                    LiteralCharExpr(desired_string[0])
                ),
                self.charlist_from_string(desired_string[1:])
            )
        )

    def expression_with_params(self, params, expression):
        if not params:
            return expression
        return ExprLambda(params[0], self.expression_with_params(params[1::], expression))

    def seq_expr_with_expressions(self, expr1, expr2):
        return ExprLet(self.empty_id(), expr1, expr2)

    def apply_expr_from(self, expr, literal_expr):
        return ExprApply(expr, literal_expr)

    def binary_expr_from(self, left_expr, operator, right_expr):
        op = keywords_dict[OP_BINARY].get(operator)
        left_apply = ExprApply(LiteralVariableExpr(op), left_expr)
        return ExprApply(left_apply, right_expr)

    def unary_expr_from(self, operator, expr):
        op = keywords_dict[OP_UNARY].get(operator)
        return ExprApply(LiteralVariableExpr(op), expr)

    def build_if(self, expr, then_expr, else_expr):
        return CaseExpr(expr, CaseBranches([CaseBranch(TRUE_ID, [], then_expr), else_expr]))

    def build_else(self, else_expr):
        return CaseBranch(FALSE_ID, [], else_expr)

    def case_expr_from(self, expr, branches):
        return CaseExpr(expr, branches)

    def empty_branches(self):
        return CaseBranches([])

    def case_branch_from(self, struct_name, params, internal_expr):
        return CaseBranch(struct_name, params, internal_expr)

    def concat_list_constructor(self):
        return 'Cons'

    def empty_list_constructor(self):
        return 'Nil'

    def empty_id(self):
        return '_'

    def literal_expr_from(self, token_str, value):
        match token_str:
            case 'LOWERID':
                return LiteralVariableExpr(value)
            case 'UPPERID':
                return LiteralConstructorExpr(value)
            case 'NUMBER':
                return LiteralNumberExpr(value)
            case 'CHAR':
                return LiteralCharExpr(value)
            case 'STRING':
                return self.charlist_from_string(value)
            case _:
                raise Exception(f"[Error] Unespected token: {value}")


TRUE_ID = 'True'
FALSE_ID = 'False'

OP_UNARY = 'unary'
OP_BINARY = 'binary'

SYMBOL_UNARY_NOT = '!'
SYMBOL_UNARY_MINUS = '-'

SYMBOL_BINARY_OR = '||'
SYMBOL_BINARY_AND = '&&'
SYMBOL_BINARY_EQ = '=='
SYMBOL_BINARY_NE = '!='
SYMBOL_BINARY_GE = '>='
SYMBOL_BINARY_LE = '<='
SYMBOL_BINARY_GT = '>'
SYMBOL_BINARY_LT = '<'
SYMBOL_BINARY_ADD = '+'
SYMBOL_BINARY_SUB = '-'
SYMBOL_BINARY_MUL = '*'
SYMBOL_BINARY_DIV = '/'
SYMBOL_BINARY_MOD = '%'

UNARY_NOT = 'NOT'
UNARY_MINUS = 'UMINUS'

BINARY_OR = 'OR'
BINARY_AND = 'AND'
BINARY_EQ = 'EQ'
BINARY_NE = 'NE'
BINARY_GE = 'GE'
BINARY_LE = 'LE'
BINARY_GT = 'GT'
BINARY_LT = 'LT'
BINARY_ADD = 'ADD'
BINARY_SUB = 'SUB'
BINARY_MUL = 'MUL'
BINARY_DIV = 'DIV'
BINARY_MOD = 'MOD'

keywords_dict = {
    OP_BINARY: {
        SYMBOL_BINARY_OR: BINARY_OR,
        SYMBOL_BINARY_AND: BINARY_AND,
        SYMBOL_BINARY_EQ: BINARY_EQ,
        SYMBOL_BINARY_NE: BINARY_NE,
        SYMBOL_BINARY_GE: BINARY_GE,
        SYMBOL_BINARY_LE: BINARY_LE,
        SYMBOL_BINARY_GT: BINARY_GT,
        SYMBOL_BINARY_LT: BINARY_LT,
        SYMBOL_BINARY_ADD: BINARY_ADD,
        SYMBOL_BINARY_SUB: BINARY_SUB,
        SYMBOL_BINARY_MUL: BINARY_MUL,
        SYMBOL_BINARY_DIV: BINARY_DIV,
        SYMBOL_BINARY_MOD: BINARY_MOD
    },
    OP_UNARY: {
        SYMBOL_UNARY_MINUS: UNARY_MINUS,
        SYMBOL_UNARY_NOT: UNARY_NOT
    }
}


class Program(AstSequence):
    def __init__(self):
        super().__init__(AstKind.Program, [])


class Def(AstNode):
    def __init__(self, id_value, expr):
        super().__init__(AstKind.Def, [AstLeaf(AstKind.Id, id_value), expr])


class ExprLet(AstNode):
    def __init__(self, _id: str, expr1, expr2):
        super().__init__(AstKind.ExprLet, [AstLeaf(AstKind.Id, _id), expr1, expr2])


class ExprApply(AstNode):
    def __init__(self, func, arg):
        super().__init__(AstKind.ExprApply, [func, arg])


class ExprLambda(AstNode):
    def __init__(self, param, expr):
        super().__init__(AstKind.ExprLambda, [AstLeaf(AstKind.Id, param), expr])


class ExprLiteral(AstLeaf):
    def __init__(self, kind: AstKind, value):
        super().__init__(kind, value)

    def _show(self):
        return [self.kind, self.value]


class LiteralNumberExpr(ExprLiteral):
    def __init__(self, value):
        super().__init__(AstKind.ExprNumber, value)


class LiteralVariableExpr(ExprLiteral):
    def __init__(self, value):
        super().__init__(AstKind.ExprVar, AstLeaf(AstKind.Id, value))


class LiteralConstructorExpr(ExprLiteral):
    def __init__(self, value):
        super().__init__(AstKind.ExprConstructor, AstLeaf(AstKind.Id, value))


class LiteralCharExpr(ExprLiteral):
    def __init__(self, value):
        super().__init__(AstKind.ExprChar, ord(value))


class CaseBranch(AstNode):
    def __init__(self, _id: str, _params: Sequence[str], expr):
        super().__init__(AstKind.CaseBranch,
                         [AstLeaf(AstKind.Id, _id), Params([AstLeaf(AstKind.Id, param) for param in _params]), expr])

    def id(self):
        return self.children[0].value

    def params(self):
        return [param.value for param in self.children[1].children]

    def expr(self):
        return self.children[2]


class Params(AstSequence):
    def __init__(self, params):
        super().__init__(AstKind.Params, params)


class CaseBranches(AstSequence):
    def __init__(self, branches: Sequence[CaseBranch]):
        super().__init__(AstKind.CaseBranches, branches)

    def add_case(self, branch):
        return self.add_node(branch)


class CaseExpr(AstNode):
    def __init__(self, expr: AstNode, branches: CaseBranches):
        super().__init__(AstKind.ExprCase, [expr] + branches.children)

    def expr(self):
        return self.children[0]

    def branches(self):
        return self.children[1:]

    def _out_branches(self):
        return [b._show() for b in self.branches()]

    def _show(self):
        return [self.kind, self.expr()._show(), self._out_branches()]
