


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


from pynput import keyboard
from player import Player
import time
HEIGHT = 10
WIDTH = 10
def main():
    game_grid = Layout(HEIGHT, WIDTH)
    print("Initial grid:")
    game_grid.display()
    player = Player(max_height=HEIGHT, max_width=WIDTH)

    game = {"running": True}

    def on_press(key):
        try:
            if key.char == 'q':
                game["running"] = False
            elif key.char == 'p':
                print("You pressed p")
        except AttributeError:
            if key == keyboard.Key.up:
                player.move("up")
            elif key == keyboard.Key.down:
                player.move("down")
            elif key == keyboard.Key.left:
                player.move("left")
            elif key == keyboard.Key.right:
                player.move("right")

            game_grid.display()

    # Start the listener in a separate thread
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    prev_position = player.get_position()

    # Game loop
    while game["running"]:
        #time.sleep(0.2)
        position = player.get_position()
        # Check if the player is within bounds before updating the grid
        if position != prev_position and 0 <= position[0] < game_grid.width and 0 <= position[1] < game_grid.height:
            game_grid.update_cell(prev_position[1], prev_position[0],'.')
            game_grid.update_cell(position[1], position[0], 'P')
            prev_position = position
        # else:
        #     print(player.get_position())  



    listener.stop()
    print("Game stopped.")

if __name__ == "__main__":
    main()
    

