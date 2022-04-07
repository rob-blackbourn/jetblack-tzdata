"""Compile with zic"""

from pathlib import Path
import subprocess


def compile_files(
        temp_folder: Path,
        version: str,
        is_verbose: bool
) -> None:
    if is_verbose:
        print("Compiling files")

    download_folder = (temp_folder / 'download' / version).resolve()

    output_folder = (temp_folder / 'zic' / version).resolve()
    if not output_folder.exists():
        output_folder.mkdir(parents=True, exist_ok=True)

    file_names = [
        'africa',
        'antarctica',
        'asia',
        'australasia',
        'etcetera',
        'europe',
        'northamerica',
        'southamerica',
        'backward'
    ]

    for file_name in file_names:
        download_file = download_folder / file_name

        args = ["zic", "-d", str(output_folder), str(download_file)]

        if is_verbose:
            print(f"Executing: {args}")

        subprocess.run(args, check=True)
