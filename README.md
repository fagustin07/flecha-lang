# flecha-parser


## Gramatica base

<programa> → ε
| <programa> <definición>

<definición> → (DEF) (LOWERID) <parámetros> (DEFEQ) <expresión>

<parámetros> → ε
| (LOWERID) <parámetros>

<expresión> → <expresiónExterna>
| <expresiónExterna> (SEMICOLON) <expresión>

<expresiónExterna> → <expresiónIf>
| <expresiónCase>
| <expresiónLet>
| <expresiónLambda>
| <expresiónInterna>

<expresiónIf> → (IF) <expresiónInterna> (THEN) <expresiónInterna> <ramasElse>

<ramasElse> → (ELIF) <expresiónInterna> (THEN) <expresiónInterna> <ramasElse>
| (ELSE) <expresiónInterna>
| ε

<expresiónCase> → (CASE) <expresiónInterna> <ramasCase>

<ramasCase> → ε
| <ramaCase> <ramasCase>

<ramaCase> → (PIPE) (UPPERID) (ARROW) <expresiónInterna>

<expresiónLet> → (LET) (ID) <parámetros> (DEFEQ) <expresiónInterna> (IN) <expresiónExterna>

<expresiónLambda> → (LAMBDA) <parámetros> (ARROW) <expresiónExterna>

<expresiónInterna> → <expresiónAplicación>
| <expresiónInterna> <operadorBinario> <expresiónInterna>
| <operadorUnario> <expresiónInterna>

<operadorBinario> → (AND)
| (OR)
| (EQ)
| (NE)
| (GE)
| (LE)
| (GT)
| (LT)
| (PLUS)
| (MINUS)
| (TIMES)
| (DIV)
| (MOD)

<operadorUnario> → (NOT)
| (MINUS)

<expresiónAplicación> → <expresiónAtómica>
| <expresiónAplicación> <expresiónAtómica>

<expresiónAtómica> → (LOWERID)
| (UPPERID)
| (NUMBER)
| (CHAR)
| (STRING)
| (LPAREN) <expresión> (RPAREN)
