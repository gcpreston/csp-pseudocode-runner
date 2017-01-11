import sys
import getopt
import pseudocode

grid = []

def main():
    global grid
    
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
    
    with open(filename) as file:
        for line in file.readlines():
            current_line = []
            
            for square in line.rstrip():
                current_line.append(square)
            grid.append(current_line)
    
    if not rectangular(grid):
        print("The grid is not rectangular.")
        sys.exit()
        
    with open("pseudocode/robot_code.txt") as file:
        code = file.read()
    
    exec(transcode(code, input_type, grid))
    
def transcode(code, input_type, grid):
    code = pseudocode.transcode(code, input_type)
    
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
        "class Robot():\n"
        "\n"
        "    def __init__(self, grid, location, facing):\n"
        "        self.grid = grid\n"
        "        self.location = location\n"
        "        self.facing = facing\n"
        "        self.moves = ((-1, 0), (0, 1), (1, 0), (0, -1))\n"
        "\n"
        "    def can_move(self, direction):\n"
        "        coords = [x + y for x, y in zip(self.location, self.moves[direction])]\n"
        "        if (0 <= coords[0] < len(self.grid) and\n"
        "            0 <= coords[1] < len(self.grid[1]) and\n"
        "            self.grid[coords[0]][coords[1]] == '.'):\n"
        "                return True\n"
        "        else:\n"
        "            return False\n"
        "\n"
        "    def move_forward(self):\n"
        "        new = [x + y for x, y in zip(self.location, self.moves[self.facing])]\n"
        "        if self.can_move(self.facing):\n"
        "            self.location = new\n"
        "            print(self.location, self.facing)\n"
        "\n"
        "    def rotate_right(self):\n"
        "        self.facing = (self.facing + 1) % 4\n"
        "\n"
        "    def rotate_left(self):\n"
        "        self.facing = (self.facing - 1) % 4\n"
        "\n"
        f"robot = Robot({grid}, {location}, {facing})\n"
        "\n"
        f"robot = Robot({grid}, {location}, {facing})\n"
        "\n"
    )
    
    if code.startswith("import random"):
        code = code[:14] + '\n' + start_code + code[14:]
    else:
        code = start_code + code
        
    replacements = {
        "CAN_MOVE ("         : "CAN_MOVE(",
        "CAN_MOVE(forward)"  : "robot.can_move(robot.facing)",
        "CAN_MOVE(left)"     : "robot.can_move((robot.facing - 1) % 4)",
        "CAN_MOVE(right)"    : "robot.can_move((robot.facing + 1) % 4)",
        "MOVE_FORWARD"       : "robot.move_forward",
        "ROTATE_LEFT"        : "robot.rotate_left",
        "ROTATE_RIGHT"       : "robot.rotate_right"
    }
    
    for _ in range(2):
        for r in replacements:
            code = code.replace(r, replacements[r])
    
    code += (
        "\nprint()\n"
        "directions = ('^', '>', 'v', '<')\n"
        "for r in range(len(robot.grid)):\n"
        "    for c in range(len(robot.grid[0])):\n"
        "        if [r, c] == robot.location:\n"
        "            print(directions[robot.facing], end='')\n"
        "        else:\n"
        "            print(robot.grid[r][c], end='')\n"
        "    print()\n"
    )
    
    return code

def rectangular(lst):
    for i in lst:
        if len(i) != len(lst[0]):
            return False
    return True
    
if __name__ == '__main__':
    main()