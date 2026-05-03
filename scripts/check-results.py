from pathlib import Path
import numpy as np


def read_frametimes(filename):
    times = []
    with open(filename) as file:
        for line in file:
            line.rstrip()
            chunks = line.split(" ")
            if len(chunks) != 3 or chunks[0] != "Frametime" or chunks[2] != "us\n":
                print(chunks)
                raise ValueError(line)
            times.append(int(chunks[1]))
    return np.array(times)


def check_result(result: Path):
    frametimes = read_frametimes(result)
    combined_frametimes = np.sum(frametimes)
    combined_frametime_seconds = combined_frametimes / 10**6
    print(combined_frametime_seconds)
    if combined_frametime_seconds < 28:
        print(
            f"invalid frametimes: {result} has only {combined_frametime_seconds} seconds"
        )
        print(
            "Please delete this benchmark out of the client and result directory and redo it"
        )


def main():
    result_data_path = Path("results")
    if not result_data_path.exists():
        print("Error: data path does not exist")
        exit(1)

    for result in result_data_path.glob("*.txt"):
        check_result(result)


if __name__ == "__main__":
    main()
