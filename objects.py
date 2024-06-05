from dataclasses import dataclass
from typing_extensions import TypeAlias as Alias


LuaToken: Alias = str
LuaKeyword: Alias = str
LuaLiteral: Alias = str

@dataclass
class Token:
    type: str
    value: str
    start: int
    end: int
    def __repr__(self):
        return f'''Token(
            type  = {self.type}, 
            value = {repr(self.value)}, 
            start = {self.start}, 
            end   = {self.end}
            )'''

@dataclass
class TokenSpecification:
    type: str
    pattern: str

# [lua.token.INDENT/DEDENT, current indentation, amount of dedents, charactercount]
@dataclass 
class IndentToken:
    type: str
    current_indentation: int
    dedents: int
    character_count: int
    value: str
