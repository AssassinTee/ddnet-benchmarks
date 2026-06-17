import shutil

from pathlib import Path
import sys

CLIENTS_DIR = "clients"


def setup_demos_for_client(client_userdir_path):
    demos = Path("resources/demos")
    for demo in demos.glob("*.demo"):
        dest_directory = client_userdir_path / "demos"
        dest_name = dest_directory / demo.name
        if dest_name.exists():
            print(f"{dest_name} exists :)")
        else:
            print(f"cp {demo} {dest_name}")
            shutil.copyfile(demo, dest_name)

        map_name = demo.name.split("-")[0]

        benchmark_name = f"benchmark-{map_name}.cfg"
        benchmark_directory = client_userdir_path / benchmark_name
        if benchmark_directory.exists():
            print(f"{benchmark_directory} exists :)")
        else:
            print(f"creating {benchmark_name}")
            with open(benchmark_directory, "w") as f:
                # f.write("toggle_local_console\n")
                f.write("demo_play\n")
                f.write(f"benchmark_quit 30 benchmark-{map_name}.txt\n")


def main(client_dir):
    clients_path = Path(client_dir)
    glob_userdir = "ddnet-*/DDNet-*/userdir" if client_dir == CLIENTS_DIR else "build/userdir"
    for settings_file in clients_path.glob(glob_userdir):
        setup_demos_for_client(settings_file)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        client_dir = sys.argv[1]
    else:
        client_dir = CLIENTS_DIR
    main(client_dir)
