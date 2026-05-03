from pathlib import Path
import shutil
import sys

CLIENTS_DIR = "clients"
SETTINGS_NAME = "settings_ddnet.cfg"
RESOURCES = "resources"


def switch_userdir(filepath: Path):
    updated_lines = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()

            # Only replace the active config line, not comments
            if stripped.startswith("add_path") and "$USERDIR" in stripped:
                line = line.replace("$USERDIR", "userdir")

            updated_lines.append(line)

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)


def create_userdir(client_dir: Path):
    directories = ["userdir", "userdir/demos"]
    for user_dir_part in directories:
        new_dir = client_dir / user_dir_part
        new_dir.mkdir(exist_ok=True)


def copy_settings(client_dir: Path, backend="vulkan"):
    destination_file = client_dir / "userdir" / SETTINGS_NAME
    resource_file = Path(RESOURCES) / "config" / f"settings_ddnet_{backend}.cfg"
    assert resource_file.parent.exists()
    shutil.copyfile(resource_file, destination_file)

    assert resource_file.exists()


def main(backend):
    clients_path = Path(CLIENTS_DIR)
    for settings_file in clients_path.glob("ddnet-*/DDNet-*/storage.cfg"):
        switch_userdir(settings_file)
        create_userdir(settings_file.parent)
        copy_settings(settings_file.parent, backend)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        backend = sys.argv[1]
    else:
        backend = "vulkan"
    main(backend)
