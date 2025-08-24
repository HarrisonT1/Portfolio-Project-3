import random

def grid_user_input():
    print("Please enter an whole number")
    grid_width = int(input("How wide would you like your grid to be: "))
    print("Please enter an whole number between 10 and 50")
    num_of_mines = int(input("How many mines would you like to place in the grid: "))

    return grid_width, num_of_mines


def create_grid():
    """
    This function will create a grid based on what the user inputs
    """
    grid_width, num_of_mines = grid_user_input()

    grid = []
    cell_width = 4

    for i in range(grid_width):
        grid.append([f"{'■':{cell_width}}"] * grid_width)
    #   this print statement and for loop creates the numbered axis x and y to
    #   make it easier to select specific tiles.
    # X axis
    print("     ", end="")
    for x in range(grid_width):
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

# def place_random_mines():
#     total_mines = range(10, 50)
#     while total_mines:



create_grid()
# place_random_mines()