# CSP-PseudocodeRunner
This is a program that runs AP Computer Science Principles pseudocode. This is done by converting the pseudocode to Python and executing it.

## Usage
To run standard pseudocode, use `pseudocode.py`. By default, this executes pseudocode in `pseudocode/code.txt`.
If the pseudocode references the robot, use `robot.py`. By default, the grid information is in `pseudocode/grid.txt` and the code is in `pseudocode/robot_code.txt`.

### Grid notation
For robot pseudocode, the grid the robot is on, as well as the default position of the robot must be given. Each space in the grid is represented by a single character in the grid file.
* Empty space = `.`
* Wall = `#`
* Robot = `^`, `v`, `<`, `>` for facing up, down, left, and right respectively

## To be added
* Combine `pseudocode.py` and `robot.py` into one file
* Make a version that uses a GUI to initialize the robot's grid configuration
* Make it possible to specify the pseudocode file locations with command line arguments
