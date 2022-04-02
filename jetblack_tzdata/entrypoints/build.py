"""Entrypoint for building the tzdata"""

import logging
import sys

from jetblack_tzdata import build_tzdata


def main():
    build_tzdata(sys.argv)
    logging.shutdown()


if __name__ == '__main__':
    main()
