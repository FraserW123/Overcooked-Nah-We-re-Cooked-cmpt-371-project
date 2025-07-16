from test_project import Layout
from player import Player
from server import start_server

def main():
    game_grid = Layout(3, 3)
    print("Initial grid:")
    game_grid.display()
    player = Player()

    # Simple interactive loop
    while True:
        command = input("Enter row,col,char (or 'quit'): ").strip()
        if command.lower() == 'quit':
            break
        elif command.lower() == 'reset':
            game_grid.reset_cells()
            game_grid.display()
        else:
            try:
                row, col, char = command.split(",")
                row = int(row)
                col = int(col)
                player.move(char)  # Assuming char is a direction for the player
                if game_grid.update_cell(row, col, char):
                    game_grid.display()
                else:
                    print("Invalid input. Please ensure row and column are within bounds and char is a single character.")
            except ValueError:
                print("Invalid input format. Use row,col,char.")