"""Compile with zic"""

from pathlib import Path
import subprocess
from typing import List


def _compile_version(
        temp_folder: Path,
        version: str,
        is_overwriting: bool,
        is_verbose: bool
) -> None:
    if is_verbose:
        print("Compiling files")

    download_folder = (temp_folder / 'download' / version).resolve()

    output_folder = (temp_folder / 'zic' / version).resolve()
    if not output_folder.exists():
        output_folder.mkdir(parents=True, exist_ok=True)
    elif is_overwriting:
        subprocess.run(
            ['rm', '-r', str(output_folder)],
            check=True
        )
    else:
        return

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


def compile_files(
        temp_folder: Path,
        versions: List[str],
        is_overwriting: bool,
        is_verbose: bool
) -> None:
    for version in versions:
        _compile_version(temp_folder, version, is_overwriting, is_verbose)
