import random
import os


# imported from stackoverflow.com - see readme
def clear_board():
    """
    This clears the terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def grid_user_input():
    """
    This function asks the user to select how large they would want
    the grid and how many mines they would like to place
    """
    while True:
        try:
            print("Please enter an whole number between 10 and 20")
            grid_width = int(input("How wide would you like your grid to be: "))
            if 10 <= grid_width <= 20:
                break
            else:
                print("This number is not within the range")
        except ValueError:
            print("Your number is invalid, please use an integer")
    clear_board()

    while True:
        try:
            print("Please enter an whole number between 10 and 30")
            num_of_mines = int(input("How many mines would you like to place in the grid: "))
            if 10 <= num_of_mines <= 30:
                break
            else:
                print("This number is not within the range")
        except ValueError:
            print("Your number is invalid, please use an integer")

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
            cell = {"mine": False, "revealed": False, "flag": False}
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
        print(f"{letter:^{cell_width}}", end="")
    print()

    # Y axis
    for y, row in enumerate(grid):
        print(f"{y+1:4} ", end="")
        for x, cell in enumerate(row):
            # this for loop determines if there should be a * or ■ if
            #  its a mine or safe
            if cell["revealed"] is True:
                if cell["mine"] is True:
                    print(f"{'*':^{cell_width}}", end="")
                else:
                    adj_mines = adjacent_mines(grid, y, x)
                    if adj_mines == 0:
                        print(f"{' ':^{cell_width}}", end="")
                    else:
                        print(f"{adj_mines:^{cell_width}}", end="")
            else:
                if cell["flag"]:
                    print(f"{'F':^{cell_width}}", end="")
                else:
                    print(f"{'■':^{cell_width}}", end="")
        print()


def place_random_mines(grid, num_of_mines):
    """
    This randomly places mines throughout the grid
    """
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
    """
    This function allows the user to select a grid coordinate with validation
    """
    message = ""
    selected_tile = input("Enter a tile using the format eg 'B3': ")

    is_flag = selected_tile.startswith("#")
    if is_flag:
        selected_tile = selected_tile[1:].strip()

    if not selected_tile[0].isalpha() or not selected_tile[1:].isdigit():
        message = "Invalid input! Use format like B3 or fB3."
        return None

    col, row = definitions(selected_tile)
    # Stops a user being able to select a x coordinate outside of the
    # grid size.
    if not (0 <= col < grid_width):
        message = "invalid X coordinate"
        return True

    # Stops a user being able to select a y coordinate outside of the
    # grid size.
    if not (0 <= row < grid_width):
        message = "invalid Y coordinate"
        return True

    if is_flag:
        if grid[row][col]["revealed"]:
            message = "This tile is already revealed, no need to place a flag"
        else:
            grid[row][col]["flag"] = not grid[row][col]["flag"]
            if grid[row][col]["flag"]:
                message = "Your selected tile has been flagged"
            else:
                message = "The flag on your selected tile has been removed"
    else:
        if not grid[row][col]["flag"]:
            grid[row][col]["revealed"] = True
            if not grid[row][col]["mine"] and adjacent_mines(grid, row, col) == 0:
                reveal_adjacent_empty(grid, row, col)
        else:
            message = "You need to remove the flag in order to reveal this tile"

    clear_board()
    show_grid(grid)
    if message:
        print(message)

    return selected_tile


def increment_score(grid, selected_tile, score):
    """
    This creates a score that tells the user how many revealed tiles
    they have got
    """
    col, row = definitions(selected_tile)
    if not grid[row][col]["mine"] and grid[row][col]["revealed"]:
        score += 1
        print(f"Your current score is {score}")
    return score


def reveal_adjacent_empty(grid, row, col):
    grid_size = len(grid)
    for x in range(max(0, row - 1), min(grid_size, row + 2)):
        for y in range(max(0, col - 1), min(grid_size, col + 2)):
            if x == row and y == col:
                continue
            if not grid[x][y]["mine"] and not grid[x][y]["revealed"]:
                grid[x][y]["revealed"] = True
                if adjacent_mines(grid, x, y) == 0:
                    reveal_adjacent_empty(grid, x, y)


def adjacent_mines(grid, row, col):
    """
    This function iterates through each adjacent tile (8) and look for a mine
    If a mine is found it will increase the total amount of mines found
    """
    grid_size = len(grid)
    mine_count = 0
    for x in range(max(0, row - 1), min(grid_size, row + 2)):
        for y in range(max(0, col - 1), min(grid_size, col + 2)):
            if x == row and y == col:
                continue
            if grid[x][y]["mine"]:
                mine_count += 1
    return mine_count


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
    """
    This function is the main function which calls the other functions in one.
    """
    grid_width, num_of_mines = grid_user_input()
    grid = create_grid(grid_width)
    place_random_mines(grid, num_of_mines)
    active_game = True
    score = 0
    show_grid(grid)

    while active_game is True:
        selected_tile = user_select_tile(grid_width, grid)
        col, row = definitions(selected_tile)
        if grid[row][col]["revealed"]:
            score = increment_score(grid, selected_tile, score)
            active_game = game_over(grid, selected_tile)


def main_menu():
    clear_board()
    name = input("Please enter your name: ")
    print(f"Welcome {name} to my Minesweeper! Please select an option")
    print("""
    "1. Play Minesweeper"
    "2. Rules of Minesweeper"
    "3. Leaderboard"
    """)

    choice = input("select an option using numbers 1-3. ")
    if choice == "1":
        clear_board()
        game_start()
    elif choice == "2":
        clear_board()
        show_rules()
    elif choice == "3":
        clear_board()
        show_leaderboard()
    else:
        print("That is not a valid option")

main_menu()