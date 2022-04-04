"""The main builder"""

import argparse
from ensurepip import version
import logging
from pathlib import Path
from typing import List

from .collector import collect
from .compiler import compile_files
from .downloader import download_data
from .dumper import dump_files
from .packager import make_package


def _parse_args(args):
    parser = argparse.ArgumentParser("Build tzdata")

    parser.add_argument(
        '-t', '--temp-dir',
        help='The temporary build folder',
        action='store',
        dest='temp_dir',
        default='temp'
    )

    parser.add_argument(
        '-i', '--iana-version',
        help='The version of the IANA tzdata',
        action='store',
        dest='version',
        default='latest'
    )

    parser.add_argument(
        '-u', '--tzdata_url',
        help='The URL to use to fetch the tzdata',
        action='store',
        dest='tzdata_url',
        default='ftp://ftp.iana.org/tz/tzdata-latest.tar.gz'
    )

    # parser.add_argument(
    #     '-i', '--input-file',
    #     help='Input filename',
    #     action='store',
    #     dest='input_filename'
    # )

    # parser.add_argument(
    #     '-o', '--output-path',
    #     help='Output folder or file',
    #     action='store',
    #     dest='output_path',
    #     default='.')
    # parser.add_argument(
    #     '-t', '--ticker',
    #     help='Add a ticker to record',
    #     action='append',
    #     dest='tickers',
    #     default=[])
    # parser.add_argument(
    #     '-s', '--silent',
    #     help='Suppress progress report',
    #     action='store_true',
    #     dest='is_silent',
    #     default=False)
    parser.add_argument(
        '-v', '--verbose',
        help='Verbose',
        action='store_true',
        dest='is_verbose',
        default=False
    )

    return parser.parse_args(args)


def build_tzdata(argv: List[str]):
    print("Building")
    args = _parse_args(argv[1:])
    if args.is_verbose:
        logging.basicConfig(level=logging.DEBUG)

    temp_folder = Path(args.temp_dir)

    download_data(
        temp_folder,
        args.tzdata_url,
        args.version
    )
    compile_files(
        temp_folder,
        args.version
    )
    dump_files(
        temp_folder,
        args.version
    )
    collect(
        temp_folder,
        args.version
    )
    make_package(
        temp_folder,
        args.version
    )
