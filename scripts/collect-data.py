from pathlib import Path
import shutil
import sys
from typing import Optional


def main(client_dir: Optional[str], result_dir: Optional[str]):
    if not client_dir or not result_dir:
        clients = Path("clients")
        results = Path("results")
        for directory in clients.glob("*"):
            if directory.is_dir():
                client_version = directory.name.split("-")[1]
                print(f"Found version {client_version}")
                for benchmark in directory.rglob("benchmark-*.txt"):
                    benchmark_name = benchmark.name
                    results_name = results / f"{client_version}-{benchmark_name}"
                    shutil.copyfile(benchmark, results_name)

    else:
        results = Path(result_dir)
        results.mkdir(exist_ok=True)
        client = Path(client_dir)
        for benchmark in client.rglob("benchmark-*.txt"):
            benchmark_name = benchmark.name
            results_name = results / f"{client.name}-{benchmark_name}"
            shutil.copyfile(benchmark, results_name)


if __name__ == "__main__":
    client_dir = None
    result_dir = None

    if len(sys.argv) != 1 and len(sys.argv) != 3:
        print(f"Usage {sys.argv[0]} [client_dir, result_dir]")
        sys.exit(1)

    if len(sys.argv) >= 3:
        client_dir = sys.argv[1]
        result_dir = sys.argv[2]

    main(client_dir, result_dir)
