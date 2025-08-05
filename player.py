class Player:
    def __init__(self, id=0, color=(255,255,255), max_height=10, max_width=10):
        self.position = (0, 0)  # Starting position of the player
        self.direction = 'R' #starting direction of the player, facing right
        self.item = None  #the items the player is holding
        self.id = id
        self.max_height = max_height
        self.max_width = max_width
        self.color = color

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

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color
    
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
        # putting import here cuz it'd have a circular import otherwise
        from interactable import window
        # Special handling for window submissions
        if isinstance(interactable, window):
            if self.item:
                if interactable.put_down_item(self.item):
                    # put down item only if it's a valid submission
                    self.item = None
                else:
                    # Can't submit unordered food, put it elsewhere
                    print("Failed to submit item to window.")
            else:
                print("No item to submit.")
        # Normal interaction for other interactables
        elif self.item and (len(interactable.items) < interactable.max_items):
            # Player has an item and the interactable has an empty spot
            interactable.put_down_item(self.item)
            self.item = None
        elif not self.item and (len(interactable.items) > 0):
            # Player is not holding an item, and the interactable does have one
            self.item = interactable.pick_up_item()