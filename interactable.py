
from player import Player


def initialize_interactable_grid(grid):
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
    return interactable_grid

class Interactable:
# the super class of stations,

    def __init__(self, x, y, items=None, max_items = 3):
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
    def drop_off_item(self,new_item):
        pass


class ingredient_bin(Interactable):
    def __init__(self, x, y, item):
        super().__init__(x, y, item[:1])

    def pick_up(self, player: Player):
        pass
    def drop_off_item(self,new_item):
        print("unable to pick up item")



