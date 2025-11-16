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


# -----------------------------
# WFC CLASS (robust)
# -----------------------------
class WFC:
    def __init__(self, width, height, tiles, debug=False):
        self.width = width
        self.height = height
        self.tiles = tiles
        self.debug = debug
        self.reset_grid()

    def reset_grid(self):
        # Each cell starts with all tiles possible (fresh copy)
        self.grid = [[list(self.tiles.keys())[:] for _ in range(self.width)] for _ in range(self.height)]

    # ---------------------------------------
    # SELECT LOWEST ENTROPY CELL
    # ---------------------------------------
    def find_lowest_entropy(self):
        min_entropy = 99999
        best = None

        for y in range(self.height):
            for x in range(self.width):
                options = len(self.grid[y][x])
                # ignore already collapsed (options == 1)
                if 1 < options < min_entropy:
                    min_entropy = options
                    best = (x, y)

        return best

    # ---------------------------------------
    # COLLAPSE A CELL (choose 1 tile)
    # ---------------------------------------
    def collapse(self, x, y):
        options = self.grid[y][x]
        if not options:
            # contradiction: no options
            raise ValueError(f"Contradiction: trying to collapse empty cell at {(x,y)}")

        weighted_list = []
        for t in options:
            weighted_list += [t] * self.tiles[t]["weight"]  # Add the tiles according to the weight

        if not weighted_list:
            # defensive: should not happen if options non-empty and weights >0
            raise ValueError(f"No weighted options for cell {(x,y)} — options: {options}")

        choice = random.choice(weighted_list)
        self.grid[y][x] = [choice]  # collapse to single tile
        if self.debug:
            print(f"Collapsed {(x,y)} -> {choice}")
        return choice

    # ---------------------------------------
    # PROPAGATE CONSTRAINTS
    # ---------------------------------------
    def propagate(self, start_x, start_y):
        queue = deque([(start_x, start_y)])

        while queue:
            x, y = queue.popleft()
            current = self.grid[y][x]

            for (dx, dy), dir_name in DIRECTIONS.items():
                nx, ny = x + dx, y + dy

                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue

                allowed = set()
                for tile in current:
                    allowed.update(self.tiles[tile]["rules"][dir_name])

                before = self.grid[ny][nx][:]
                # compute intersection of before and allowed
                new_options = [t for t in before if t in allowed]

                if not new_options:
                    # contradiction found -> return False
                    if self.debug:
                        print(f"Contradiction at {(nx,ny)} -- before: {before} allowed: {sorted(allowed)}")
                    return False

                if new_options != before:
                    self.grid[ny][nx] = new_options
                    queue.append((nx, ny))
                    if self.debug:
                        print(f"Updated {(nx,ny)}: {before} -> {new_options}")

        return True

    # ---------------------------------------
    # MAIN RUN LOOP (with restarts)
    # ---------------------------------------
    def run(self, max_restarts=10):
        tries = 0
        while tries <= max_restarts:
            tries += 1
            self.reset_grid()
            if self.debug:
                print(f"\n--- Run attempt {tries} ---")
            success = True

            try:
                while True:
                    pos = self.find_lowest_entropy()
                    if pos is None:
                        # fully collapsed
                        break

                    x, y = pos
                    self.collapse(x, y)
                    ok = self.propagate(x, y)
                    if not ok:
                        # contradiction during propagation; break and restart
                        success = False
                        if self.debug:
                            print(f"Restarting due to contradiction after collapsing {(x,y)}")
                        break

            except ValueError as e:
                # some contradiction occurred
                success = False
                if self.debug:
                    print("Exception:", e)

            if success:
                if self.debug:
                    print("Succeeded!")
                return self.grid

            # else we will retry with a different random seed (or different choices)
            # small random shuffle to vary randomness
            random.shuffle(list(range(10)))  # quick entropy to change RNG state
            # continue loop to restart

        raise RuntimeError(f"WFC failed after {max_restarts} restarts")

# -----------------------------
# UTILS
# -----------------------------
def pretty_print(grid):
    # Safe pretty print: if cell is empty show '?', else first letter
    for row in grid:
        print(" ".join((cell[0][0].upper() if cell else "?") for cell in row))


# -----------------------------
# RUN THE WFC
# -----------------------------
if __name__ == "__main__":
    random.seed()  # system seed
    wfc = WFC(20, 10, TILES, debug=True)
    try:
        result = wfc.run(max_restarts=20)
        print("\nFinal map:")
        pretty_print(result)
    except RuntimeError as e:
        print("Generation failed:", e)
        sys.exit(1)
