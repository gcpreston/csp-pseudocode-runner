import sys
import pseudocode

grid = []

def main():
    global grid
    
    with open("grid.txt") as file:
        for line in file.readlines():
            current_line = []
            
            for square in line.rstrip():
                current_line.append(square)
            grid.append(current_line)
    
    if not rectangular(grid):
        print("The grid is not rectangular.")
        sys.exit()
        
    execute(grid)
    
# may make different functions for transcoding and executing, or may change pseudocode.py to be like this
def execute(grid, filename="robot_code.txt"):
    with open(filename) as file:
        code = file.read()
        
    code = pseudocode.transcode(code)
    
    facing = 4
    directions = ('^', '>', 'v', '<')
    
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in directions and facing == 4:
                if facing != 4:
                    print("You cannot have more than one start position.")
                    sys.exit()
                facing = directions.index(grid[r][c])
                location = [r, c]
            
    if facing == 4:
        print("You must have a start position.")
        sys.exit()
        
    grid[location[0]][location[1]] = '.'
    
    start_code = (
        f"grid = {grid}\n"
        "moves = ((-1, 0), (0, 1), (1, 0), (0, -1))\n"
        f"facing = {facing}\n"
        f"location = {location}\n"
        "\n"
        "def can_move(direction):\n"
        "    coords = [x + y for x, y in zip(location, moves[direction])]\n"
        "    if 0 <= coords[0] < len(grid) and 0 <= coords[1] < len(grid[1]) and grid[coords[0]][coords[1]] == '.':\n"
        "        return True\n"
        "    else:\n"
        "        return False\n"
        "\n"
        "def move_forward():\n"
        "    global moves\n"
        "    global facing\n"
        "    global location\n"
        "    global can_move\n"
        "    new = [x + y for x, y in zip(location, moves[facing])]\n"
        "    if can_move(facing):\n"
        "        location = new\n"
        "        print(location, facing)\n"
        "\n"
        "def rotate_right():\n"
        "    global facing\n"
        "    facing = (facing + 1) % 4\n"
        "\n"
        "def rotate_left():\n"
        "    global facing\n"
        "    facing = (facing - 1) % 4\n"
        "\n"
    )
    
    if code.startswith("import random"):
        code = code[:14] + '\n' + start_code + code[14:]
    else:
        code = start_code + code
        
    replacements = {
        "CAN_MOVE ("         : "CAN_MOVE(",
        "CAN_MOVE(forward)"  : "can_move(facing)",
        "CAN_MOVE(left)"     : "can_move((facing - 1) % 4)",
        "CAN_MOVE(right)"    : "can_move((facing + 1) % 4)",
        "MOVE_FORWARD"       : "move_forward",
        "ROTATE_LEFT"        : "rotate_left",
        "ROTATE_RIGHT"        : "rotate_right"
    }
    
    for _ in range(2):
        for r in replacements:
            code = code.replace(r, replacements[r])
    
    print(code)
    print("OUTPUT:")
    exec(code)

def rectangular(lst):
    for i in lst:
        if len(i) != len(lst[0]):
            return False
    return True
    
if __name__ == '__main__':
    main()