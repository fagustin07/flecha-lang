import os

from parser import Parser


if __name__ == "__main__":
    parser = Parser()

    filename = os.path.join(os.path.dirname(__file__), 'main.arr')
    with open(filename, 'r') as file:
        file_content = file.read()

    result = parser.parse(file_content)
    print(">> Analisis sintáctico finalizado, El significado de su programa es:\n\n")
    print(result)
