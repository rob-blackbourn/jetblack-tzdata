"""Downloader for tzdata"""

import logging
from pathlib import Path
import subprocess
from typing import List

LOGGER = logging.getLogger(__name__)


def _download_file(tzdata_url: str, curl_file: Path) -> None:
    args = ["curl", tzdata_url, "-o", str(curl_file)]

    LOGGER.debug("Executing: %s", ' '.join(args))

    subprocess.run(
        args,
        check=True
    )


def _unpack_file(curl_file: Path, dest_folder: Path) -> None:
    args = ["tar", "xf", str(curl_file), "-C", str(dest_folder)]

    LOGGER.debug("Executing: %s", ' '.join(args))

    subprocess.run(
        args,
        check=True
    )


def _download_version(
        temp_folder: Path,
        tzdata_url: str,
        version: str,
        is_overwriting: bool
) -> None:
    curl_folder = temp_folder / 'curl' / version

    if curl_folder.exists():
        if is_overwriting:
            LOGGER.debug("Clearing folder: %s", curl_folder)
            subprocess.run(
                ['rm', '-r', str(curl_folder)],
                check=True
            )
        else:
            return
    curl_folder.mkdir(parents=True, exist_ok=True)

    curl_file = curl_folder / 'data.tar.gz'
    _download_file(tzdata_url, curl_file)

    dest_folder = temp_folder / 'download' / version
    if dest_folder.exists():
        if is_overwriting:
            LOGGER.debug("Clearing folder: %s", dest_folder)
            subprocess.run(
                ['rm', '-r', str(dest_folder)],
                check=True
            )
        else:
            return
    dest_folder.mkdir(parents=True, exist_ok=True)

    _unpack_file(curl_file, dest_folder)


def download_data(
        temp_folder: Path,
        tzdata_url: str,
        versions: List[str],
        is_overwriting: bool
) -> None:
    for version in versions:
        _download_version(
            temp_folder,
            tzdata_url,
            version,
            is_overwriting
        )
