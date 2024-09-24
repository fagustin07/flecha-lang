import unittest

from src.abstract_syntax_tree.ast import AstNodeSequence, AstKind, AstNode, AstLeaf


class TestAstNodes(unittest.TestCase):

    def test01_un_ast_es_igual_a_otro_en_base_a_su_estructura(self):
        leaf1 = AstLeaf(AstKind.ExprVar, "x")
        leaf2 = AstLeaf(AstKind.ExprVar, "x")
        leaf3 = AstLeaf(AstKind.ExprVar, "y")

        self.assertEqual(leaf1, leaf2)
        self.assertNotEqual(leaf1, leaf3)

    def test02_un_ast_sabe_representarse_como_secuencia_de_nodos(self):
        leaf1 = AstLeaf(AstKind.ExprVar, "x")
        leaf2 = AstLeaf(AstKind.ExprVar, "y")
        apply_node = AstNode(AstKind.ExprApply, [leaf1, leaf2])
        root = AstNodeSequence(AstKind.Program, [apply_node])

        self.assertEqual(repr(root), '[["ExprApply","x","y"]]')

    def test03_una_hoja_sabe_representarse_como_numero(self):

        leaf = AstLeaf(AstKind.ExprNumber, 42)
        self.assertEqual(leaf._out(), 42)
        self.assertEqual(repr(leaf), '42')

    def test04_una_hoja_sabe_representarse_como_char(self):
        leaf = AstLeaf(AstKind.ExprChar, 'a')
        self.assertEqual(leaf._out(), 'a')
        self.assertEqual(repr(leaf), '"a"')

    def test05_un_ast_sabe_representarse_con_sus_nodos_hijos(self):
        child1 = AstLeaf(AstKind.ExprVar, "x")
        child2 = AstLeaf(AstKind.ExprVar, "y")
        node = AstNode(AstKind.ExprApply, [child1, child2])

        expected_output = [AstKind.ExprApply, "x", "y"]
        self.assertEqual(node._out(), expected_output)
        self.assertEqual(repr(node), '["ExprApply","x","y"]')

    def test06_un_ast_sabe_incorporar_nuevos_hijos(self):
        # Comprobación de añadir nodos dinámicamente
        root = AstNodeSequence(AstKind.Program, [])
        child1 = AstLeaf(AstKind.ExprVar, "x")
        child2 = AstLeaf(AstKind.ExprVar, "y")

        root.append(child1).append(child2)

        self.assertEqual(repr(root), '["x","y"]')

    def test07_un_ast_con_expr_lambda_se_representa_correctamente(self):
        # Nodo lambda con una variable 'x' y una aplicación dentro
        leaf1 = AstLeaf(AstKind.ExprVar, "x")
        leaf2 = AstLeaf(AstKind.ExprVar, "y")
        apply_node = AstNode(AstKind.ExprApply, [leaf1, leaf2])
        lambda_node = AstNode(AstKind.ExprLambda, [AstLeaf(AstKind.Params, "x"), apply_node])
        root = AstNodeSequence(AstKind.Program, [lambda_node])

        self.assertEqual(repr(root), '[["ExprLambda","x",["ExprApply","x","y"]]]')

    def test08_un_ast_con_let_se_representa_correctamente(self):
        # let x = 5 in x + y
        leaf_x = AstLeaf(AstKind.ExprVar, "x")
        leaf_y = AstLeaf(AstKind.ExprVar, "y")
        leaf_5 = AstLeaf(AstKind.ExprNumber, "5")
        binary_expr = AstNode(AstKind.ExprApply, [leaf_x, leaf_y])  # x + y
        let_node = AstNode(AstKind.ExprLet, [leaf_x, leaf_5, binary_expr])
        root = AstNodeSequence(AstKind.Program, [let_node])

        self.assertEqual(repr(root), '[["ExprLet","x","5",["ExprApply","x","y"]]]')

    def test09_un_ast_con_niveles_de_anidacion_se_sabe_representar_separando_las_anidaciones(self):
        leaf_x = AstLeaf(AstKind.ExprVar, "x")
        leaf_y = AstLeaf(AstKind.ExprVar, "y")
        leaf_z = AstLeaf(AstKind.ExprVar, "z")
        leaf_1 = AstLeaf(AstKind.ExprNumber, "1")

        plus_expr1 = AstNode(AstKind.ExprApply, [leaf_x, leaf_y])

        plus_expr2 = AstNode(AstKind.ExprApply, [leaf_z, leaf_1])

        multiply_expr = AstNode(AstKind.ExprApply, [plus_expr1, plus_expr2])

        root = AstNodeSequence(AstKind.Program, [multiply_expr])

        self.assertEqual(repr(root), '[["ExprApply",["ExprApply","x","y"],["ExprApply","z","1"]]]')

    def test10_un_ast_con_condicional_sabe_representarse(self):
        # if x then y else z
        leaf_x = AstLeaf(AstKind.ExprVar, "x")
        leaf_y = AstLeaf(AstKind.ExprVar, "y")
        leaf_z = AstLeaf(AstKind.ExprVar, "z")

        case_branch_true = AstNode(AstKind.CaseBranch, [leaf_y])  # then branch
        case_branch_false = AstNode(AstKind.CaseBranch, [leaf_z])  # else branch
        case_branches = AstNodeSequence(AstKind.CaseBranches, [case_branch_true, case_branch_false])

        case_node = AstNode(AstKind.ExprCase, [leaf_x, case_branches])
        root = AstNodeSequence(AstKind.Program, [case_node])

        self.assertEqual(repr(root), '[["ExprCase","x",[["CaseBranch","y"],["CaseBranch","z"]]]]')


if __name__ == '__main__':
    unittest.main()
