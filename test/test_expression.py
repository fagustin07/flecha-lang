from abstract_syntax_tree.expression import ExprApply, LiteralCharExpr, LiteralConstructorExpr, ExprLambda, ExprLet, \
    LiteralVariableExpr, FlechaFactoryExpression
import unittest


class TestExpression(unittest.TestCase):

    def setUp(self):
        self.factory = FlechaFactoryExpression()

    def test01_se_genera_el_constructor_de_lista_vacia_al_recibir_un_string_vacio(self):
        result = self.factory.charlist_from_string("")

        expected = LiteralConstructorExpr('Nil')

        self.assertEqual(expected, result)

    def test02_se_genera_una_lista_de_caracteres_al_recibir_un_string(self):
        result = self.factory.charlist_from_string("abc")

        expected = ExprApply(
            ExprApply(LiteralConstructorExpr('Cons'), LiteralCharExpr('a')),
            ExprApply(
                ExprApply(LiteralConstructorExpr('Cons'), LiteralCharExpr('b')),
                ExprApply(
                    ExprApply(LiteralConstructorExpr('Cons'), LiteralCharExpr('c')),
                    LiteralConstructorExpr('Nil')
                )
            )
        )

        self.assertEqual(expected, result)

    def test03_si_no_hay_parametros_entonces_se_toma_la_expresion_a_derecha(self):
        expr = ExprLambda(LiteralVariableExpr('x'), LiteralVariableExpr('x'))

        result = self.factory.expression_with_params([], expr)

        self.assertEqual(result, expr)

    def test04_cuando_hay_un_parametro_entonces_se_genera_una_expresion_lambda(self):
        expr = ExprLambda(LiteralVariableExpr('x'), LiteralVariableExpr('x'))

        result = self.factory.expression_with_params([LiteralVariableExpr('y')], expr)

        expected = ExprLambda(LiteralVariableExpr('y'), expr)
        self.assertEqual(expected, result)

    def test05_cuando_hay_mas_de_un_parametro_entonces_se_anidan_lambdas(self):
        expr = ExprLambda(LiteralVariableExpr('x'), LiteralVariableExpr('x'))

        result = self.factory.expression_with_params([LiteralVariableExpr('y'), LiteralVariableExpr('z')], expr)

        expected = ExprLambda(LiteralVariableExpr('y'), ExprLambda(LiteralVariableExpr('z'), expr))
        self.assertEqual(expected, result)

    def test06_cuando_hay_una_secuencia_de_expresiones_entonces_se_traduce_a_un_let_que_ignora_el_argumento(self):
        expr1 = ExprLambda(LiteralVariableExpr('x'), LiteralVariableExpr('x'))
        expr2 = ExprLambda(LiteralVariableExpr('y'), LiteralVariableExpr('y'))

        result = self.factory.seq_expr_with_expressions(expr1, expr2)

        expected = ExprLet(self.factory.empty_id(), expr1, expr2)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
