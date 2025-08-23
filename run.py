def create_grid():
    print("Please enter an whole number")
    grid_wdith = int(input("How wide would you like your grid to be: "))
    grid = []
    for i in range(grid_wdith):
        grid.append(["■"] * grid_wdith)
    for row in grid:
        print(" ".join(row))
    return grid


create_grid()