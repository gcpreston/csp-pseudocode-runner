import sys
import getopt

def main():
    # by default, set INPUT () to recognize floats
    # 0 = string, 1 = int, 2 = float
    input_type = 2
    filename = "pseudocode/code.txt"
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:is", ["file=", "int", "string"])
    except getopt.GetoptError:
        sys.exit()
        
    for opt, arg in opts:
        if opt in ("-f", "--file"):
            filename = arg
    
    for arg in args:
        if arg in ("-i", "--int"):
            input_type = 1
        elif arg in ("-s", "--string"):
            input_type = 0
        
    try:
        with open(filename) as file:
            code = file.read()
        
        # change code to Python
        code = transcode(code, input_type)
               
        # execute the newly created Python code
        exec(code)
        
    except FileNotFoundError:
        print(filename + " not found.")
        
def transcode(code, input_type):
    # fix indentation
    code = code.replace('\t', '')
    
    layers = 0
    i = 0
    while i < len(code):
        if code[i] == '{':
            layers += 1
        elif code[i] == '}':
            layers -= 1
        elif code[i] == '\n' and layers > 0:
            if code[i+1] == '}':
                code = code[:i+1] + ('\t' * (layers - 1)) + code[i+1:]
            else:
                code = code[:i+1] + ('\t' * layers) + code[i+1:]
        i += 1
          
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
        "LENGTH"       : "len",
        "RANDOM"       : "random.randint"
    }
    
    if input_type == 0:
        replacements["INPUT"] = "input"
    elif input_type == 1:
        replacements["INPUT("] = "int(input()"
        replacements["INPUT ("] = "int(input()"
    elif input_type == 2:
        replacements["INPUT("] = "float(input()"
        replacements["INPUT ("] = "float(input()"
    
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
            times = line[:index].split()[1]
            
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