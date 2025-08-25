import random
import os


# imported from stackoverflow.com - see readme
def clear_board():
    os.system('cls' if os.name == 'nt' else 'clear')


def grid_user_input():
    print("Please enter an whole number")
    grid_width = int(input("How wide would you like your grid to be: "))
    print("Please enter an whole number between 10 and 50")
    num_of_mines = int(input("How many mines would you like to place in the grid: "))
    clear_board()
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
            # this for loop determines if there should be a * or ■ if
            #  its a mine or safe
            if cell["revealed"] is True:
                if cell["mine"] is True:
                    print(f"{'*':{cell_width}}", end="")
                else:
                    print(f"{' ':{cell_width}}", end="")
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


def definitions(selected_tile):
    col_let = selected_tile[0].upper()
    row_num = selected_tile[1:]

    col = ord(col_let) - ord('A')
    row = int(row_num) - 1

    return col, row


def user_select_tile(grid_width, grid):
    selected_tile = input("Enter a tile using the format eg 'B3': ")
    col, row = definitions(selected_tile)
    # Stops a user being able to select a x coordinate outside of the
    # grid size.
    if not (0 <= col < grid_width):
        print("invalid X coordinate")
        return True

    # Stops a user being able to select a y coordinate outside of the
    # grid size.
    if not (0 <= row < grid_width):
        print("invalid Y coordinate")

    grid[row][col]["revealed"] = True
    clear_board()
    show_grid(grid)

    score = 0
    if not grid[row][col]["mine"]:
        score += 1
        print(score)
    
    return selected_tile


def game_over(grid, selected_tile):
    """
    If user hits a mine, the board is revealed and the user is shown a
    game over message
    """
    col, row = definitions(selected_tile)
    if grid[row][col]["mine"]:
        for row in grid:
            for cell in row:
                cell["revealed"] = True
            clear_board()
            show_grid(grid)
        print("You Hit A Mine! You Lose!")
        return False
    return True


def game_start():
    grid_width, num_of_mines = grid_user_input()
    grid = create_grid(grid_width)
    place_random_mines(grid, num_of_mines)
    active_game = True
    show_grid(grid)

    while active_game is True:
        selected_tile = user_select_tile(grid_width, grid)
        if selected_tile:
            active_game = game_over(grid, selected_tile)


game_start()
