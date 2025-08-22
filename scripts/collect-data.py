from pathlib import Path
import shutil


def main():
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


if __name__ == "__main__":
    main()
