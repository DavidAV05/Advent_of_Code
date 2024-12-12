import argparse as ap


verbose = False


# Reads in the file and turns it into the grid
def file_to_grid(map_file: str) -> list[list]:
    try:
        with open(map_file, "r") as f:
            read_map = f.readlines()
    except FileNotFoundError:
        print("File:", map_file, "not found")
        exit(0)

    # Strip all \n
    read_map = [x.strip() for x in read_map]

    # Make grid of lists
    grid = [[x for x in y] for y in read_map]

    # Remove empty lists
    grid = [x for x in grid if x]

    grid_size = (len(grid), len(grid[0]))

    return grid, grid_size


# Locate antennas within the grid
def locate_antennas(grid: dict) -> dict:
    antennas_dict: dict[str, list] = {}

    # Loop through whole grid
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            # If place isn't equal to empty space or antinode
            if grid[y][x] != "." and grid[y][x] != "#":
                # If new found frequency
                if grid[y][x] not in antennas_dict.keys():
                    antennas_dict[grid[y][x]] = [(y, x)]
                # If already found frequency
                else:
                    antennas_dict[grid[y][x]].append((y, x))

    return antennas_dict


# Counts the total antinodes within the given grid
def count_antinodes(ants_pos: dict[str, list],
                    grid_size: tuple[int, int],
                    harmonic: bool) -> int:
    antinode_pos = set()

    # Loop through all frequencies
    for x in ants_pos:
        # For every antenna on frequency x
        for pos in ants_pos[x]:
            # Check every other antenna within frequency
            for other_pos in ants_pos[x]:
                if pos != other_pos:
                    if not harmonic:
                        found_pos = (None, None)
                        found_pos = (pos[0] - 2 * (pos[0] - other_pos[0]),
                                     pos[1] - 2 * (pos[1] - other_pos[1]))
                        if (found_pos[0] < grid_size[0]
                                and found_pos[1] < grid_size[1]
                                and found_pos[0] >= 0
                                and found_pos[1] >= 0):
                            antinode_pos.add(found_pos)
                            if verbose:
                                print("From:", pos, "found pos:",
                                      found_pos, "for freq", x)
                    if harmonic:
                        for i in range(1, max(grid_size)):
                            found_pos = (None, None)
                            found_pos = (pos[0] - i * (pos[0] - other_pos[0]),
                                         pos[1] - i * (pos[1] - other_pos[1]))

                            if (found_pos[0] < grid_size[0]
                                    and found_pos[1] < grid_size[1]
                                    and found_pos[0] >= 0
                                    and found_pos[1] >= 0):
                                antinode_pos.add(found_pos)
                                if verbose:
                                    print("From:", pos, "found pos:",
                                          found_pos, "for freq", x)

                            else:
                                break

    return len(antinode_pos)


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("map_file", help="File that contains the map text",
                        type=str)
    parser.add_argument("--verbose", "-v",
                        help="Makes the program more verbose",
                        action="store_true")
    parser.add_argument("--harmonic",
                        help="Calculates harmonic resonant",
                        action="store_true")
    args = parser.parse_args()

    if args.verbose:
        verbose = True

    grid, grid_size = file_to_grid(args.map_file)

    antennas_pos = locate_antennas(grid)

    n_antinodes = count_antinodes(antennas_pos, grid_size, args.harmonic)

    print("Found:", n_antinodes, "antinodes")
