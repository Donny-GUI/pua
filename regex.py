import re

# MACROS
def oneOrNone(pattern):return rf"{pattern}?"
def group(*choices): return '(' + '|'.join(choices) + ')'
def any(*choices): return group(*choices) + '*'
def maybe(*choices): return group(*choices) + '?'
def rightBefore(this, that):
    """ capture `this` pattern, only if it comes right before
    `that` pattern. 

    Args:
        this (str): capture this pattern
        that (str): recognize that pattern is after `this`

    Returns:
        str: regex pattern for matching `this` if it comes right before `that` pattern
    """
    return rf"{this}(?={that})"
def rightAfter(this, that):return rf"(?={that}){this}"
def spacedBefore(this, that):return rf"{this}(?=\s{that})"
def spacedAfter(that, this):return rf"(?={that}\s){this}"

def insideParentheses(this):return rf"\((\s*{this}\s*)\)"
def insideBrackets(this):return r"\{" + rf"(\s*{this}\s*)" + r"\}"
def insideBraces(this):return r"\[" + rf"(\s*{this}\s*)" + r"\]"
def thisIndexed(this):return rf"{this}\[.*\]"
def asAttribute(object, attribute):return rf"{object}\.{attribute}"
def asMethod(this): return rf"[A-Za-z][A-Za-z0-9_]*\.{this}\(.*\)"
def equalsAnything(this): return rightBefore(this, r"\s*\=\s*.*\n")
def asVariableAssignment(this): return rf"{this}\s*\=\s*"
esc = re.escape
def once(char):return rf"{esc(char)}(?!{esc(char)})"
def twice(char: str):return rf"{esc(char)}{esc(char)}(?!{esc(char)})"
def thrice(char: str):return rf"{esc(char)}{esc(char)}{esc(char)}(?!{esc(char)})"



IntegerConstant1 = r"0[xX](?:_?[a-f][a-f])+" # 0xff
IntegerConstant2 = r"0[xX](?:_?[A-F])+"      # 0xBEBADA
Hexnumber = r'0[xX](?:_?[0-9a-fA-F])+'
Binnumber = r'0[bB](?:_?[01])+'
Octnumber = r'0[oO](?:_?[0-7])+'
Decnumber = r'(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
Intnumber = group(Hexnumber, Binnumber, Octnumber, Decnumber)
Exponent = r'[eE][-+]?[0-9](?:_?[0-9])*'
Pointfloat = group(r'[0-9](?:_?[0-9])*\.(?:[0-9](?:_?[0-9])*)?', r'\.[0-9](?:_?[0-9])*') + maybe(Exponent)
Expfloat = r'[0-9](?:_?[0-9])*' + Exponent
Floatnumber = group(Pointfloat, Expfloat)
Whitespace = r'[ \f\t]*'
Ignore = Whitespace + any(r'\\\r?\n' + Whitespace)
Imagnumber = group(r'[0-9](?:_?[0-9])*[jJ]', Floatnumber + r'[jJ]')
ConString = group(r"'[^\n'\\]*(?:\\.[^\n'\\]*)*" + group("'", r'\\\r?\n'), 
                   r'"[^\n"\\]*(?:\\.[^\n"\\]*)*' +group('"', r'\\\r?\n'))
String1 = r"\'.*\'"
String2 = r'\".*\"'
InsideParentheses = r'\((.*?)\)'


Num = group(Imagnumber, Floatnumber, Intnumber)
Str = group(String1, String2)
KeywordPatterns = group("and", "break", "do", "else", "elseif", "end", "false", "for",
    "function", "goto", "if", "in", "local", "nil", "not", "or",
    "repeat", "return", "then", "true", "until", "while")

Operators = group(
    once(r"+"), 
    once(r"-"), 
    once(r"*"), 
    once(r"/"), 
    once(r"%"), 
    once(r"^"), 
    once(r"#"), 
    once(r"&"), 
    once(r"~"), 
    once(r"|"), 
    twice(r"<"), 
    twice(r">"), 
    twice(r"/"), 
    twice(r"="),
    r"\~\=", 
    r"\<\=", 
    r"\>\=", 
    once(r"<"), 
    once(r">"), 
    once(r"="), 
    twice(r":"), 
    once(r";"), 
    once(r":"), 
    once(r","), 
    once(r"."),
    twice(r"."), 
    thrice(r".") 
)