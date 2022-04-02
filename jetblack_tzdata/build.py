"""The main builder"""

import argparse
import logging
from typing import List

from .collector import collect
from .compiler import compile_files
from .downloader import download_data
from .dumper import dump_files
from .packager import make_package


def _parse_args(args):
    parser = argparse.ArgumentParser("Build tzdata")

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

    # download_data()
    # compile_files()
    # dump_files()
    # collect()
    make_package()
