


class Layout:

    def __init__(self, height, width, fill="."):
        self.width = width
        self.height = height
        self.grid = [[fill for _ in range(height)] for _ in range (width)]

    def display(self):
        for row in self.grid:
            print(" ".join(row))
        print()

    def update_cell(self, row, col, char="."):
        """Update the character at a specific cell."""
        if 0 <= row < self.height and 0 <= col < self.width and len(char) == 1:
            self.grid[row][col] = char
            return True
        return False
    
    def reset_cells(self):
        fill = "."
        self.grid = [[fill for _ in range(self.height)] for _ in range (self.width)]



    def get_cell(self, row, col):
        """Get the value at a specific cell."""
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col]
        return None


import keyboard
def main():

    # keyboard.on_press_key("p", lambda _:print("You pressed p"))

    game_grid = Layout(3,3)
    print("Initial grid:")
    game_grid.display()

    # Simple interactive loop
    while True:
        command = input("Enter row,col,char (or 'quit'): ").strip()
        if command.lower() == 'quit':
            break
        elif command.lower() == 'reset':
            print("got here")
            game_grid.reset_cells()
            game_grid.display()
        else:
            try:
                row, col, char = command.split(",")
                row = int(row)
                col = int(col)
                if game_grid.update_cell(row, col, char):
                    game_grid.display()
                else:
                    print("Invalid input or position.")
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    main()

    

