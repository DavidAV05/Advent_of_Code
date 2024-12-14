import argparse as ap


verbose = False


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
    grid = [[x for x in y] for y in grid]

    return grid


def find_region_neighbours(grid: list[list], y: int, x: int) -> list[tuple]:
    if not grid:
        print("Grid is empty")
        exit(-1)

    region_neighbours = []
    grid_size = (len(grid), len(grid[0]))

    for neighbor_pos in [(y-1, x), (y+1, x), (y, x+1), (y, x-1)]:
        # Check if neighbour is within grid
        if neighbor_pos[0] < 0 or neighbor_pos[0] >= grid_size[0]:
            continue
        if neighbor_pos[1] < 0 or neighbor_pos[1] >= grid_size[1]:
            continue

        # Check if neighbour is in same region
        if grid[y][x] == grid[neighbor_pos[0]][neighbor_pos[1]]:
            region_neighbours.append(neighbor_pos)

    return region_neighbours


# Goes through the grid and gathers data on the regions
def get_regions(grid: list[list]) -> dict:
    # Store visited places within grid
    visited = []
    regions: dict[tuple: list] = {}

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (y, x) not in visited:
                # Update visited
                visited.append((y, x))

                # Make new region
                regions[(y, x)] = [(y, x)]

                # Initialise queue for breadth first search
                queue = [(y, x)]

                # Breadth first search on region
                while queue:
                    pos = queue.pop(0)

                    for reg_neigh in find_region_neighbours(
                                                        grid, pos[0], pos[1]):
                        if reg_neigh not in visited:
                            queue.append(reg_neigh)
                            visited.append(reg_neigh)
                            regions[(y, x)].append(reg_neigh)

    if verbose:
        print(f"Found regions: {regions}")

    return regions


# Takes in a region list with all coords within the region and calculates
# the perimeter size of given region and its area
def calc_area_and_perimeters_region(region: list) -> int:
    perimeters = []

    # Check every pos in region
    for pos in region:
        (y, x) = pos
        # Check open spaces per pos in region
        for neighbor in [(y-1, x, "north"), (y+1, x, "south"),
                         (y, x-1, "west"), (y, x+1, "east")]:
            (n_y, n_x, _) = neighbor
            if (n_y, n_x) not in region:
                perimeters.append(neighbor)

    if verbose:
        print(f"Perimeter size for region {region} is {len(perimeters)}")

    return len(region), perimeters


# Takes in a perimeter list with all coords within the perimeter and
# calculates the number of sides of given region and its area
def calc_total_sides_region(perimeters: list) -> int:
    n_sides = 0

    visited = set()

    # Go through all perimeter places
    while perimeters:
        if verbose:
            print("Searching new side with current perimetes:", perimeters)
        start_per = perimeters.pop(0)

        # Start queue
        side_queue = [start_per]

        # Go through all perimeter coords alongside oneother (one side)
        n_sides += 1

        # BFS the side
        while side_queue:
            cur = side_queue.pop(0)

            # Get current per
            (y, x, s) = cur

            if verbose:
                print(f"Checking {(y, x)}")

            # Remove current per from list

            # Check if neighbouring same-sided perimeter exists
            for neighbor in [(y-1, x, s), (y+1, x, s),
                             (y, x-1, s), (y, x+1, s)]:
                # If so, go search for neighbor
                if neighbor in perimeters and neighbor not in visited:
                    if verbose:
                        print(f"Neighbour {neighbor} inside perimeter!")

                    visited.add(neighbor)
                    perimeters.remove(neighbor)
                    side_queue.append(neighbor)

        if verbose:
            print(f"Total side is {n_sides} in this perimeter")

    return n_sides


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("file_dir",
                        help="Directory of file which contains garden map")
    parser.add_argument("--verbose", "-v",
                        help="Makes the program mare verbose",
                        action="store_true")
    parser.add_argument("--bulk_discount",
                        help="Activates discount when buying in bulk" +
                        "(cost = area * n_sides)",
                        action="store_true")
    args = parser.parse_args()

    if args.verbose:
        verbose = True

    grid = file_to_grid(args.file_dir)

    regions = get_regions(grid)

    total_cost = 0
    if not args.bulk_discount:
        for region in regions.values():
            area, perimeters = calc_area_and_perimeters_region(region)
            total_cost += area * len(perimeters)

    elif args.bulk_discount:
        for region in regions.values():
            area, perimeters = calc_area_and_perimeters_region(region)
            n_sides = calc_total_sides_region(perimeters)
            total_cost += area * n_sides

    if verbose:
        print("----------")
    print(f"Total cost of fencing the garden is: {total_cost}")
