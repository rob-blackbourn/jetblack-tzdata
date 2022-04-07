"""Collect dumped files"""

from datetime import datetime, timedelta
import json
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple

from jetblack_iso8601 import datetime_to_iso8601, timedelta_to_iso8601

from .types import TimezoneDelta


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
) -> Tuple[str, List[TimezoneDelta]]:
    if is_verbose:
        print(f"Collecting file: {zdump_file}")

    name: Optional[str] = None
    payload: List[TimezoneDelta] = []
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

    if name is None:
        raise ValueError('No name')

    return name, payload


def _collect_folder(
        zdump_folder: Path,
        results: Dict[str, List[TimezoneDelta]],
        is_verbose: bool,
) -> None:

    if is_verbose:
        print(f"Collecting files in folder: {zdump_folder}")

    for path in zdump_folder.iterdir():

        if path.is_dir():
            _collect_folder(path, results, is_verbose)
        else:
            name, values = _collect_file(path, is_verbose)
            if name in results:
                raise KeyError('Duplicate')
            results[name] = values


def collect(
        temp_folder: Path,
        version: str,
        is_verbose: bool
) -> None:
    if is_verbose:
        print("Collecting data")

    zdump_folder = temp_folder / "zdump" / version
    collect_folder = temp_folder / "collect" / version
    if not collect_folder.exists():
        collect_folder.mkdir(parents=True, exist_ok=True)

    results: Dict[str, List[TimezoneDelta]] = {}

    _collect_folder(zdump_folder, results, is_verbose)

    collect_file = collect_folder / 'tzdata.json'

    with open(collect_file, "wt", encoding='utf-8') as fp:
        json.dump(results, fp, indent=2, cls=JSONEncoderEx)
