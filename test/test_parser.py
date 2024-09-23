import unittest
from src.parser import Parser


class ParserTest(unittest.TestCase):

    def test01_cuando_se_analiza_sintacticamente_una_expresion_secuenciacion_entonces_se_genera_ast_de_let(self):
        input_seq = """
        def main = print "hola\n"; print "chau\n"
        """

        ast_let = [
            ['Def',
             'main',
             ['LetExpr',
              '_',
              ['ExprApply', ['ExprVar', 'print'], ['ExprString', 'hola\n']],
              ['ExprApply', ['ExprVar', 'print'], ['ExprString', 'chau\n']]]]]

        parser = Parser()
        seq_ast = parser.parse(input_seq)

        self.assertEqual(seq_ast, ast_let)

    def test02_cuando_se_reciben_deficiniones_entonces_se_genera_el_ast_correspondiente(self):
        input_program = """
            -- Numeros
            def uno = 1
            def dos =2--comentario
            def tres= 3  -- otro comentario
            def
            cuatro=4--comentario
            def cinco = 5 def seis = 6def siete = 7
              def
                ocho
                  =
                     8 def
            nueve
            =9
            def cero=0
            def cerocero=00
            def cerocerocero=000
            def def_=10
            def ifthenelse=11
            def p_r_u_e_b_a=1987654321
            def camelCase=12
            def x1 = 11
            def x2 = 12
        """

        expected_ast = [
            ["Def", "uno",
             ["ExprNumber", 1]
             ],
            ["Def", "dos",
             ["ExprNumber", 2]
             ],
            ["Def", "tres",
             ["ExprNumber", 3]
             ],
            ["Def", "cuatro",
             ["ExprNumber", 4]
             ],
            ["Def", "cinco",
             ["ExprNumber", 5]
             ],
            ["Def", "seis",
             ["ExprNumber", 6]
             ],
            ["Def", "siete",
             ["ExprNumber", 7]
             ],
            ["Def", "ocho",
             ["ExprNumber", 8]
             ],
            ["Def", "nueve",
             ["ExprNumber", 9]
             ],
            ["Def", "cero",
             ["ExprNumber", 0]
             ],
            ["Def", "cerocero",
             ["ExprNumber", 0]
             ],
            ["Def", "cerocerocero",
             ["ExprNumber", 0]
             ],
            ["Def", "def_",
             ["ExprNumber", 10]
             ],
            ["Def", "ifthenelse",
             ["ExprNumber", 11]
             ],
            ["Def", "p_r_u_e_b_a",
             ["ExprNumber", 1987654321]
             ],
            ["Def", "camelCase",
             ["ExprNumber", 12]
             ],
            ["Def", "x1",
             ["ExprNumber", 11]
             ],
            ["Def", "x2",
             ["ExprNumber", 12]
             ]
        ]

        parser = Parser()
        actual_ast = parser.parse(input_program)
        self.assertEqual(actual_ast, expected_ast)

    def test03_cuando_se_reciben_deficiniones_con_mas_de_un_parametro_entonces_se_genera_un_ast_con_expresiones_lambda(self):
        input_seq = """

def null list =
  case list
  | Nil       -> True
  | Cons x xs -> False

def head list =
  case list
  | Cons x xs -> x

def tail list =
  case list
  | Cons x xs -> xs

def take n list =
  if n == 0 || null list
   then Nil
   else Cons (head list) (take (n - 1) (tail list))

def sum list =
  if null list
   then 0
   else head list + tail list

def gen n =
  if n == 0
   then Nil
   else Cons n (gen (n - 1))

def main =
  sum (gen 100)
        """

        ast_let = [
            ["Def", "null",
             ["ExprLambda", "list",
              ["ExprCase",
               ["ExprVar", "list"],
               [
                   ["CaseBranch", "Nil", [],
                    ["ExprConstructor", "True"]
                    ],
                   ["CaseBranch", "Cons", ["x", "xs"],
                    ["ExprConstructor", "False"]
                    ]
               ]
               ]
              ]
             ],
            ["Def", "head",
             ["ExprLambda", "list",
              ["ExprCase",
               ["ExprVar", "list"],
               [
                   ["CaseBranch", "Cons", ["x", "xs"],
                    ["ExprVar", "x"]
                    ]
               ]
               ]
              ]
             ],
            ["Def", "tail",
             ["ExprLambda", "list",
              ["ExprCase",
               ["ExprVar", "list"],
               [
                   ["CaseBranch", "Cons", ["x", "xs"],
                    ["ExprVar", "xs"]
                    ]
               ]
               ]
              ]
             ],
            ["Def", "take",
             ["ExprLambda", "n",
              ["ExprLambda", "list",
               ["ExprCase",
                ["ExprApply",
                 ["ExprApply",
                  ["ExprVar", "OR"],
                  ["ExprApply",
                   ["ExprApply",
                    ["ExprVar", "EQ"],
                    ["ExprVar", "n"]
                    ],
                   ["ExprNumber", 0]
                   ]
                  ],
                 ["ExprApply",
                  ["ExprVar", "null"],
                  ["ExprVar", "list"]
                  ]
                 ],
                [
                    ["CaseBranch", "True", [],
                     ["ExprConstructor", "Nil"]
                     ],
                    ["CaseBranch", "False", [],
                     ["ExprApply",
                      ["ExprApply",
                       ["ExprConstructor", "Cons"],
                       ["ExprApply",
                        ["ExprVar", "head"],
                        ["ExprVar", "list"]
                        ]
                       ],
                      ["ExprApply",
                       ["ExprApply",
                        ["ExprVar", "take"],
                        ["ExprApply",
                         ["ExprApply",
                          ["ExprVar", "SUB"],
                          ["ExprVar", "n"]
                          ],
                         ["ExprNumber", 1]
                         ]
                        ],
                       ["ExprApply",
                        ["ExprVar", "tail"],
                        ["ExprVar", "list"]
                        ]
                       ]
                      ]
                     ]
                ]
                ]
               ]
              ]
             ],
            ["Def", "sum",
             ["ExprLambda", "list",
              ["ExprCase",
               ["ExprApply",
                ["ExprVar", "null"],
                ["ExprVar", "list"]
                ],
               [
                   ["CaseBranch", "True", [],
                    ["ExprNumber", 0]
                    ],
                   ["CaseBranch", "False", [],
                    ["ExprApply",
                     ["ExprApply",
                      ["ExprVar", "ADD"],
                      ["ExprApply",
                       ["ExprVar", "head"],
                       ["ExprVar", "list"]
                       ]
                      ],
                     ["ExprApply",
                      ["ExprVar", "tail"],
                      ["ExprVar", "list"]
                      ]
                     ]
                    ]
               ]
               ]
              ]
             ],
            ["Def", "gen",
             ["ExprLambda", "n",
              ["ExprCase",
               ["ExprApply",
                ["ExprApply",
                 ["ExprVar", "EQ"],
                 ["ExprVar", "n"]
                 ],
                ["ExprNumber", 0]
                ],
               [
                   ["CaseBranch", "True", [],
                    ["ExprConstructor", "Nil"]
                    ],
                   ["CaseBranch", "False", [],
                    ["ExprApply",
                     ["ExprApply",
                      ["ExprConstructor", "Cons"],
                      ["ExprVar", "n"]
                      ],
                     ["ExprApply",
                      ["ExprVar", "gen"],
                      ["ExprApply",
                       ["ExprApply",
                        ["ExprVar", "SUB"],
                        ["ExprVar", "n"]
                        ],
                       ["ExprNumber", 1]
                       ]
                      ]
                     ]
                    ]
               ]
               ]
              ]
             ],
            ["Def", "main",
             ["ExprApply",
              ["ExprVar", "sum"],
              ["ExprApply",
               ["ExprVar", "gen"],
               ["ExprNumber", 100]
               ]
              ]
             ]
        ]

        parser = Parser()
        seq_ast = parser.parse(input_seq)

        self.assertEqual(seq_ast, ast_let)


if __name__ == '__main__':
    unittest.main()
