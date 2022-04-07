"""Dump the compiled files"""

from pathlib import Path
import subprocess


def _dump_file(
        zic_file: Path,
        zic_base_folder: Path,
        zdump_folder: Path,
        is_verbose: bool
) -> None:
    if is_verbose:
        print(f"Dumping file: {zic_file}")

    args = ["zdump", "-v", str(zic_file)]

    if is_verbose:
        print(f"Executing: {' '.join(args)}")

    result = subprocess.run(
        args,
        check=True,
        capture_output=True,
        encoding='utf-8'
    )

    if not result.stdout:
        args = ["zdump", "UTC", str(zic_file)]

        if is_verbose:
            print(f"Executing: {' '.join(args)}")

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
        zdump_folder: Path,
        is_verbose: bool
) -> None:
    if is_verbose:
        print(f"Dumping folder: {zic_folder}")

    if not zdump_folder.exists():
        zdump_folder.mkdir(parents=True, exist_ok=True)

    for path in zic_folder.iterdir():

        if path.is_dir():
            _dump_folder(
                path,
                zic_base_folder,
                zdump_folder / path.name,
                is_verbose
            )
        else:
            _dump_file(
                path,
                zic_base_folder,
                zdump_folder,
                is_verbose
            )


def dump_files(
        temp_folder: Path,
        version: str,
        is_overwriting: bool,
        is_verbose: bool
) -> None:
    if is_verbose:
        print("Dumping files")

    zic_folder = (temp_folder / "zic" / version).resolve()
    zdump_folder = (temp_folder / "zdump" / version).resolve()

    if not zdump_folder.exists():
        zdump_folder.mkdir(parents=True, exist_ok=True)
    elif is_overwriting:
        subprocess.run(
            ['rm', '-r', str(zdump_folder)],
            check=True
        )
    else:
        return

    _dump_folder(zic_folder, zic_folder, zdump_folder, is_verbose)
