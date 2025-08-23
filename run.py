def create_grid():
    """
    This function will create a grid based on what the user inputs
    """
    print("Please enter an whole number")
    grid_wdith = int(input("How wide would you like your grid to be: "))
    grid = []
    for i in range(grid_wdith):
        grid.append(["■"] * grid_wdith)
    #   this print statement and for loop creates the numbered axis x and y to
    #   make it easier to select specific tiles.
    print("  " + " ".join(str(x) for x in range(grid_wdith)))
    for y, row in enumerate(grid):
        print(f"{y:3} " + " ".join(row))
    return grid


create_grid()