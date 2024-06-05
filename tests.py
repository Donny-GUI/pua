from tokenizer import tokenize_lua
import os

desktop = f"C:\\Users\\{os.getlogin()}\\Desktop"

def collect(file_extension):
    retv = []
    for root, dirs, files in os.walk(desktop):
        for file in files:
            if file.endswith(file_extension):
                retv.append(os.path.join(root, file))
    return retv


def tokenizer_test():
    files = collect(".lua")
    passes = 0
    for file in files:
        print("\033[31m FILE  \033[0m", file)
        with open(file, "r", errors="ignore", encoding="utf-8") as f:
            content = f.read()
        tokens = tokenize_lua(content)
        buffer = []
        for token in tokens:
            if token.type == "UNKNOWN":
                buffer.append(token.value)
        if len(buffer) == 0:
            print("\033[42m  PASS  \033[0m")
            passes+=1
        else:
            print("\033[41m  FAIL  \033[0m")
        print("".join(buffer))

    print(f"{passes}/{len(files)} tokenized successfully")

tokenizer_test()