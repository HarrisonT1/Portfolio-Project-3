import gspread
from google.oauth2.service_account import Credentials
import random
import os
from colorama import init, Fore, Style
import time
init(autoreset=True)

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Project-Portfolio-3')

stats = SHEET.worksheet('stats')
data = stats.get_all_values()


# imported from stackoverflow.com - see readme
def clear_board():
    """
    This clears the terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def show_rules():
    clear_board()
    print("""
How to play Minesweeper
    1. Select how large you would like the grid to be.
    2. Choose how many mines you would like to be places in the grid.
    3. Type a coordinate of a tile to reveal it using the format 'B3'
    4. When a mine is revealed the user loses.
    5. When all safe tiles are revealed the user wins.
    6. Keep track of the amount of mines you flagged.
          """)

    input(Fore.GREEN + "Press Enter to return to the main menu")
    clear_board()
    return


def show_tips():
    clear_board()
    print("""
Tips to help you in minesweeper:
    1. You can flag a suspected mine using the format '#b3'
    2. You can remove a flag using same flagging format '#b3'
    3. The numbers show you how many mines are adjacent to that tile.
    4. Be patient as rushing can lead to simple mistakes
          """)

    input(Fore.GREEN + "Press Enter to return to the main menu")
    clear_board()
    return


def show_stats():
    """
    This displayed the data from the spreadsheet, which is updated
    in real time with the update_stats function
    """
    clear_board()

    stats = SHEET.worksheet('stats')
    data = stats.get_all_values()

    headers = data[0]
    values = data[1]

    for i in range(len(headers)):
        title = headers[i].strip()
        value = values[i]
        print(Fore.GREEN + f"{title}: {value}")

    input(Fore.GREEN + "Press Enter to return to the main menu")
    clear_board()
    return


def update_stats(
        games_played=0,
        mines_hit=0,
        safe_tiles=0,
        games_won=0,
        games_lost=0):
    stats = SHEET.worksheet('stats')
    data = stats.get_all_values()

    # this selects the line after the headings
    values = [int(i) for i in data[1] if i != '']

    # This increases the value of each stat
    values[0] += games_played
    values[1] += mines_hit
    values[2] += safe_tiles
    values[3] += games_won
    values[4] += games_lost

    # rows a2 through e2 are updated
    stats.update([values], 'A2:E2')


def grid_user_input():
    """
    This function asks the user to select how large they would want
    the grid and how many mines they would like to place
    """

    while True:
        try:
            print(
                Fore.GREEN
                + "Please enter an whole number between 10 and 20")
            grid_width = int(
                input(
                    Fore.GREEN + "How wide would you like your grid to be: "))
            if 10 <= grid_width <= 20:
                break
            else:
                print(Fore.RED + "This number is not within the range")
        except ValueError:
            print(Fore.RED + "Your number is invalid, please use an integer")
    clear_board()

    while True:
        print(Fore.GREEN, end="")
        try:
            print(
                Fore.GREEN
                + "Please enter an whole number between 10 and 30")
            num_of_mines = int(
                input(
                    Fore.GREEN
                    + "How many mines would you like to place in the grid: "))
            if 10 <= num_of_mines <= 30:
                break
            else:
                print(Fore.RED + "This number is not within the range")
        except ValueError:
            print(Fore.RED + "Your number is invalid, please use an integer")

    print(Style.RESET_ALL)
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
                        if adj_mines == 1:
                            color = Fore.GREEN
                        elif adj_mines == 2:
                            color = Fore.YELLOW
                        elif adj_mines == 3:
                            color = Fore.RED
                        else:
                            color = Fore.CYAN
                        print(
                            color + f"{adj_mines:^{cell_width}}"
                            + Fore.RESET, end=""
                            )
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
    print(Fore.GREEN + "You can flag a tile using the format '#B3")
    selected_tile = input(Fore.GREEN + "Enter a tile using the format 'B3': ")

    is_flag = selected_tile.startswith("#")
    if is_flag:
        selected_tile = selected_tile[1:].strip()

    if not selected_tile[0].isalpha() or not selected_tile[1:].isdigit():
        message = "Invalid input! Use format like B3 or #B3."
        print(Fore.RED + message)
        return None

    col, row = definitions(selected_tile)
    # Stops a user being able to select a x coordinate outside of the
    # grid size.
    if not (0 <= col < grid_width):
        message = "invalid X coordinate"
        print(Fore.RED + message)
        return None

    # Stops a user being able to select a y coordinate outside of the
    # grid size.
    if not (0 <= row < grid_width):
        message = "invalid Y coordinate"
        print(Fore.RED + message)
        return None

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
        if grid[row][col]["revealed"]:
            message = Fore.RED + "This tile is already revealed"
            print(message)
            return None
        elif grid[row][col]["flag"]:
            message = (
                Fore.RED
                + "You need to remove the flag to reveal this tile")
            print(message)
            return None
        elif not grid[row][col]["revealed"]:
            grid[row][col]["revealed"] = True
            if (
                not grid[row][col]["mine"]
                and adjacent_mines(grid, row, col) == 0
            ):
                reveal_adjacent_empty(grid, row, col)

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


def game_over(grid, selected_tile, calced_time):
    """
    If user hits a mine, the board is revealed and the user is shown a
    game over message
    """
    col, row = definitions(selected_tile)
    if (
        grid[row][col]["mine"]
        and grid[row][col]["revealed"]
        and not grid[row][col]["flag"]
    ):
        for row in grid:
            for cell in row:
                cell["revealed"] = True
            clear_board()
            show_grid(grid)
        print(Fore.RED + "You Hit A Mine! You Lose!")
        print(f"You took {calced_time} before losing")
        return False
    return True


def game_win(grid):
    for row in grid:
        for cell in row:
            if not cell["mine"] and not cell["revealed"]:
                return False

    for row in grid:
        for cell in row:
            cell["revealed"] = True

    clear_board()
    show_grid(grid)
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
    update_stats(games_played=1)

    start_time = time.time()

    while active_game is True:

        update_stats(games_played=1)
        selected_tile = user_select_tile(grid_width, grid)
        if not selected_tile:
            continue

        col, row = definitions(selected_tile)

        if grid[row][col]["revealed"] and not grid[row][col]["mine"]:
            score = increment_score(grid, selected_tile, score)
            update_stats(safe_tiles=1)

        end_time = time.time()
        total_time = end_time - start_time
        minutes = int(total_time // 60)
        seconds = int(total_time % 60)
        calced_time = f"{minutes} minutes and {seconds} seconds"

        # Game over
        if grid[row][col]["revealed"]:
            if grid[row][col]["mine"]:
                game_over(grid, selected_tile, calced_time)
                update_stats(mines_hit=1, games_lost=1,)
                active_game = False

        # Game win
        if game_win(grid):
            clear_board()
            show_grid(grid)
            print(Fore.GREEN + "Congratulations! You Win!")
            print(f"Your score was: {score}")
            print(f"You took {calced_time} before winning")
            update_stats(games_won=1)
            active_game = False

    input("Press Enter to return to the main menu").strip()
    clear_board()
    return


def main_menu():
    clear_board()
    print(Fore.CYAN + Style.BRIGHT + """
