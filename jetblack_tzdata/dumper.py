"""Dump the compiled files"""

from pathlib import Path
import subprocess


def _dump_file(zic_file: Path, zic_base_folder: Path, zdump_folder: Path) -> None:
    result = subprocess.run(
        ["zdump", "-v", str(zic_file)],
        check=True,
        capture_output=True,
        encoding='utf-8'
    )

    if not result.stdout:
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


def _dump_folder(zic_folder: Path, zic_base_folder: Path, zdump_folder: Path) -> None:
    if not zdump_folder.exists():
        zdump_folder.mkdir(parents=True, exist_ok=True)

    for path in zic_folder.iterdir():

        if path.is_dir():
            _dump_folder(path, zic_base_folder, zdump_folder / path.name)
        else:
            _dump_file(path, zic_base_folder, zdump_folder)


def dump_files(
        temp_folder: Path = Path("temp"),
        version: str = 'latest'
) -> None:
    zic_folder = (temp_folder / "zic" / version).resolve()
    zdump_folder = (temp_folder / "zdump" / version).resolve()

    _dump_folder(zic_folder, zic_folder, zdump_folder)
