import random
from collections import deque
import sys

# -----------------------------
# TILE DEFINITIONS
# -----------------------------

TILES = {
    "grass": {
        "weight": 5,
        "rules": {
            "N": ["grass", "forest", "sand"],
            "E": ["grass", "forest", "sand"],
            "S": ["grass", "forest", "sand"],
            "W": ["grass", "forest", "sand"],
        }
    },
    "forest": {
        "weight": 2,
        "rules": {
            "N": ["forest", "grass"],
            "E": ["forest", "grass"],
            "S": ["forest", "grass"],
            "W": ["forest", "grass"],
        }
    },
    "sand": {
        "weight": 3,
        "rules": {
            "N": ["sand", "grass"],
            "E": ["sand", "grass"],
            "S": ["sand", "water"],
            "W": ["sand", "grass"],
        }
    },
    "water": {
        "weight": 1,
        "rules": {
            "N": ["water", "sand"],
            "E": ["water", "sand"],
            "S": ["water", "sand"],
            "W": ["water", "sand"],
        }
    }
}

DIRECTIONS = {
    (0, -1): "N",
    (1, 0): "E",
    (0, 1): "S",
    (-1, 0): "W"
}

class WFC:
    def __init__(self, width, height, tiles):
        self.width = width
        self.height = height
        self.tiles = tiles

        # Each cell starts with all tiles possible
        self.grid = [[list(tiles.keys())[:] for _ in range(width)] for _ in range(height)]
        i = random.randint(0,10)
        j = random.randint(0,10)

    
        
    def min_entropy():
        pass

    def collapse(self,x,y):
        options = self.grid[y][x]

        weighted_list = []
        for t in options:
            weighted_list += [t] * self.tiles[t]["weight"] #Add the tiles according to the weight, 

        choice = random.choice(weighted_list)
        self.grid[y][x] = [choice]  # collapse to single tile
        return choice
    
    def propogate():
        pass

wfc = WFC(5,5,TILES)
for i in range(0,5):
    for j in range(0,5):
        wfc.collapse(i,j)
    
for i in range(0,5):
       print(wfc.grid)
