def create_grid():
    """
    This function will create a grid based on what the user inputs
    """
    print("Please enter an whole number")
    grid_wdith = int(input("How wide would you like your grid to be: "))
    grid = []
    cell_width = 4

    for i in range(grid_wdith):
        grid.append([f"{'■':{cell_width}}"] * grid_wdith)
    #   this print statement and for loop creates the numbered axis x and y to
    #   make it easier to select specific tiles.
    # X axis
    print("     ", end="")
    for x in range(grid_wdith):
        letter = chr(ord('A') + x)
        print(f"{letter:{cell_width}}", end="")
    print()
    # Y axis
    for y, row in enumerate(grid):
        print(f"{y+1:4} ", end="")
        for cell in row:
            print(f"{cell:3}", end="")
        print()
    return grid


create_grid()