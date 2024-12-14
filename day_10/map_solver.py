import sys


# Reads in a file and turns it into a grid (2d list)
def file_to_grid(map_file: str) -> list[list]:
    with open(map_file, "r") as f:
        read_map = f.readlines()

    # Strip all \n
    read_map = [x.strip() for x in read_map]

    # Make grid of lists
    grid = [[x for x in y] for y in read_map]

    # Remove empty lists
    grid = [x for x in grid if x]

    # Make string ints
    grid = [[int(x) for x in y] for y in grid]

    return grid


def find_uphill_neighbours(grid, y: int, x: int) -> tuple[int, int]:
    if x < 0 or x >= len(grid[0]):
        return (-1, -1)
    if y < 0 or y >= len(grid):
        return (-1, -1)

    # Get value at current coord
    value = grid[y][x]

    uphill_neighbours = []

    # Check upstairs neighbour
    if y != 0:
        value_neighbour = grid[y-1][x]
        if value_neighbour == value + 1:
            uphill_neighbours.append((y-1, x))

    # Check downstairs neighbour
    if y != len(grid) - 1:
        value_neighbour = grid[y+1][x]
        if value_neighbour == value + 1:
            uphill_neighbours.append((y+1, x))

    # Check left neighbour
    if x != 0:
        value_neighbour = grid[y][x-1]
        if value_neighbour == value + 1:
            uphill_neighbours.append((y, x-1))

    # Check right neighbour
    if x != len(grid[0]) - 1:
        value_neighbour = grid[y][x+1]
        if value_neighbour == value + 1:
            uphill_neighbours.append((y, x+1))

    # Return tuples of all coords that are one height uphill
    return uphill_neighbours


def search_peaks_per_trailhead(grid, start_y: int, start_x: int) -> int:
    score = 0

    # Create queue
    q = []

    # Track visited cells
    visited = []

    # Append starting point
    q.append((start_y, start_x))
    visited.append((start_y, start_x))

    # Breadth first search
    while q:
        curr = q.pop(0)
        for neighbour in find_uphill_neighbours(grid, curr[0], curr[1]):
            if neighbour not in visited:
                if grid[neighbour[0]][neighbour[1]] == 9:
                    score += 1

                visited.append(neighbour)
                q.append(neighbour)

    return score


def search_trails_per_peak(grid, start_y: int, start_x: int) -> int:
    score = 0

    # Create queue
    q = []

    # Append starting point
    q.append((start_y, start_x))

    # Breadth first search
    while q:
        curr = q.pop(0)
        for neighbour in find_uphill_neighbours(grid, curr[0], curr[1]):
            if grid[neighbour[0]][neighbour[1]] == 9:
                score += 1

            q.append(neighbour)

    return score


if __name__ == "__main__":
    mode_options = ["peak_per_trailead", "trails_per_peak"]
    # Check argv
    if len(sys.argv) != 3 or sys.argv[2] not in mode_options:
        print(f"Use: map_solver.py <map.txt> <mode ({mode_options})>")
        exit(0)

    # Read map file and make it into a 2d grid
    map_file = sys.argv[1]
    grid = file_to_grid(map_file)

    mode = sys.argv[2]

    total_score = 0

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 0:
                if mode == "peaks_per_trailhead":
                    total_score += search_peaks_per_trailhead(grid, y, x)
                elif mode == "trails_per_peak":
                    total_score += search_trails_per_peak(grid, y, x)

    print("Total score is: ", total_score)
