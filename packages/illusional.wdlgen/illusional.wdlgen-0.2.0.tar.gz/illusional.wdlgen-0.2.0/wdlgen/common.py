from typing import Union, List

from .types import WdlType
from .util import WdlBase


class Input(WdlBase):
    def __init__(self, data_type: WdlType, name: str, expression: str = None, requires_quotes=True):
        self.type = data_type
        self.name = name
        self.expression = expression
        self.requires_quotes = requires_quotes

        self.format = "{type} {name}{def_w_equals}"

    def get_string(self):
        if self.type is None:
            raise Exception(f"Could not convert wdlgen.Input ('{self.name}') to string because type was null")

        wd = self.type.get_string()
        if isinstance(wd, list):
            return self.get_string_from_type(wd[0])
        return self.get_string_from_type(wd)

    def get_string_from_type(self, wdtype):
        expression = self.expression
        requires_quotes = self.requires_quotes and not (expression is None or
                                                        isinstance(expression, bool) or
                                                        isinstance(expression, int) or
                                                        isinstance(expression, float))

        if isinstance(expression, bool):
            expression = "true" if expression else "false"

        if requires_quotes:
            expression = f'"{expression}"'

        return self.format.format(
            type=wdtype,
            name=self.name,
            def_w_equals=((" = " + expression) if expression is not None else "")
        )


class Output(WdlBase):
    def __init__(self, data_type: WdlType, name: str, expression: str = None):
        self.type = data_type
        self.name = name
        self.expression = expression

    def get_string(self):
        f = "{type} {name}{def_w_equals}"
        if isinstance(self.type, list):
            return [
                f.format(
                    type=self.type[i].get_string(),
                    name=self.name + ("" if i == 0 else "_" + str(i)),
                    def_w_equals=(" = {val}".format(val=self.expression) if self.expression else ""))
                for i in range(len(self.type))]

        wd = self.type.get_string()
        if isinstance(wd, list):

            return [f.format(
                type=t,
                name=self.name,
                def_w_equals=(" = {val}".format(val=self.expression) if self.expression else "")
            ) for t in wd]
        return f.format(
                type=wd,
                name=self.name,
                def_w_equals=(" = {val}".format(val=self.expression) if self.expression else "")
            )
