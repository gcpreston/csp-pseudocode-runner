def main():
    filename = "pseudocode/code.txt"
    try:
        with open(filename) as file:
            code = file.read()
        
        # change code to Python
        code = transcode(code)
               
        # execute the newly created Python code
        exec(code)
        
    except FileNotFoundError:
        print(filename + " not found.")
        
def transcode(code):
    # fix indentation
    code = code.replace('\t', '')
    
    layers = 0
    for i in range(len(code)):
        if code[i] == '{':
            layers += 1
        elif code[i] == '}':
            layers -= 1
        elif code[i] == '\n' and layers > 0:
            if code[i+1] == '}':
                code = code[:i+1] + ('\t' * (layers - 1)) + code[i+1:]
            else:
                code = code[:i+1] + ('\t' * layers) + code[i+1:]
          
    # fix odd characters
    # NOTE: greater than and less than symbols must be fixed in the original file
    # greater than: >=, less than: <=
    for i in range(len(code)):
        if ord(code[i]) == 8592:
            code = code[:i] + '<-' + code[i+1:]
        elif ord(code[i]) == 8800:
            code = code[:i] + '!=' + code[i+1:]
            
    # change syntax
    if "RANDOM" in code:
        code = "import random\n" + code
    
    replacements = {
        ' = '          : ' == ',
        '<-'           : '=',
        '\n{'          : ':',
        ' {'           : ':',
        '}'            : '',
        "DISPLAY"      : "print",
        " AND "        : " and ",
        " OR "         : " or ",
        "NOT"          : "not",
        "MOD"          : "%",
        "IF"           : "if",
        "ELSE"         : "else",
        "PROCEDURE"    : "def",
        "FOR EACH"     : "for",
        "REPEAT UNTIL" : "while not",
        " IN "         : " in ",
        "RETURN"       : "return",
        "INPUT"        : "input",
        "LENGTH"       : "len",
        "RANDOM"       : "random.randint"
    }
    
    equals_replaced = False
    for r in replacements:
        if not (r == ' = ' and equals_replaced):
            code = code.replace(r, replacements[r])
        if r == ' = ':
            equals_replaced = True
    
    for i in range(len(code)):
        if code[i:i+6] == "REPEAT":
            line = code[i:]
            index = line.index('\n')
            times = int(line[:index].split()[1])
            
            new_line = f"for i in range({times}):"
            
            code = code[:i] + new_line + code[i+index:]
        
        elif code[i:i+6] == "APPEND":
            params_s = code[i:]
            index = params_s.index('\n')
            params_s = params_s[params_s.index('(')+1:index - 1]
            
            params = find_params(params_s)
            append_py = f"{params[0]}.append({params[1]})"
            
            code = code[:i] + append_py + code[i+index:]   
        
        elif code[i:i+6] == "REMOVE":
            params_s = code[i:]
            index = params_s.index('\n')
            params_s = params_s[params_s.index('(')+1:index - 1]
            
            params = find_params(params_s)
            remove_py = f"del {params[0]}[{params[1]}]"
            
            code = code[:i] + remove_py + code[i+index:]
            
        elif code[i:i+6] == "INSERT":
            params_s = code[i:]
            index = params_s.index('\n')
            params_s = params_s[params_s.index('(')+1:index - 1]
            
            params = find_params(params_s)
            insert_py = f"{params[0]}.insert({params[1]}, {params[2]})"
            
            code = code[:i] + insert_py + code[i+index:]
        
    return code
        
def find_params(s):
    params = []
    
    ignore = False
    i = 0
    while i < len(s):
        if s[i] == '(':
            ignore = True
        elif s[i] == ')':
            ignore = False
            
        if ((not ',' in s and len(s) > 0) or
            (i == len(s) - 1 and len(s) > 0)):
            params.append(s)
            break
        
        if s[i] == ',' and not ignore:
            params.append(s[:i].strip())
            s = s[i+1:]
            i = -1
        i += 1
        
    return params
        
if __name__ == '__main__':
    main()