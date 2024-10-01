from enum import Enum


class FlechaExceptionType(Enum):
    LEXICAL_ANALYSIS = "[Error lexico]"
    SYNTACTIC_ANALYSIS = "[Error sintactico]"


class FlechaLangException(RuntimeError):
    def __init__(self, exception_type: FlechaExceptionType, message):
        super().__init__(f'{exception_type.value} {message}')

