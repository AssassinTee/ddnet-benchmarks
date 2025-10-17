import os
import subprocess
from pathlib import Path

DEMOS_DIR = "resources/demos"
CLIENTS_DIR = "clients"
BENCHMARKS_DIR = "benchmarks"  # Directory to store benchmark outputs
DDNET_EXECUTABLE = "DDNet.exe"  # Path to DDNet executable


def extract_map_name(demo_filename: Path) -> str:
    # Example: "Abyss-Benchmark.demo" -> "Abyss-Benchmark"
    return demo_filename.name.split("-")[0]


def benchmark_exists(client: Path, demo_filename: Path) -> bool:
    # Benchmarks will be stored like benchmarks/client/demo_name.log
    benchmark_path = client.parent / f"benchmark-{extract_map_name(demo_filename)}.txt"
    return benchmark_path.exists()


def run_benchmark(client: Path, demo_file: Path):
    if benchmark_exists(client, demo_file):
        print(f"[SKIP] Benchmark already exists for {client} - {demo_file.name}")
        return

    map_name = extract_map_name(demo_file)

    # Build command
    command = f'{DDNET_EXECUTABLE} "play demos/{demo_file.name}; exec benchmark-{map_name}.cfg"'
    print(f"[RUN] {command} for client {client}")

    # Run DDNet.exe with client's config/environment
    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=client.parent)

    # Save output to log
    for line in result.stdout.split('\n'):
        print(line)

    print(f"[DONE] Benchmark created")


def main():
    demos = [f for f in Path(DEMOS_DIR).glob("*.demo")]
    clients = [d for d in Path(CLIENTS_DIR).glob("ddnet-*/DDNet-*/DDNet.exe")]

    if not demos:
        print("No demos found in resources/demos/")
        return
    if not clients:
        print("No clients found in clients/")
        return

    for client in clients:
        print(f"\n=== Processing Client: {client} ===")
        for demo in demos:
            run_benchmark(Path(client), Path(demo))


if __name__ == "__main__":
    main()
