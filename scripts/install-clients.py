import json
import sys
import os
import tarfile
import zipfile

import requests
from pathlib import Path
import platform


def get_os_suffix() -> str:
    if platform.system() == 'Linux':
        return 'linux-x86_64.tar.gz'
    elif platform.system() == 'Windows':
        return 'win64.zip'
    else:
        raise ValueError("OS not supported, feel free to PR")


def download_file(client_version, output_dir, os_suffix):
    local_filename = Path(output_dir) / f"ddnet-{client_version}-{os_suffix}"
    if local_filename.exists():
        print(f"download exists already :) at \"{str(local_filename)}\"")
        return local_filename

    url = f"https://ddnet.org/downloads/DDNet-{client_version}-{os_suffix}"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(str(local_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {str(local_filename)}")
        return local_filename

def open_archive(local_filename: Path):
    destination_directory = f"clients/{local_filename.stem}"
    if Path(destination_directory).exists():
        print(f"Archive directory exists already :) at \"{destination_directory}\"")
        return
    if tarfile.is_tarfile(local_filename):
        with tarfile.open(local_filename) as f:
            f.extractall(path=destination_directory)
    elif zipfile.is_zipfile(local_filename):
        with zipfile.ZipFile(local_filename, 'r') as client_zip:
            client_zip.extractall(path=destination_directory)
    else:
        raise ValueError("unknown archive format")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <path_to_json>")
        sys.exit(1)

    json_path = sys.argv[1]

    with open(json_path, 'r') as f:
        data = json.load(f)

    # Expecting JSON like: { "clients": ["https://example.com/client1.zip", "https://example.com/client2.zip"] }
    clients = data.get("client_list", [])

    if not clients:
        print("No clients found in JSON!")
        sys.exit(1)

    output_dir = Path("clients")
    assert output_dir.exists()

    os_suffix = get_os_suffix()

    for client_version in clients:
        try:
            filename = download_file(client_version, output_dir, os_suffix)
            open_archive(filename)
        except Exception as e:
            print(f"Failed to download ddnet-{client_version}: {e}")


if __name__ == "__main__":
    main()
