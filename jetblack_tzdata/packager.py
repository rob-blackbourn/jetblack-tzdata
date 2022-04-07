"""Make the npm package"""

import json
import subprocess
from pathlib import Path
from typing import List


def _make_package_version(
        temp_folder: Path,
        version: str,
        is_overwriting: bool,
        is_verbose: bool
) -> None:
    if is_verbose:
        print("Making package")

    collect_file = temp_folder / "collect" / version / 'tzdata.json'
    package_folder = Path("package") / "dist" / version
    if not package_folder.exists():
        package_folder.mkdir(parents=True, exist_ok=True)
    elif is_overwriting:
        subprocess.run(
            ['rm', '-r', str(package_folder)],
            check=True
        )
    else:
        return

    with open(collect_file, "rt", encoding='utf-8') as fp:
        tzdata = json.load(fp)

    for key, data in tzdata.items():
        parts = key.split('/')
        filename = parts[-1] + '.json'
        folder = package_folder
        if len(parts) > 1:
            for part in parts[:-1]:
                folder = folder / part
        path = folder / filename
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
        print(f"Writing {path}")
        with open(path, "wt", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2)

    zones = list(tzdata.keys())
    zones.sort()
    zones_file = package_folder / 'zones.json'
    with open(zones_file, "wt", encoding="utf-8") as fp:
        json.dump(zones, fp, indent=2)


def make_package(
        temp_folder: Path,
        versions: List[str],
        is_overwriting: bool,
        is_verbose: bool
) -> None:
    for version in versions:
        _make_package_version(
            temp_folder,
            version,
            is_overwriting,
            is_verbose
        )
