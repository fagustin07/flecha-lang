import os

from parser import Parser


if __name__ == "__main__":
    parser = Parser()

    filename = os.path.join('./main.arr')
    with open(filename, 'r') as file:
        file_content = file.read()

    result = parser.parse(file_content)
    print("Resultado del parseo:")
    print(result)
