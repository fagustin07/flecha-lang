import os
from parser import Parser
from flecha_exception import FlechaLangException

if __name__ == "__main__":
    parser = Parser()

    filename = os.path.join(os.path.dirname(__file__), 'main.arr')
    try:
        with open(filename, 'r') as file:
            file_content = file.read()

        result = parser.parse(file_content)
        print(f'>> Análisis sintáctico finalizado, El AST que representa a su programa es:\n{result}')
    except FlechaLangException as e:
        print(e)
    except Exception as e:
        print(f'[Error inesperado] {e}')
