from regex import Str, Num, KeywordPatterns, Operators
from objects import TokenSpecification
import re


class lua:
                
    class token:
        KEYWORD = "KEYWORD"
        NUMBER = "NUMBER"
        STRING = "STRING"
        OPERATOR = "OPERATOR"
        COMMENT = "COMMENT"
        WHITESPACE = "WHITESPACE"
        NEWLINE = "NEWLINE"
        INDENT = "INDENT"
        DEDENT = "DEDENT"
        EOF = "EOF"
        PUNCTUATION = "PUNCTUATION"
        NAME = "NAME"
        AND = "AND"
        BREAK = "BREAK"
        DO = "DO"
        ELSE = "ELSE"
        ELSEIF = "ELSEIF"
        END = "END"
        FALSE = "FALSE"
        FOR = "FOR"
        FUNCTION = "FUNCTION"
        GOTO = "GOTO"
        IF = "IF"
        IN = "IN"
        LOCAL = "LOCAL"
        NIL = "NIL"
        NOT = "NOT"
        OR = "OR"
        REPEAT = "REPEAT"
        RETURN = "RETURN"
        THEN = "THEN"
        TRUE = "TRUE"
        UNTIL = "UNTIL"
        WHILE = "WHILE"
        LPAREN = "LPAREN"
        RPAREN = "RPAREN"
        LBRACKET = "LBRACKET"
        RBRACKET = "RBRACKET"
        LBRACE = "LBRACE"
        RBRACE = "RBRACE"
        types = None
    
    class keyword:
        AND = "and"
        BREAK = "break"
        DO = "do"
        ELSE = "else"
        ELSEIF = "elseif"
        END = "end"
        FALSE = "false"
        FOR = "for"
        FUNCTION = "function"
        GOTO = "goto"
        IF = "if"
        IN = "in"
        LOCAL = "local"
        NIL = "nil"
        NOT = "not"
        OR = "or"
        REPEAT = "repeat"
        RETURN = "return"
        THEN = "then"
        TRUE = "true"
        UNTIL = "until"
        WHILE = "while"

        @staticmethod
        def all() -> list:
            return [lua.keyword.AND, lua.keyword.BREAK, lua.keyword.DO, lua.keyword.ELSE, lua.keyword.ELSEIF, lua.keyword.END, lua.keyword.FALSE, lua.keyword.FOR, lua.keyword.FUNCTION, lua.keyword.GOTO, lua.keyword.IF, lua.keyword.IN, lua.keyword.LOCAL, lua.keyword.NIL, lua.keyword.NOT, lua.keyword.OR, lua.keyword.REPEAT, lua.keyword.RETURN, lua.keyword.THEN, lua.keyword.TRUE, lua.keyword.UNTIL, lua.keyword.WHILE]
        @staticmethod
        def iskeyword(string: str) -> bool:
            return string in lua.keyword.all()
        
    class literal:
        LEFTPAREN = "("
        RIGHTPAREN = ")"
        LEFTBRACKET = "{"
        RIGHTBRACKET = "}"
        LEFTBRACE = "]"
        RIGHTBRACE = "["
        QUOTE = "'"
        DOUBLEQUOTE = '"'
        PLUS = "+"
        MINUS = "-"
        STAR = "*"
        FORWARDSLASH = "/"
        PERCENT = "%"
        CARET = "^"
        HASHTAG = "#"
        AMPERSAND = "&"
        TILDE = "~"
        PIPE = "|"
        LSHIFT = "<<"
        RSHIFT = ">>"
        DOUBLEFORWARDSLASH = "//"
        DOUBLEEQUALS = "=="
        TILDEEQUALS = "~="
        LESSTHANEQUALS = "<="
        MORETHANEQUALS = ">="
        GREATERTHAN = ">"
        LESSTHAN = "<"
        EQUALS = "="
        SEMICOLON = ";"
        COLON = ":"
        DOUBLECOLON = "::"
        COMMA = ","
        DOT = "."
        DOTDOT = ".."
        DOTDOTDOT = "..."

    class arithmetic:
        ADD = "+"
        SUBTRACT = "-"
        MULTIPLY = "*"
        FLOAT_DIVISION = "/"
        FLOOR_DIVISION = "//"
        MODULO = "%"
        EXPONENT = "^"
        NEGATE = "-"
    
    ARITHMETICS = [arithmetic.ADD, arithmetic.SUBTRACT, arithmetic.MULTIPLY, 
                   arithmetic.FLOAT_DIVISION, arithmetic.FLOOR_DIVISION, arithmetic.MODULO,
                   arithmetic.EXPONENT, arithmetic.NEGATE]

    class bitwise:
        LSHIFT = "<<"
        RSHIFT = ">>"
        AND = "&"
        XOR = "~"
        UNOT = "~"
    
    class relational:
        EQUALITY = "=="
        INEQUALITY = "~="
        LESSTHAN = "<"
        GREATERTHAN = ">"
        GTE = ">="
        LTE = "<="

    class logical:
        AND = "and"
        OR = "or"
        NOT = "not"
        
    class object:
        ACCESS = "."
        CONCAT = ".."
        LENGTH = "#"
        ASSIGN = "="


LUA_KEYWORDS = [
    "and", "break", "do", "else", "elseif", "end", "false", "for",
    "function", "goto", "if", "in", "local", "nil", "not", "or",
    "repeat", "return", "then", "true", "until", "while", "require"
]


specification_token_indent = TokenSpecification(lua.token.INDENT, r"\t")
spcification_token_dedent =  TokenSpecification(lua.token.DEDENT, ""   )

token_specification = [
    TokenSpecification(lua.token.COMMENT,     r'--.*\n'                              ),                  # Single line comment
    TokenSpecification(lua.token.STRING,      Str                                    ),                        # String literals
    TokenSpecification(lua.token.COMMENT,     re.compile(r'--\[\[.*\]\]--', re.DOTALL)),          # Multi Line Comment
    TokenSpecification(lua.token.KEYWORD,     KeywordPatterns                        ),
    TokenSpecification(lua.token.NUMBER,      Num                                    ),                        # Integer or decimal number
    TokenSpecification(lua.token.NAME,        r'\b[A-Za-z_][A-Za-z0-9_]*\b'          ),  # Identifiers
    TokenSpecification(lua.token.OPERATOR,    Operators                              ),                  # Lua operators
    TokenSpecification(lua.token.LBRACKET,    r"\{"                                  ),
    TokenSpecification(lua.token.RBRACKET,    r"\}"                                  ),
    TokenSpecification(lua.token.LBRACE,      r"\["                                  ),
    TokenSpecification(lua.token.RBRACE,      r"\]"                                  ),
    TokenSpecification(lua.token.LPAREN,      r"\("                                  ),
    TokenSpecification(lua.token.RPAREN,      r"\)"                                  ),
    TokenSpecification(lua.token.NEWLINE,     r"\n"                                  ),
]

lua.token.types = [spec.type for spec in token_specification]
lua.token.types.extend([specification_token_indent, spcification_token_dedent])
