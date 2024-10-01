import unittest

from abstract_syntax_tree.expression import Def, ExprLet, ExprApply, LiteralVariableExpr, FlechaFactoryExpression, \
    Program, LiteralNumberExpr, CaseExpr, CaseBranches, CaseBranch, ExprLambda, LiteralConstructorExpr
from parser import Parser

from flecha_exception import FlechaLangException

from src.flecha_exception import FlechaExceptionType


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.factory = FlechaFactoryExpression()

    def test01_cuando_se_analiza_sintacticamente_una_expresion_secuenciacion_entonces_se_genera_ast_de_let(self):
        input_seq = """
        def main = print "hola\n"; print "chau\n"
        """

        ast_let = Program()
        ast_let.add_node(Def(
            'main',
            ExprLet(
                '_',
                ExprApply(
                    LiteralVariableExpr('print'),
                    self.factory.literal_expr_from('STRING', 'hola\n'),
                ),
                ExprApply(
                    LiteralVariableExpr('print'),
                    self.factory.literal_expr_from('STRING', 'chau\n'),
                )
            )
        ))
        parser = Parser()
        seq_ast = parser.parse(input_seq)

        self.assertEqual(seq_ast, ast_let)

    def test02_cuando_se_reciben_deficiniones_entonces_se_genera_el_ast_correspondiente(self):
        input_program = """
            def uno = 1
            def dos = 2
            def tres = 3
        """

        defs = [
            Def("uno", LiteralNumberExpr(1)),
            Def("dos", LiteralNumberExpr(2)),
            Def("tres", LiteralNumberExpr(3)),
        ]
        expected_prog = Program()

        for d in defs:
            expected_prog.add_node(d)

        parser = Parser()
        actual_ast = parser.parse(input_program)
        self.assertEqual(actual_ast, expected_prog)

    def test03_cuando_se_analiza_una_expresion_let_entonces_se_genera_el_ast_correctamente(self):
        input_let = """
        def x = let y = 5 in y
        """

        ast_let = Program()

        ast_let.add_node(Def(LiteralVariableExpr('x'),
                             self.factory.let_expression_from(LiteralVariableExpr('y'), [], LiteralNumberExpr(5),
                                                              LiteralVariableExpr('y'))))

        parser = Parser()
        actual_ast = parser.parse(input_let)
        self.assertEqual(ast_let, actual_ast)

    def test04_cuando_se_analiza_una_expresion_lambda_entonces_se_genera_el_ast_correctamente(self):
        input_lambda = """
        def increment =  \\x -> x + 1
        """

        ast_lambda = Program()

        x = Def("increment", ExprLambda(LiteralVariableExpr('x'),
                                        ExprApply(
                                            ExprApply(LiteralVariableExpr('ADD'), LiteralVariableExpr('x')),
                                            LiteralNumberExpr(1)
                                        )
                                        ))
        ast_lambda.add_node(x)
        parser = Parser()
        actual_ast = parser.parse(input_lambda)
        self.assertEqual(actual_ast, ast_lambda)

    def test05_cuando_se_analiza_una_expresion_case_entonces_se_genera_el_ast_correctamente(self):
        input_case = """
            def null list =
              case list
              | Nil       -> True
              | Cons x xs -> False
        """
        case_expr = ExprLambda(LiteralVariableExpr('list'),
                               CaseExpr(LiteralVariableExpr('list'), CaseBranches(
                                   [CaseBranch('Nil', [], LiteralConstructorExpr('True')),
                                    CaseBranch('Cons', ['x', 'xs'], LiteralConstructorExpr('False')),
                                    ]
                               )))
        program = Program()
        case_def_expr = Def("null", case_expr)
        program.add_node(case_def_expr)
        parser = Parser()

        actual_ast = parser.parse(input_case)

        self.assertEqual(program, actual_ast)

    def test06_cuando_se_analiza_una_expresion_if_entonces_se_genera_el_ast_correctamente(self):
        input_if = """
        def natural x = if x > 0 then print 1 else print 2
        """
        expected_if_then_else_ast = (
            Def(
                'natural',
                ExprLambda(
                    'x',
                    CaseExpr(
                        ExprApply(
                            ExprApply(
                                LiteralVariableExpr('GT'),
                                LiteralVariableExpr('x')
                            ),
                            LiteralNumberExpr(0)
                        ),
                        CaseBranches(
                            [
                                CaseBranch(
                                    'True',
                                    [],
                                    ExprApply(
                                        LiteralVariableExpr('print'),
                                        LiteralNumberExpr(1)
                                    )
                                ),
                                CaseBranch(
                                    'False',
                                    [],
                                    ExprApply(
                                        LiteralVariableExpr('print'),
                                        LiteralNumberExpr(2)
                                    )
                                ),
                            ]
                        )
                    )
                )
            ))
        ast_if = Program().add_node(expected_if_then_else_ast)

        parser = Parser()
        actual_ast = parser.parse(input_if)
        self.assertEqual(ast_if, actual_ast)

    def test07_cuando_se_analiza_un_programa_con_comentarios_se_genera_el_ast_correctamente(self):
        input_with_comments = """
        def a = 10 -- variable a
        def b = 20 -- variable b
        """

        ast_program = Program()
        ast_program.add_node(Def("a", LiteralNumberExpr(10)))
        ast_program.add_node(Def("b", LiteralNumberExpr(20)))

        parser = Parser()
        actual_ast = parser.parse(input_with_comments)
        self.assertEqual(actual_ast, ast_program)

    def test08_cuando_se_analiza_una_expresion_con_parentesis_se_genera_el_ast_correctamente(self):
        input_apply = """
        def init = print (sum 1 2)
        """

        init = Def(
            "init",
            ExprApply(
                LiteralVariableExpr('print'),
                ExprApply(
                    ExprApply(
                        LiteralVariableExpr('sum'),
                        LiteralNumberExpr(1)
                    ),
                    LiteralNumberExpr(2)
                )
            )
        )
        ast_apply = Program().add_node(init)
        parser = Parser()

        actual_ast = parser.parse(input_apply)

        self.assertEqual(ast_apply, actual_ast)

    def test09_cuando_se_analiza_una_expresion_con_un_caracter_desconocido_se_levanta_una_excepcion_de_analisis_lexico(self):
        with self.assertRaises(FlechaLangException) as context:
            Parser().parse("""def x = if ' then ' else ' """)
        self.assertEqual(context.exception.args[0], FlechaExceptionType.LEXICAL_ANALYSIS.value)

    def test10_cuando_se_analiza_una_expresion_valida_con_caracter_inesperado_se_levanta_una_excepcion_de_analisis_sintactico(self):
        with self.assertRaises(FlechaLangException) as context:
            Parser().parse("def es_par x = if x/2 == 0 then True else False|")
        self.assertEqual(context.exception.args[0], FlechaExceptionType.LEXICAL_ANALYSIS.value)



if __name__ == '__main__':
    unittest.main()
