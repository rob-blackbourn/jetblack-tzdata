"""Collect dumped files"""

from datetime import datetime, timedelta
import json
from pathlib import Path
import re
import subprocess
from typing import Dict, List, Optional, Tuple

from jetblack_iso8601 import datetime_to_iso8601, timedelta_to_iso8601

from .types import TimezoneDelta, MinTimezoneDelta


class JSONEncoderEx(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return datetime_to_iso8601(o)
        elif isinstance(o, timedelta):
            return timedelta_to_iso8601(o)
        else:
            return super(JSONEncoderEx, self).default(o)


# "MMM D HH:mm:ss YYYY"
DATE_FORMAT = "%b %d %H:%M:%S %Y"


def _collect_file(
    zdump_file: Path,
    is_verbose: bool
) -> Tuple[str, List[TimezoneDelta], List[MinTimezoneDelta]]:
    if is_verbose:
        print(f"Collecting file: {zdump_file}")

    name: Optional[str] = None
    payload: List[TimezoneDelta] = []
    min_payload: List[MinTimezoneDelta] = []
    with open(zdump_file, "rt", encoding="utf-8") as fp:
        for line in fp:
            parts = re.split(r'\s+', line.rstrip())
            if len(parts) < 13:
                raise ValueError('invalid line')

            if name is None:
                name = parts[0]
            elif name != parts[0]:
                raise ValueError('Name changed')

            utc_timestamp = datetime.strptime(
                ' '.join(parts[2:6]), DATE_FORMAT)
            local_timestamp = datetime.strptime(
                ' '.join(parts[9:13]), DATE_FORMAT)
            diff = (local_timestamp - utc_timestamp)

            abbr = parts[13]

            if parts[14].startswith('isdst'):
                is_dst = parts[14][-1] == '1'
            else:
                raise ValueError('isdst missing')

            payload.append(
                {
                    'utc': utc_timestamp,
                    'local': local_timestamp,
                    'offset': diff,
                    'abbr': abbr,
                    'isDst': is_dst
                }
            )

            min_payload.append(
                {
                    'u': int(utc_timestamp.timestamp() * 1000),
                    'o': int(diff.total_seconds() // 60),
                    'a': abbr,
                    'd': 1 if is_dst else 0
                }
            )

    if name is None:
        raise ValueError('No name')

    return name, payload, min_payload


def _collect_folder(
        zdump_folder: Path,
        results: Dict[str, List[TimezoneDelta]],
        min_results: Dict[str, List[MinTimezoneDelta]],
        is_verbose: bool,
) -> None:

    if is_verbose:
        print(f"Collecting files in folder: {zdump_folder}")

    for path in zdump_folder.iterdir():

        if path.is_dir():
            _collect_folder(path, results, min_results, is_verbose)
        else:
            name, values, min_values = _collect_file(path, is_verbose)
            if name in results:
                raise KeyError('Duplicate')
            results[name] = values
            min_results[name] = min_values


def _collect_version(
        temp_folder: Path,
        version: str,
        is_overwriting: bool,
        is_verbose: bool
) -> None:
    zdump_folder = temp_folder / "zdump" / version

    collect_folder = temp_folder / "collect" / version
    if collect_folder.exists():
        if is_overwriting:
            if is_verbose:
                print(f"Clearing folder: {collect_folder}")
            subprocess.run(
                ['rm', '-r', str(collect_folder)],
                check=True
            )
        else:
            return
    collect_folder.mkdir(parents=True, exist_ok=True)

    results: Dict[str, List[TimezoneDelta]] = {}
    min_results: Dict[str, List[MinTimezoneDelta]] = {}

    _collect_folder(zdump_folder, results, min_results, is_verbose)

    collect_file = collect_folder / 'tzdata.json'
    min_collect_file = collect_folder / 'tzdata.min.json'

    with open(collect_file, "wt", encoding='utf-8') as fp:
        json.dump(results, fp, indent=2, cls=JSONEncoderEx)

    with open(min_collect_file, "wt", encoding='utf-8') as fp:
        json.dump(min_results, fp)


def collect(
        temp_folder: Path,
        versions: List[str],
        is_overwriting: bool,
        is_verbose: bool
) -> None:
    if is_verbose:
        print("Collecting data")

    for version in versions:
        _collect_version(temp_folder, version, is_overwriting, is_verbose)
