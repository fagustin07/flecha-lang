import os

from parser import Parser


if __name__ == "__main__":
    parser = Parser()
    filename = os.path.join(os.path.dirname(__file__), '..', 'inputs', '01_ops.fc')

    with open(filename, 'r') as file:
        file_content = file.read()

    result = parser.parse(file_content)
    print("Resultado del parseo:")
    print(result)