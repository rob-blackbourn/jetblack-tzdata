"""Dump the compiled files"""

import logging
from pathlib import Path
import subprocess
from typing import List

from jetblack_tzdata.downloader import LOGGER

LOGGER = logging.getLogger(__name__)


def _dump_file(
        zic_file: Path,
        zic_base_folder: Path,
        zdump_folder: Path
) -> None:
    LOGGER.debug("Dumping file: %s", zic_file)

    args = ["zdump", "-v", str(zic_file)]

    LOGGER.debug("Executing: %s", ' '.join(args))

    result = subprocess.run(
        args,
        check=True,
        capture_output=True,
        encoding='utf-8'
    )

    if not result.stdout:
        args = ["zdump", "UTC", str(zic_file)]

        LOGGER.debug("Executing: %s", ' '.join(args))

        result = subprocess.run(
            ["zdump", "UTC", str(zic_file)],
            check=True,
            capture_output=True,
            encoding='utf-8'
        )

    zdump_name = zic_file.name + '.zdump'
    zdump_file = zdump_folder / zdump_name

    with open(zdump_file, "wt", encoding="utf-8") as fp:
        fp.write(result.stdout.replace(str(zic_base_folder) + '/', ''))


def _dump_folder(
        zic_folder: Path,
        zic_base_folder: Path,
        zdump_folder: Path
) -> None:
    LOGGER.debug("Dumping folder: %s", zic_folder)

    if not zdump_folder.exists():
        zdump_folder.mkdir(parents=True, exist_ok=True)

    for path in zic_folder.iterdir():

        if path.is_dir():
            _dump_folder(
                path,
                zic_base_folder,
                zdump_folder / path.name
            )
        else:
            _dump_file(
                path,
                zic_base_folder,
                zdump_folder
            )


def _dump_version(
        temp_folder: Path,
        version: str,
        is_overwriting: bool,
) -> None:
    LOGGER.info("Dumping files for version: %s", version)

    zic_folder = (temp_folder / "zic" / version).resolve()
    zdump_folder = (temp_folder / "zdump" / version).resolve()

    if zdump_folder.exists():
        if is_overwriting:
            LOGGER.debug("Clearing folder %s", zdump_folder)
            subprocess.run(
                ['rm', '-r', str(zdump_folder)],
                check=True
            )
        else:
            return
    zdump_folder.mkdir(parents=True, exist_ok=True)

    _dump_folder(zic_folder, zic_folder, zdump_folder)


def dump_files(
        temp_folder: Path,
        versions: List[str],
        is_overwriting: bool
) -> None:
    for version in versions:
        _dump_version(temp_folder, version, is_overwriting)
