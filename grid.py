

class Layout:

    def __init__(self, layout=None, height = None, width = None, fill="."):
        if height and width:
            self.width = width
            self.height = height
            self.grid = [[fill for _ in range(height)] for _ in range (width)]
        elif layout:
            self.grid = layout
            self.width = len(layout[0])
            self.height = len(layout)
    def display(self):
        for row in self.grid:
            print(" ".join(row))
        print()

    def update_cell(self, row, col, string="."):
        """Update the character at a specific cell."""
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = string
            return True
        return False
    
    def reset_cells(self):
        fill = "."
        self.grid = [[fill for _ in range(self.height)] for _ in range (self.width)]


    def get_grid(self):
        """Return the current grid."""
        return self.grid



    def get_cell(self, row, col):
        """Get the value at a specific cell."""
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col]
        return None
