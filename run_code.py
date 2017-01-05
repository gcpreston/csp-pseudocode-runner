def main():
    filename = "code.txt"
    try:
        with open(filename) as file:
            code = file.read()
        
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
            ' = '          : '==',
            '<-'           : '=',
            '\n{'          : ':',
            ' {'           : ':',
            '}'            : '',
            "DISPLAY"      : "print",
            "AND"          : "and",
            "OR"           : "or",
            "NOT"          : "not",
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
            if r == ' = ':
                equals_replaced = True
            if not (r == ' = ' and equals_replaced):
                code = code.replace(r, replacements[r])
        
        for i in range(len(code)):
            if code[i:i+6] == "APPEND":
                param_open, param_close = find_params(code, i, 6)

                list_name, value = [p.strip() for p in code[i+param_open:i+param_close].split(',')]
                append_py = f"{list_name}.append({value})"
                
                code = code[:i] + append_py + code[i+param_close+1:]
            
            elif code[i:i+6] == "REMOVE":
                param_open, param_close = find_params(code, i, 6)

                params = [p.strip() for p in code[i+param_open:i+param_close].split(',')]
                remove_py = f"del {params[0]}[{params[1]}]"
                
                code = code[:i] + remove_py + code[i+param_close+1:]
                
            elif code[i:i+6] == "INSERT":
                param_open, param_close = find_params(code, i, 6)

                params = [p.strip() for p in code[i+param_open:i+param_close].split(',')]
                insert_py = f"{params[0]}.insert({params[1]}, {params[2]})"
                
                code = code[:i] + insert_py + code[i+param_close+1:]
               
        # execute the newly created Python code
        exec(code)
        
    except FileNotFoundError:
        print(filename + " not found.")
        
def find_params(s, i, j):
    parameter_open = 0
    while s[i+j-1] != ')':
        if parameter_open == 0 and s[i+j] == "(":
            parameter_open = j+1
        elif s[i+j] == ")":
            parameter_close = j
        j += 1
    
    return [parameter_open, parameter_close]
        
if __name__ == '__main__':
    main()