import re
from objects import Token, IndentToken, TokenSpecification
from Lua import lua, token_specification




def tokenize_lua(code: str) -> list[Token]:
    
    def get_indent_dedent(code: str) -> list[IndentToken]:
        
        def count_startswith(string: str, startswith:str) -> int:
            c = 0
            for char in string:
                if char == startswith:c+=1
                else:
                    return c
            return c

        def indentation(line) -> int:
            x = count_startswith(line, " ")
            if x < 4: 
                return 0
            return round(x/4)
        
        lines = [line+"\n" for line in code.split("\n")]
        indents = [indentation(line) for line in lines]
        charcount = 0
        current_indents = 0
        items = []

        for index, line in enumerate(lines):
            indent = indents[index]
            if indent == 0:
                items.append(None)
            diff = indent - current_indents
            if diff > 0:
                items.append(
                    IndentToken(lua.token.INDENT, 
                                current_indents, 
                                abs(diff), 
                                charcount, 
                                "\t"))
            elif diff < 0:
                items.append(
                    IndentToken(lua.token.DEDENT, 
                                current_indents, 
                                0, 
                                charcount, 
                                ""))
            elif diff == 0:
                items.append(
                    IndentToken(lua.token.INDENT, 
                                current_indents, 
                                abs(diff), 
                                charcount, 
                                "\t"))
            current_indents = indent
            charcount+=len(line)
        
        return items

    def get_tokenmap(code) -> dict[int, Token]:
        
        tokenmap = {}
        # get all the possible tokens
        tokspec: TokenSpecification
        for tokspec in token_specification:
            find: re.Match
            for find in re.finditer(tokspec.pattern, code):
                start = find.start()
                end = find.end()
                string = code[start:end]
                ts: str = tokspec.type
                if ts == lua.token.NAME and string in lua.keyword.all():
                    ts = string.upper()
                tokenmap[start] = Token(ts, string, start, end)
        
        return tokenmap

    def list_tokens(tokenmap: dict[int, Token], codelen: int) -> list[Token]:
        
        # Collect only the tokens that dwarf other ones
        count = -1
        current_token= None
        tokens = []
        while True:
            count+=1
            if count>=codelen:
                break 
            try:
                current_token = tokenmap[count]
                count = current_token.end - 1
                tokens.append(current_token)
                continue
            except KeyError:
                current_token = code[count]
                if current_token == "\n":
                    tokens.append(Token(lua.token.NEWLINE, value="\n", start=count, end=count+1))
                    continue
                elif current_token == " ":
                    tokens.append(Token(lua.token.WHITESPACE, value=" ", start=count, end=count+1))
                    continue
                else:
                    t = Token("UNKNOWN", value=current_token, start=count, end=count+len(current_token))
                    tokens.append(t)
                    continue
        
        return tokens

    def merge_tokens(listed: list[Token], indent_dedent_list: list[IndentToken, None]) -> list[Token]:
        
        indents = iter(indent_dedent_list)
        indent = next(indents)
        merged = []
        count = -1
        length = len(listed)
        
        def progress(count, listed, length) -> Token|None:
            
            count+=1
            if count > length:
                return None
            tok = listed[count]
            
            return tok
        
        def pass_whitespaces(count, listed, tok, length) -> int:
            
            while True:
                count+=1
                try:
                    tok = listed[count]
                except IndexError:
                    break

                if tok.type != lua.token.WHITESPACE:
                    count-=1
                    break
            
            return count
        
        def resolve_current_indentation(indent: IndentToken, merged: list[Token], tok: Token) -> None:
            
            for i in range(0, indent.current_indentation):
                merged.append(Token(type=indent.type, 
                                    value=indent.value, 
                                    start=tok.start+1, 
                                    end=indent.character_count
                                    ))
            
        
        def add_dedent(indent:IndentToken, merged: list[Token], tok:Token) -> None:
            for i in range(0, indent.dedents):
                merged.append(Token(type=indent.type, 
                                    value=indent.value, 
                                    start=tok.start+1, 
                                    end=indent.character_count))
                
        def next_indent_item(count:int, indents: list[IndentToken], merged, tok, length) -> None:
            count = pass_whitespaces(count, listed, tok, length)
            try:
                indent: IndentToken = next(indents)
            except:
                return count
            if isinstance(indent, IndentToken):
                if indent.type != None:
                    if indent.current_indentation != 0:
                        resolve_current_indentation(indent, merged, tok)
                        if indent.type == lua.token.DEDENT:
                            add_dedent(indent, merged, tok)
            return count
        
        while True:
            count+=1
            try:
                tok = listed[count]
            except IndexError:
                break

            if tok.type == lua.token.NEWLINE:
                count = next_indent_item(count, indents, merged, tok, length)
                continue
            merged.append(tok)
        
        return merged

    # get the indent/dedent tokens and locations and counts first
    #inde_counts = get_indent_dedent(code)
    # get a mapping of tokens to start locations
    #tokenmap = get_tokenmap(code)
    #codelen = len(code)
    #listed_tokens = list_tokens(get_tokenmap(code), len(code))
    
    tokenmap = get_tokenmap(code)
    tokens = list_tokens(tokenmap, len(code))
    ides = get_indent_dedent(code)
    retv = merge_tokens(tokens, ides)
    return retv 

    




# Test the tokenizer
lua_code = '''
-- This is a comment

--[[
    this is a multiline
    comment
]]--

local x = 42
local y = 13.37
local str = "Hello, World!"
x = x + y
if x == y then
    
else
    
end
function foo(a, b)
    return a + b
end
'''
import time

def time_tokenizer(code):

    start = time.time()
    tokens = tokenize_lua(lua_code)
    end = time.time()
    d = end - start 
    print(f"total time: {d}")

def test():
    start = time.time()
    tokens = tokenize_lua(lua_code)
    d = time.time() - start
    for tok in tokens:
        print(tok)
    print(f"total time: {d}")

time_tokenizer(lua_code)