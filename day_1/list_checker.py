import argparse as ap


verbose = False


def parse_file(file_dir: str) -> list:
    list0 = []
    list1 = []

    try:
        with open(file_dir, "r") as f:
            line = f.readline().strip()
            while line != "":
                # Split line into ints
                line = line.split()
                line = [int(x) for x in line]

                # Append each value to a list
                list0.append(line[0])
                list1.append(line[1])

                # Read next line
                line = f.readline().strip()
    except FileNotFoundError:
        print(f"File {file_dir} not found")
        exit(-1)

    return sorted(list0), sorted(list1)


def calc_distance(list0, list1) -> int:
    if len(list0) != len(list1):
        return -1

    dist = 0

    for i in range(len(list0)):
        dist += abs(list0[i] - list1[i])

    return dist


def calc_similarity(list0, list1) -> int:
    sim_score = 0

    list1_n_times = {}

    for x in list1:
        if x in list1_n_times.keys():
            list1_n_times[x] += 1
        else:
            list1_n_times[x] = 1

    for x in list0:
        sim_score += x * list1_n_times.get(x, 0)

    return sim_score


if __name__ == "__main__":
    parser = ap.ArgumentParser()

    parser.add_argument("file_dir", help="Directory to file containing lists")
    parser.add_argument("--verbose", "-v", help="Makes program more verbose",
                        action="store_true")
    parser.add_argument("--similarity", help="Calc similarity lists",
                        action="store_true")

    args = parser.parse_args()

    if args.verbose:
        verbose = True

    list0, list1 = parse_file(args.file_dir)

    if verbose:
        print("Lists are:", list0, list1)

    if not args.similarity:
        distance = calc_distance(list0, list1)
        print("Total distance is:", distance)
    else:
        similarity = calc_similarity(list0, list1)
        print("Total similarity is:", similarity)
