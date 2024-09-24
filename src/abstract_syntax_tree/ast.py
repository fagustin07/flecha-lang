import json
from enum import Enum
from typing import Sequence


class AstKind(Enum):
    Program = "Program"
    Def = "Def"
    ExprVar = "ExprVar"
    ExprConstructor = "ExprConstructor"
    ExprNumber = "ExprNumber"
    ExprChar = "ExprChar"
    ExprCase = "ExprCase"
    ExprLet = "ExprLet"
    ExprLambda = "ExprLambda"
    ExprApply = "ExprApply"
    CaseBranch = "CaseBranch"
    CaseBranches = ""
    Id = "Id"
    Params = "Params"


jsonConfig = dict(separators=(',', ':'), default=lambda obj: obj.value)


def flecha_json_encode(out):
    return json.dumps(out, **jsonConfig)


AstNodeOutput = int | str | Sequence['AstNodeOutput']


class AstNode:

    def __init__(self, kind: AstKind, children):
        self.value = None
        self.kind = kind
        self.children: list['AstNode'] = children

    def add_node(self, child: 'AstNode') -> 'AstNode':
        self.children.append(child)
        return self

    def _out(self):
        return [self.kind] + self._children_out()

    def _children_out(self):
        return [c._out() for c in self.children]

    def __repr__(self) -> str:
        return flecha_json_encode(self._out())

    def __eq__(self, __o: object) -> bool:
        return self.__repr__() == __o.__repr__()


class AstLeaf(AstNode):
    def __init__(self, kind: AstKind, value):
        super().__init__(kind, None)
        self.value = value

    def _out(self) -> AstNodeOutput:
        return self.value


class AstSequence(AstNode):
    def __init__(self, kind: AstKind, nodes: Sequence[AstNode]):
        super().__init__(kind, nodes)

    def _out(self) -> AstNodeOutput:
        return self._children_out() if self.children else []
