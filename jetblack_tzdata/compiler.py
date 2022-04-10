"""Compile with zic"""

import logging
from pathlib import Path
import subprocess
from typing import List

LOGGER = logging.getLogger(__name__)


def _compile_version(
        temp_folder: Path,
        version: str,
        is_overwriting: bool
) -> None:
    LOGGER.info("Compiling files for version: %s", version)

    download_folder = (temp_folder / 'download' / version).resolve()

    output_folder = (temp_folder / 'zic' / version).resolve()
    if output_folder.exists():
        if is_overwriting:
            LOGGER.debug("Clearing folder: %s", output_folder)
            subprocess.run(
                ['rm', '-r', str(output_folder)],
                check=True
            )
        else:
            return
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

        LOGGER.debug("Executing: %s", args)

        subprocess.run(args, check=True)


def compile_files(
        temp_folder: Path,
        versions: List[str],
        is_overwriting: bool
) -> None:
    for version in versions:
        _compile_version(temp_folder, version, is_overwriting)
