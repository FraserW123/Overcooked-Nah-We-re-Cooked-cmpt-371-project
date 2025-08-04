
from player import Player


def initialize_interactable_grid(grid, tasklist=None):
    height = len(grid)
    width = len(grid[0])
    interactable_grid = []
    for i in range(height):
        row = [None] * width
        interactable_grid.append(row)
    for row in range(height):
        for col in range(width):
            if grid[row][col][0] == 'T':
                interactable_grid[row][col] = Interactable(col,row,items=list(grid[row][col][1:]))
            elif grid[row][col][0] == 'G':
                #G standing for garbage bin
                interactable_grid[row][col] = garbage_bin(col,row)
            elif grid[row][col][0] == 'I':
                #I for ingredient bin
                interactable_grid[row][col] = ingredient_bin(col,row, items = [grid[row][col][1]])
            elif grid[row][col][0] == 'A':
                # A for assembly station
                interactable_grid[row][col] = assembly_station(col, row, items=list(grid[row][col][1:]))
            elif grid[row][col][0] == 'W':
                # W for window, initialize with task list from server
                interactable_grid[row][col] = window(col, row, tasklist)
    return interactable_grid
class Interactable:
# the super class of stations,

    def __init__(self, x, y, items=None, max_items = 5):
        #taking in an x, y coordinate,
        # and an item list of up to three items to be present on the table
        self.x = x
        self.y = y
        self.max_items = max_items
        if items is None:
            self.items = []
        else:
            self.items = items[:max_items]

    def put_down_item(self,new_item):
        holding = len(self.items)
        if holding< self.max_items:
            self.items.append(new_item)
        else:
            print("unable to drop off item")

    def pick_up_item(self):
        holding = len(self.items)
        if holding>0:
            item= self.items[-1]
            self.items.pop()
            return item
        else:
            print("unable to pick up item")

class garbage_bin(Interactable):
    def pick_up_item(self):
        print("unable to pick up item")
    def put_down_item(self,new_item):
        pass

class ingredient_bin(Interactable):

    def __init__(self, x, y, items=None, max_items=5):
        super().__init__(x, y, items, max_items)
        self.max_items = 1

    def pick_up_item(self):
        item = self.items[-1]
        return item
    def put_down_item(self,new_item):
        pass

class assembly_station(Interactable):
    
    def __init__(self, x, y, items=None, max_items=3):
        #taking in an x, y coordinate,
        # and an item list of up to three items to be present on the table
        super().__init__(x, y, items, max_items)
        self.max_items = 5
        
    def pick_up_item(self):
        if len(self.items)>0:
            item = self.items[-1]
            self.items.pop()
            return item
        else:
            print("unable to pick up item")
            
    def put_down_item(self, new_item):
        holding = len(self.items)
        if holding < self.max_items:
            self.items.append(new_item)

            if len(self.items) == 5:
                # Check if the item is a burger and create it
                self.create_burger()
            elif len(self.items) == 3:
                # Check if the item is a sushi and create it
                self.create_sushi()
            elif len(self.items) == 4:
                # Check if the item is a pizza and create it
                self.create_pizza()
        else:
            print("unable to drop off item")
            
    def create_burger(self):
        # Krabby Patty
        # go through the items and check if correct items and in order
        # h = b + p + c + l + b
        if (self.items[0] == "b" and self.items[1] == "p" and
            self.items[2] == "c" and self.items[3] == "l" and
            self.items[4] == "b"):
            # Clear the items and create a burger
            self.items.clear()
            self.items.append("h") 
            print("Burger created.")
        else:
            print("Failure to create burger.")

    def create_sushi(self):
        # Sushi
        # go through the items and check if correct items and in order
        # s = w + r + f
        if (self.items[0] == "w" and self.items[1] == "r" and
            self.items[2] == "f"):
            # Clear the items and create a sushi
            self.items.clear()
            self.items.append("s") 
            print("Sushi created.")
    
    def create_pizza(self):
        # Pizza
        # go through the items and check if correct items and in order
        # p = d + t + c + o
        if (self.items[0] == "d" and self.items[1] == "t" and
            self.items[2] == "c" and self.items[3] == "o"):
            # Clear the items and create a pizza
            self.items.clear()
            self.items.append("z") 
            print("Pizza created.")
        else:
            print("Failure to create pizza.")

class window(Interactable):
    # submission window for players to submit orders according to task list
    def __init__(self, x, y, tasklist=None):
        super().__init__(x, y, max_items=0) 
        self.tasklist = tasklist
    
    def put_down_item(self, new_item):
        # safety check
        if self.tasklist is None:
            print("No tasklist available.")
            return
        
        # Check if food is in tasklist
        if self.tasklist.mark_completed(new_item):
            print(f"Order submitted successfully: {new_item}")
            return True
        else:
            print(f"Invalid order: {new_item} not in current tasks.")
            return False
    
    def pick_up_item(self):
        print("Cannot pick up items from the submission window.")
        pass