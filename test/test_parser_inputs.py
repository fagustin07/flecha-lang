import os
import json
import unittest

from parser import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
        self.input_dir = os.path.join(os.path.dirname(__file__), 'inputs')

    def test_el_analizador_lexico_genera_los_ast_esperados(self):
        test_cases = [f for f in os.listdir(self.input_dir) if f.endswith('.input')]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                base_name = test_case.split('.')[0]
                flecha_input_file = os.path.join(self.input_dir, f'{base_name}.input')
                expected_json_file = os.path.join(self.input_dir, f'{base_name}.expected')

                with open(expected_json_file, 'r') as f:
                    expected_ast = json.dumps(json.load(f), separators=(',', ':'))
                with open(flecha_input_file, 'r') as f:
                    flecha_code = f.read()

                actual_ast = self.parser.parse(flecha_code)

                self.assertEqual(expected_ast, repr(actual_ast),
                                 msg=f"Fallo de analisis sintáctico en el archivo {flecha_input_file}: El parser no genera el output esperado.")


if __name__ == '__main__':
    unittest.main()
