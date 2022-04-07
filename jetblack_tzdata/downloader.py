"""Downloader for tzdata"""

from pathlib import Path
import subprocess


def _download_file(tzdata_url: str, curl_file: Path, is_verbose: bool) -> None:
    args = ["curl", tzdata_url, "-o", str(curl_file)]

    if is_verbose:
        print(f"Executing: {' '.join(args)}")

    subprocess.run(
        args,
        check=True
    )


def _unpack_file(curl_file: Path, dest_folder: Path, is_verbose: bool) -> None:
    args = ["tar", "xf", str(curl_file), "-C", str(dest_folder)]

    if is_verbose:
        print(f"Executing: {' '.join(args)}")

    subprocess.run(
        args,
        check=True
    )


def download_data(
    temp_folder: Path,
    tzdata_url: str,
    version: str,
    is_verbose: bool
) -> None:
    if not temp_folder.exists():
        temp_folder.mkdir(parents=True, exist_ok=True)

    curl_folder = temp_folder / 'curl' / version
    if not curl_folder.exists():
        curl_folder.mkdir(parents=True, exist_ok=True)

    curl_file = curl_folder / 'data.tar.gz'
    _download_file(tzdata_url, curl_file, is_verbose)

    dest_folder = temp_folder / 'download' / version
    if not dest_folder.exists():
        dest_folder.mkdir(parents=True, exist_ok=True)

    _unpack_file(curl_file, dest_folder, is_verbose)
