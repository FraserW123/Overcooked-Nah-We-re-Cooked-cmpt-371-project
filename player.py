
class Player:
    def __init__(self, id, max_height=10, max_width=10):
        self.position = (0, 0)  # Starting position of the player
        self.direction = 'R' #starting direction of the player, facing right
        self.item = None  #the items the player is holding
        self.id = id
        self.max_height = max_height
        self.max_width = max_width

    def move(self, direction):
        """Move the player in a specified direction."""
        x, y = self.position
        if direction == "up":
            self.position = (x, y - 1)
            self.direction = 'U'
        elif direction == "down":
            self.position = (x, y + 1)
            self.direction = 'D'
        elif direction == "left":
            self.position = (x - 1, y)
            self.direction = 'L'
        elif direction == "right":
            self.position = (x + 1, y)
            self.direction = 'R'
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
    def get_looking_position(self):
        #getting the position that the player is looking at
        x, y = self.position
        direction = self.direction
        if direction == "U":
            return (x, y - 1)
        elif direction == "D":
            return (x, y + 1)
        elif direction == "L":
            return (x-1, y)
        elif direction == "R":
            return (x+1, y)
    def interact(self, interactable):
        if self.item and not (len(interactable.items)>=interactable.max_items):
            #player has an item and the interactable have an empty spot
            self.item = interactable.pick_up_item()
        elif not self.item and (len(interactable.items)> 0):
            #player is not holding an item, and the interactable does have one
            interactable.drop_off_item(self.item)
            self.item = None
    