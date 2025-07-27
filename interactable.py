
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
                interactable_grid[row][col] = Interactable(col,row,items=grid[row][col][1:])

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

    def pick_up(self, player: Player):
        if 0< len(self.items):
            player.pick_item(self.items[-1])
            self.items.pop()

    def drop_off(self,player:Player):
        if len(self.items)<self.max_items:
            item = player.drop_item()
            if item:
                self.items.append(item)
        else:
            print("full counter")


class garbage_bin(Interactable):
    def drop_off(self,player:Player):
        _=player.drop_item()

class ingredient_bin(Interactable):
    def __init__(self, x, y, item):
        super().__init__(x, y, item[:1])

    def pick_up(self, player: Player):
        player.pick_item(self.items[0])



