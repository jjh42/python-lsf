#!/usr/bin/env python
from __future__ import print_function, division

from hostlist import Hostlist
from utility import color

import sys
import re
import argparse


def ehosts(args, bhostsargs):
    r = ""
    select = []
    # get selects from -R
    if args.R:
        match = re.search("select\[(.*?)\]", args.R)
        if match:
            select += match.groups()
        r = re.sub("select\[.*\]", "", args.R)

    # add selects
    if args.aices:
        select += ("aices",)
    if args.model:
        select += ("model==" + args.model,)

    if len(select):
        select = " && ".join("(" + s + ")" for s in select)
        r = (r + " select[" + select + "]").strip()

    if len(r):
        bhostsargs += ["-R", r]

    if sys.stdout.isatty():
        print("Reading host list from LSF ...", end="\r")
    sys.stdout.flush()
    hostlist = Hostlist(bhostsargs)
    if sys.stdout.isatty():
        print("                              ", end="\r")
    hostlist.sort()
    hostlist.display(wide=args.wide, parallel=not args.nopar)


def main():
    global args
    parser = argparse.ArgumentParser(
        description="More comprehensive version of bhosts.")
    parser.add_argument(
        "-w", "--wide",
        help="don't shorten strings",
        action="store_true",
    )
    parser.add_argument(
        "-aices",
        help="short for -R select[aices]",
        action="store_true",
    )
    parser.add_argument(
        "-m", "--model",
        help="short for -R select[model==MODEL]",
    )
    parser.add_argument(
        "--nopar",
        help="faster response, longer runtime",
        action="store_true",
    )
    parser.add_argument(
        "-d", "--debug",
        help="show debug info on errors",
        action="store_true",
    )
    parser.add_argument(
        "-R",
        help=argparse.SUPPRESS
    )
    parser.add_argument_group("further arguments",
                              description="are passed to bhosts")

    args, bhostsargs = parser.parse_known_args()

    if args.debug:
        ehosts(args, bhostsargs)
    else:
        try:
            ehosts(args, bhostsargs)
        except KeyboardInterrupt:
            pass
        except Exception:
            print(color("ERROR -- probably a job status changed while " +
                        sys.argv[0] + " processed it", "r"), file=sys.stderr)


if __name__ == "__main__":
    main()
