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
    # Number of times simulation is ran
    for blink in range(n_blinks):
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

        if verbose:
            print("After", blink + 1, "blinks, the sequence is:", sequence)

        if blink % (n_blinks // 10 + 1) == 0:
            print(f"{blink} blinks passed, size is {len(sequence)}")

    return sequence


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("file_dir", help="File directory of stone sequence")
    parser.add_argument("total_blinks",
                        help="Number of blinks happening in simulation",
                        type=int)
    parser.add_argument("--verbose", "-v", help="Makes program more verbose",
                        action="store_true")

    args = parser.parse_args()

    if args.verbose:
        verbose = True

    sequence = file_to_list(args.file_dir)

    sequence = simulate_blinks(sequence, args.total_blinks)

    print(f"Final sequence is: {sequence} \nNumber of stones: {len(sequence)}")
