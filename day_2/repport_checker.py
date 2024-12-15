import argparse as ap

verbose = False


def parse_file(file_dir: str) -> list[list[int]]:
    """Parses the input file and returns a list of reports."""
    reports = []

    with open(file_dir, "r") as f:
        for line in f:
            report = list(map(int, line.strip().split()))
            reports.append(report)

    if verbose:
        print("Found reports:", reports)

    return reports


def is_safe(report: list[int], max_step: int) -> bool:
    increasing = report[0] < report[1]

    for i in range(len(report) - 1):
        diff = report[i + 1] - report[i]
        if abs(diff) > max_step or (diff > 0) != increasing or diff == 0:
            return False

    return True


def validate_safety(report: list[int], max_step: int, damper: bool) -> bool:
    if is_safe(report, max_step):
        return True

    if not damper:
        return False

    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1:]
        if is_safe(modified_report, max_step):
            if verbose:
                print(f"Report {report} is safe with dampener by removing" +
                      f"level at index {i}: {modified_report}")
            return True

    return False


if __name__ == "__main__":
    parser = ap.ArgumentParser()

    parser.add_argument("file_dir", help="Directory file containing reports")
    parser.add_argument("max_step", help="Max step size allowed within report",
                        type=int)
    parser.add_argument("--verbose", "-v", help="Makes program more verbose",
                        action="store_true")
    parser.add_argument("--damper", "-d", help="Uses problem dampener",
                        action="store_true")

    args = parser.parse_args()

    verbose = args.verbose

    reports = parse_file(args.file_dir)

    total_safe = 0

    for report in reports:
        if validate_safety(report, args.max_step, args.damper):
            total_safe += 1

    print("Total safe reports:", total_safe)