███╗   ███╗██╗███╗   ██╗███████╗███████╗██╗    ██╗███████╗██████╗ ███████╗██████╗
████╗ ████║██║████╗  ██║██╔════╝██╔════╝██║    ██║██╔════╝██╔══██╗██╔════╝██╔══██╗
██╔████╔██║██║██╔██╗ ██║█████╗  ███████╗██║ █╗ ██║█████╗  ██████╔╝█████╗  ██████╔╝
██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ╚════██║██║███╗██║██╔══╝  ██╔═══╝ ██╔══╝  ██╔══██╗
██║ ╚═╝ ██║██║██║ ╚████║███████║███████║╚███╔███╔╝███████╗██║     ███████╗██║  ██║
╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝
""" + Style.RESET_ALL)  # noqa: E501
    while True:
        name = input("Please enter your name: ")
        if not name:
            print(Fore.RED + "You need to input a username")
            continue
        if not name.isalpha():
            print(Fore.RED + "You can only input letters, try again")
            continue
        name_upper = name[0].upper() + name[1:]
        break
    clear_board()
    while True:
        print(
            f"{Fore.MAGENTA}{Style.BRIGHT}Welcome {name_upper} to my "
            "Minesweeper! Please select an option.")
        print(Fore.CYAN + Style.BRIGHT + """
1. Play Minesweeper
2. Rules of Minesweeper
3. Tips for Minesweeper
4. Minesweeper Stats
        """)

        choice = input(
            Fore.GREEN + Style.BRIGHT
            + "Select an option using numbers 1-4.\n")
        if choice == "1":
            clear_board()
            game_start()
        elif choice == "2":
            clear_board()
            show_rules()
        elif choice == "3":
            clear_board()
            show_tips()
        elif choice == "4":
            clear_board()
            show_stats()
        else:
            print("That is not a valid option")
            clear_board()


main_menu()
