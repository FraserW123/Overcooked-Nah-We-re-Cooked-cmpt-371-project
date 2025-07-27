
class Player:
    def __init__(self, id, max_height=10, max_width=10):
        self.position = (0, 0)  # Starting position of the player
        self.direction = "R"
        self.item = None  #the items the player is holding
        self.id = id
        self.max_height = max_height
        self.max_width = max_width

    def move(self, direction):
        """Move the player in a specified direction."""
        x, y = self.position
        if direction == "up":
            self.position = (x, y - 1)
        elif direction == "down":
            self.position = (x, y + 1)
        elif direction == "left":
            self.position = (x - 1, y)
        elif direction == "right":
            self.position = (x + 1, y)
        else:
            print("Invalid direction. Use 'up', 'down', 'left', or 'right'.")
        
        # Ensure the player stays within bounds
        self.position = (
            max(0, min(self.position[0], self.max_width - 1)),
            max(0, min(self.position[1], self.max_height - 1))
        )

    def get_id(self):
        """Return the player's ID."""
        return self.id

    def get_position(self):
        """Return the current position of the player."""
        return self.position
    
    def set_position(self, position):
        """Set the player's position to a specific coordinate."""
        if (0 <= position[0] < self.max_width) and (0 <= position[1] < self.max_height):
            self.position = position
        else:
            print("Position out of bounds.")
    def set_direction(self,direction):
        self.direction = direction
    
    def pick_item(self, item):
        """Add an item to the player's holdings."""
        if not self.item:
            self.item = item
            print(f"Picked up: {item}")
        else:
            print("Unable to pick up item, hand is full")

    def drop_item(self):
        """Remove an item from the player's holdings."""
        if self.item:
            item = self.item
            self.item = None
            print("dropped off item")
            return item
        else:
            print(f"Nothing to drop off.")
    
    