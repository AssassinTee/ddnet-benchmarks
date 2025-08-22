import shutil

from storage_finder import StorageFinder
from pathlib import Path


def main():
    # this one ignores steam directories
    data_path = StorageFinder.instance().getDataPath()
    print("Ignore the client error, we don't need the client")
    print(data_path)
    demos = Path("resources/demos")
    print(demos.absolute())
    for demo in demos.glob("*.demo"):
        dest_directory = data_path / "demos"
        dest_name = dest_directory / demo.name
        if dest_name.exists():
            print(f"{dest_name} exists :)")
        else:
            print(f"cp {demo} {dest_name}")
            shutil.copyfile(demo, dest_name)

        map_name = demo.name.split("-")[0]

        benchmark_name = f"benchmark-{map_name}.cfg"
        benchmark_directory = data_path / benchmark_name
        if benchmark_directory.exists():
            print(f"{benchmark_directory} exists :)")
        else:
            print(f"creating {benchmark_name}")
            with open(benchmark_directory, "w") as f:
                f.write("toggle_local_console\n")
                f.write("demo_play\n")
                f.write(f"benchmark_quit 30 benchmark-{map_name}.txt\n")


if __name__ == "__main__":
    main()
