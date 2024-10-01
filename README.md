# Lenguaje Flecha

## Requerimientos

Este proyecto está desarrollado con Python 3.10.

Para correr el proyecto debemos tener instalado
- Python 3.10.
- El package-management para Python (pip).

Luego, para instalar el resto de las bibliotecas, correr `pip install -r dependencias.txt` en el root del proyecto.

_Tengamos en cuenta que los comandos en python para documentados aquí, utilizamos la entrada `python3`. Podría pasarnos que tengamos en nuestro sistema la entrada de python como `py`, o bien, `python`._

## TP1: Analizador léxico y sintáctico

### Casos de prueba
Los archivos .input (código escrito en Flecha), y los archivos .expected (JSON que describe el AST esperado), se encuentran en `/test/inputs/`, y en `/test/test_parser_inputs.py` se encuentra descripto un test que, por cada archivo en dicho directorio, lee la entrada en Flecha, se la envía al analizador sintáctico, y luego compara el resultado con el JSON correspondiente a dicho input.

Luego, hay varios archivos con casos de prueba que fueron útiles para el desarrollo incremental del proyecto.

Para correr todos los test, debemos correr ` python3 -m unittest discover`

### Correr el proyecto

Por otro lado, también podemos correr nuestro propio código en Flecha y generar los AST de dicho análisis. Para esto, hay un archivo `/src/main.arr`, el cual podemos modificar con nuestro propio código y ejecutar el análisis sintáctico del código ejecutando `python3 ./src/main.py `. La salida será el resultado del análisis sintáctico del codigo en `main.arr`.


### Contexto sobre el desarrollo del TP1

Se comenzó desarrollando con el lenguaje Go nuestro propio `lexer`, pero luego de consultas en clases, se intentó cambiar por `antlr4` para poder desarrollar con mayor rapidez; no se pudo adaptar el parser de generado a el lexer propio, por lo que se comenzó de cero el proyecto utilizando Python con la biblioteca PLY.