import sys
import getopt


def main():
    '''
    This function iterates through a properly formatted
    pseudocode text file and returns (roughly) equivalent
    python code.

    TODO:
    The main() function probably shouldn't be used for
    anything other than opening the file and calling
    a different function to parse through everything.
    '''

    ### Input Types ###
    # 0 = string, 1 = int, 2 = float
    input_type = 2
    filename = "pseudocode/code.txt"
    
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "f:is", ["file=", "int", "string"])
    except getopt.GetoptError:
        sys.exit()
        
    for opt, arg in opts:
        if opt in ("-f", "--file"):
            filename = arg
        if opt in ("-i", "--int"):
            input_type = 1
        if opt in ("-s", "--string"):
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
    # Removes all tabbed indentation
    code = code.replace('\t', '')
    
    # Tracks where the parser is in terms of layered stuff
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
          
    # Replaces characters ≥, ≤, ≠, ← with things that python can recognize
    for i in range(len(code)):
        if ord(code[i]) == 8592:
            code = code[:i] + '<-' + code[i + 1:]
        elif ord(code[i]) == 8800:
            code = code[:i] + '!=' + code[i + 1:]
        elif ord(code[i]) == 8805:
            code = code[:i] + '>=' + code[i + 1:]
        elif ord(code[i]) == 8804:
            code = code[:i] + '<=' + code[i + 1:]
            
    # Imports random if random is used
    if "RANDOM" in code:
        code = "import random\n" + code
    
    # Dict of pseudocode keywords/syntax and their python equivalents
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
    
    # Adds proper implementation for input() based on
    # the input type specified in the command line 
    if input_type == 0:
        replacements["INPUT"] = "input"
    elif input_type == 1:
        replacements["INPUT("] = "int(input()"
        replacements["INPUT ("] = "int(input()"
    elif input_type == 2:
        replacements["INPUT("] = "float(input()"
        replacements["INPUT ("] = "float(input()"
    
    # Replaces everything in the pseudocode with python equivalents
    equals_replaced = False
    for r in replacements:
        if not (r == ' = ' and equals_replaced):
            code = code.replace(r, replacements[r])
        if r == ' = ':
            equals_replaced = True
    
    # Selects all cases of things with parameters and treats them appropiately
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
    '''
    Takes a section of pseudocode that is being passed to something as
    a parameter or set of parameters and parses them out individually
    '''
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