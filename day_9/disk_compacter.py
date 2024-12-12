import argparse as ap

verbose = False


# Convert disk from string to formatted list
def convert_disk(file_dir: str):
    # Read the file
    raw_disk: str = open(file_dir, "r").readline().strip()

    # Make ints
    raw_disk = [int(x) for x in raw_disk]
    if verbose:
        print("Raw disk: ", raw_disk)

    converted_disk = [0] * len(raw_disk)

    curr_index = 0

    file_data = [None] * (len(raw_disk) // 2 + 1)

    for i in range(len(raw_disk)):
        # If i is even, read nunmber corresponds to blocks
        if i % 2 == 0:
            converted_disk[i] = [i // 2] * raw_disk[i]

            # Store file data
            file_data[i // 2] = {
                "index": curr_index,
                "size": raw_disk[i]
            }

            curr_index += raw_disk[i]
        # If uneven, read number corresponds to empty space
        else:
            converted_disk[i] = ["."] * raw_disk[i]
            curr_index += raw_disk[i]

    # Remove empty spaces of size zero
    converted_disk = [x for x in converted_disk if x]

    # Reformate list of lists to single list
    converted_disk = [
        str(x)
        for xs in converted_disk
        for x in xs
    ]

    if verbose:
        print("Converted disk: ", converted_disk)

    return converted_disk, file_data


# Zip the disk by moving all blocks to the start within empty spaces
def zip_disk(disk: list, file_data: list, whole_files=False):
    # If disk has length of 1
    if len(disk) < 1:
        return disk

    # Start at beginning and end of disk
    start = 0
    end = len(disk) - 1

    if not whole_files:
        # Loop through disk
        while start < end:
            # Find first empty space
            while disk[start] != ".":
                start += 1

            # Find last non empty space
            while disk[end] == ".":
                end -= 1

            # Swap values
            temp = disk[start]
            disk[start] = disk[end]
            disk[end] = temp

            # Move one along
            start += 1
            end -= 1

    if whole_files:
        # Whole file movement for part two
        for file_id in range(len(file_data) - 1, -1, -1):

            if file_id % 100 == 0:
                print("Zipping file: ", file_id)
            file_start = file_data[file_id]["index"]
            file_size = file_data[file_id]["size"]

            # Find the leftmost span of free space that fits the file
            i = 0
            while i <= end:
                # Find the start of a free space span
                while i <= end and disk[i] != ".":
                    i += 1
                free_start = i

                # Count the size of this free space span
                while i <= end and disk[i] == ".":
                    i += 1
                free_size = i - free_start

                # Check if the span is large enough and left of the file
                if free_size >= file_size and free_start < file_start:
                    # Move the file to this span
                    for j in range(file_size):
                        disk[free_start + j] = disk[file_start + j]
                        disk[file_start + j] = "."
                    break

            if verbose:
                print("Disk after: ", "".join(disk), "\n")

    # print(disk)
    if verbose:
        print("Zipped disk: ", disk)

    return disk


# Calculates the checksum of a zipped disk
def calc_checksum(disk: list):
    checksum = 0
    i = 0

    for i in range(len(disk)):
        if disk[i] != ".":
            checksum += i * int(disk[i])

    return checksum


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("file_dir", help="The directory of the disk file",
                        type=str)
    parser.add_argument("--verbose", "-v", help="Makes program more verbose",
                        action="store_true")
    parser.add_argument("--packed",
                        help="Zips disk on whole files instead of blocks",
                        action="store_true")
    args = parser.parse_args()

    disk_file = args.file_dir

    if args.verbose:
        verbose = True

    converted_disk, file_data = convert_disk(disk_file)

    zipped_disk = zip_disk(converted_disk, file_data, whole_files=args.packed)

    checksum = calc_checksum(zipped_disk)

    if verbose:
        # Distinguish from debug prints
        print("------")

    print("Checksum: ", checksum)
