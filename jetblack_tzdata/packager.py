"""Make the npm package"""

import json
import logging
import subprocess
from pathlib import Path
from typing import List

LOGGER = logging.getLogger(__name__)


def _make_package_version(
        temp_folder: Path,
        version: str,
        is_overwriting: bool
) -> None:
    LOGGER.info("Making package for version: %s", version)

    package_folder = Path("package") / "dist" / version
    if package_folder.exists():
        if is_overwriting:
            LOGGER.debug("Clearing folder: %s", package_folder)
            subprocess.run(
                ['rm', '-r', str(package_folder)],
                check=True
            )
        else:
            return
    package_folder.mkdir(parents=True, exist_ok=True)

    collect_file = temp_folder / "collect" / version / 'tzdata.json'
    with open(collect_file, "rt", encoding='utf-8') as fp:
        tzdata = json.load(fp)

    min_collect_file = temp_folder / "collect" / version / 'tzdata.min.json'
    with open(min_collect_file, "rt", encoding='utf-8') as fp:
        min_tzdata = json.load(fp)

    for key, data in tzdata.items():
        parts = key.split('/')
        filename = parts[-1] + '.json'
        min_filename = parts[-1] + '.min.json'
        folder = package_folder
        if len(parts) > 1:
            for part in parts[:-1]:
                folder = folder / part
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
        path = folder / filename
        min_path = folder / min_filename
        print(f"Writing {path}")
        with open(path, "wt", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2)
        with open(min_path, "wt", encoding="utf-8") as fp:
            json.dump(min_tzdata[key], fp)

    zones = list(tzdata.keys())
    zones.sort()
    zones_file = package_folder / 'zones.json'
    with open(zones_file, "wt", encoding="utf-8") as fp:
        json.dump(zones, fp, indent=2)


def make_package(
        temp_folder: Path,
        versions: List[str],
        is_overwriting: bool
) -> None:
    for version in versions:
        _make_package_version(
            temp_folder,
            version,
            is_overwriting
        )
