# bw-save-game - BioWare save game tools
# Copyright (C) 2024 Tim Niederhausen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Website: https://github.com/timniederhausen/bw_save_game
# -*- coding: utf-8 -*-
import argparse
import json
import logging
import sys

from bw_save_game import __version__
from bw_save_game.container import read_save_from_reader, write_save_to_writer
from bw_save_game.db_object import from_raw_dict, to_raw_dict
from bw_save_game.db_object_codec import dumps, loads

__author__ = "Tim Niederhausen"
__copyright__ = "Tim Niederhausen"
__license__ = "GPL-3.0-only"

_logger = logging.getLogger(__name__)


# ---- Python API ----


def csav_to_json(filename, output):
    with open(filename, "rb") as f:
        m, d = read_save_from_reader(f)

    m = loads(m)
    d = loads(d)

    if output == "-":
        json.dump(dict(meta=m, data=d), sys.stdout, indent=2, default=to_raw_dict)
    else:
        with open(output, "w", encoding="utf-8") as f:
            json.dump(dict(meta=m, data=d), f, indent=2, default=to_raw_dict)


def json_to_csav(filename, output):
    with open(filename, "r", encoding="utf-8") as f:
        doc = json.load(f, object_hook=from_raw_dict)

    m = doc["meta"]
    d = doc["data"]

    # re-encode our object tree into a DbObject byte string
    m = dumps(m)
    d = dumps(d)

    if output == "-":
        # TODO: warn if not a binary stream?
        write_save_to_writer(sys.stdout, m, d)
    else:
        with open(output, "wb") as f:
            write_save_to_writer(f, m, d)


# ---- CLI ----


def register_common_args(parser):
    """Parse command line parameters

    Args:
      parser (argparse.ArgumentParser): parser object to add arguments to.

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser.add_argument(
        "--version",
        action="version",
        version=f"bw_save_game {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )


def parse_from_bin_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Dump a JSON representation of a BioWare Frostbite save game")
    register_common_args(parser)
    parser.add_argument("input", help="Path to the input save game .csav")
    parser.add_argument("output", nargs="?", default="-", help="Path to the output .json document")
    return parser.parse_args(args)


def parse_from_json_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Re-encode a JSON representation to a BioWare Frostbite save game")
    register_common_args(parser)
    parser.add_argument("input", help="Path to the input save game .json")
    parser.add_argument("output", nargs="?", default="-", help="Path to the output save game .csav")
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def run_to_json():
    args = parse_from_bin_args(sys.argv[1:])
    setup_logging(args.loglevel)
    csav_to_json(args.input, args.output)


def run_to_bin():
    args = parse_from_json_args(sys.argv[1:])
    setup_logging(args.loglevel)
    json_to_csav(args.input, args.output)


if __name__ == "__main__":
    # e.g.     python -m bw_save_game.convert test.csav
    run_to_json()
