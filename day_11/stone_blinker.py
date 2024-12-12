import argparse as ap


verbose = False


# Reads in the file and converts it to a list of ints
def file_to_list(file_dir: str) -> list[int]:
    raw_file: str = ""

    # Check if file exists
    try:
        with open(args.file_dir, "r") as f:
            raw_file = f.readline()
    except FileNotFoundError:
        print("File", args.file_dir, "not found")
        exit(-1)

    # Split string into list and make it ints
    sequence = [int(x) for x in raw_file.split(" ")]

    if verbose:
        print("Sequence from file:", sequence)

    return sequence


# Simulates the blinking behaviour of magical pluto rocks
def simulate_blinks(sequence: list[int], n_blinks: int) -> list[int]:
    if n_blinks > 25:
        print("WARNING: If the program takes too long, try using the flag" +
              "--only_count")

    # Store initial sequence
    queue = [sequence]

    # Number of times simulation is ran
    for blink in range(n_blinks):
        # Go through all sequence parts in queue, split up for RAM
        for _ in range(len(queue)):
            # Get first sequence of batch
            sequence = queue.pop(0)

            # Go through all rocks
            i = 0
            while i < (len(sequence)):
                # If the stone is equal to 0, make it 1
                if sequence[i] == 0:
                    sequence[i] = 1
                    i += 1
                # If stone has even number of digits, split in two
                elif len(str(sequence[i])) % 2 == 0:
                    str_digit = str(sequence[i])
                    middle_of_digit = len(str_digit) // 2
                    first_half = str_digit[:middle_of_digit]
                    second_half = str_digit[middle_of_digit:]
                    sequence[i] = int(second_half)
                    sequence.insert(i, int(first_half))
                    i += 2
                # If no rule applies, multiply by 2024
                else:
                    sequence[i] *= 2024
                    i += 1

            if len(sequence) >= (n_blinks // 2) + 2:
                middle_of_sequence = len(sequence) // 2
                queue.append(sequence[:middle_of_sequence])
                queue.append(sequence[middle_of_sequence:])
            else:
                queue.append(sequence)

        if verbose:
            print("After", blink + 1, "blinks, the sequence is:", queue)

        if blink % (n_blinks // 10 + 1) == 0:
            total_sequence_size = sum([len(x) for x in queue])
            print(f"{blink} blinks passed, size is {total_sequence_size}")

    return queue


# Simulates blinks, but only remembers count
def simulate_count(sequence: list[int], n_blinks: int):
    # Store how often a single number occurs in sequence
    n_number_now: dict[int: int] = {}
    n_number_next: dict[int: int] = {}

    for x in sequence:
        if x in n_number_now.keys():
            n_number_now[x] += 1
        else:
            n_number_now[x] = 1

    if verbose:
        print(f"Stones in dict: {n_number_now}")

    for blink in range(n_blinks):
        for distinct_stone in n_number_now.keys():
            # If the stone is equal to 0, make it 1
            if distinct_stone == 0:
                if 1 in n_number_next.keys():
                    n_number_next[1] += n_number_now[0]
                else:
                    n_number_next[1] = n_number_now[0]
            # If stone has even number of digits, split in two
            elif len(str(distinct_stone)) % 2 == 0:
                # Check if even digits
                str_digit = str(distinct_stone)
                middle_of_digit = len(str_digit) // 2
                first_half = int(str_digit[:middle_of_digit])
                second_half = int(str_digit[middle_of_digit:])

                # Store amount of equal stones
                if first_half in n_number_next.keys():
                    n_number_next[first_half] += n_number_now[distinct_stone]
                else:
                    n_number_next[first_half] = n_number_now[distinct_stone]

                if second_half in n_number_next.keys():
                    n_number_next[second_half] += n_number_now[distinct_stone]
                else:
                    n_number_next[second_half] = n_number_now[distinct_stone]

            # If no rule applies, multiply by 2024
            else:
                if distinct_stone * 2024 in n_number_next.keys():
                    n_number_next[distinct_stone*2024] += n_number_now[
                                                            distinct_stone
                                                            ]
                else:
                    n_number_next[distinct_stone*2024] = n_number_now[
                                                            distinct_stone
                                                            ]

        if verbose:
            print("After", blink + 1,
                  "blinks, the number of stones per value are:", n_number_next)

        n_number_now = n_number_next
        n_number_next = {}

    return sum(n_number_now.values())


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("file_dir", help="File directory of stone sequence")
    parser.add_argument("total_blinks",
                        help="Number of blinks happening in simulation",
                        type=int)
    parser.add_argument("--verbose", "-v", help="Makes program more verbose",
                        action="store_true")
    parser.add_argument("--only_count", help="Only remembers number of rocks",
                        action="store_true")

    args = parser.parse_args()

    if args.verbose:
        verbose = True

    sequence = file_to_list(args.file_dir)

    if not args.only_count:
        split_sequences = simulate_blinks(sequence, args.total_blinks)

        total_stones = sum([len(x) for x in split_sequences])
        print(f"Final sequence is: {split_sequences} \n" +
              f"Number of stones: {total_stones}")
    else:
        total_rocks = simulate_count(sequence, args.total_blinks)
        print(f"Number of stones: {total_rocks}")
