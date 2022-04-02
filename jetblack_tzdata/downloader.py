"""Downloader for tzdata"""

from pathlib import Path
import subprocess


def download_data(
    temp_folder: Path = Path("temp"),
    tzdata_url: str = 'ftp://ftp.iana.org/tz/tzdata-latest.tar.gz',
    version: str = 'latest'
) -> None:
    if not temp_folder.exists():
        temp_folder.mkdir(parents=True, exist_ok=True)

    curl_folder = temp_folder / 'curl' / version
    if not curl_folder.exists():
        curl_folder.mkdir(parents=True, exist_ok=True)

    curl_file = curl_folder / 'data.tar.gz'

    subprocess.run(
        ["curl", tzdata_url, "-o", str(curl_file)],
        check=True
    )

    dest_folder = temp_folder / 'download' / version
    if not dest_folder.exists():
        dest_folder.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        ["tar", "xf", str(curl_file), "-C", str(dest_folder)],
        check=True
    )
