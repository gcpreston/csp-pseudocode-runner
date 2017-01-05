import sys
from tkinter import Tk, Button

squares = []
colors = []
start_exists = False

def main():
    try:
        dims = [int(input("Enter number of rows: ")), int(input("Enter number of columns: "))]
    except (TypeError, ValueError):
        print("Please enter an integer.")
        sys.exit()
    
    root = Tk()
    
    global squares
    squares = [[None for _ in range(dims[1])] for _ in range(dims[0])]
    
    global colors
    colors = [["SystemButtonFace" for _ in range(dims[1])] for _ in range(dims[0])]

    for r in range(dims[0]):
        for c in range(dims[1]):
            squares[r][c] = Button(root, width=6, height=3)
            squares[r][c].bind("<Button-1>", lambda event, r=r, c=c: set_wall(r, c))
            squares[r][c].bind("<Button-3>", lambda event, r=r, c=c: set_start(r, c))
            
            squares[r][c].grid(row=r, column=c)
            
    print()
    print("Left click to set/remove black squares, right click to set/remove the start position.")
    print("Only one start square can be present on the screen at a time.")
    print()
    print("Close the window when the grid is complete...")
    print()
    
    root.mainloop()
    
    for r in colors:
        print(r)
    
def set_wall(r, c):
    global colors
    
    if squares[r][c].cget('bg') == "black":
        squares[r][c].configure(bg="SystemButtonFace")
        colors[r][c] = "SystemButtonFace"
    else:
        squares[r][c].configure(bg="black")
        colors[r][c] = "black"
    
def set_start(r, c):
    global start_exists
    global colors
    
    if not start_exists:
        squares[r][c].configure(bg="blue")
        colors[r][c] = "blue"
        start_exists = True
    elif squares[r][c].cget('bg') == "blue":
        squares[r][c].configure(bg="SystemButtonFace")
        colors[r][c] = "SystemButtonFace"
        start_exists = False
     
if __name__ == '__main__':
    main()
