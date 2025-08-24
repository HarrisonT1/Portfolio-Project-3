import random

def grid_user_input():
    print("Please enter an whole number")
    grid_width = int(input("How wide would you like your grid to be: "))
    print("Please enter an whole number between 10 and 50")
    num_of_mines = int(input("How many mines would you like to place in the grid: "))

    return grid_width, num_of_mines


def create_grid(grid_width):
    """
    This makes each cell a dictionary rather than a string
    """
    grid = []
    for x in range(grid_width):
        row = []
        for y in range(grid_width):
            cell = {"mine": False, "revealed": False}
            row.append(cell)
        grid.append(row)
    return grid


def show_grid(grid):
    """
    This function will create a grid based on what the user inputs
    """

    grid_size = len(grid)
    cell_width = 4

    #   this print statement and for loop creates the numbered axis x and y to
    #   make it easier to select specific tiles.
    #   X axis
    print("     ", end="")
    for x in range(grid_size):
        letter = chr(ord('A') + x)
        print(f"{letter:{cell_width}}", end="")
    print()

    # Y axis
    for y, row in enumerate(grid):
        print(f"{y+1:4} ", end="")
        for cell in row:
            # this for loop determines if there should be a * or ■ if its 
            # a mine or safe
            if cell["mine"] is True:
                print(f"{'*':{cell_width}}", end="")
            else:
                print(f"{'■':{cell_width}}", end="")
        print()


def place_random_mines(grid, num_of_mines):
    grid_width = len(grid)
    every_cell = []

    # The first for loop created a list of all the tiles in the grid
    for i in range(grid_width):
        for x in range(grid_width):
            every_cell.append((i, x))
    # this uses the random import to select a random tile from the for loop
    mine_positions = random.sample(every_cell, num_of_mines)
    # This final for loop changes the earlier dictionary key into true,
    # thus placing a mine
    for i, x in mine_positions:
        grid[i][x]["mine"] = True


grid_width, num_of_mines = grid_user_input()
grid = create_grid(grid_width)
place_random_mines(grid, num_of_mines)
show_grid(grid)