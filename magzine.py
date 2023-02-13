#!/usr/bin/env python
#
# written by: Muhammad Zahid  Feb.2022
# muhammadzahid11@gmail.com


import argparse
import logging
import os
import sys
from typing import list, tuple


__VERSION__ = "0.1"
__appname__ = "CalculateMagzineArticleOverlapping"


try:
    # create a custom logger
    logger = logging.getLogger(__name__)

    # create log handler
    # By default it uses the sys.stderr (error stream handler of terminal)
    CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
    # setting the format of logs
    FORMATTER = logging.Formatter('%(message)s')
    CONSOLE_HANDLER.setFormatter(FORMATTER)

    # Add handler to logger
    logger.addHandler(CONSOLE_HANDLER)
except Exception as e:
    logging.error('[E] Custom logger Configuration causes an error: '
                  '{}'.format(e), exc_info=True)
    sys.exit(1)


def get_args():
    """Command Line arguements are set in ftn.

    The ftn returns the specified arguments
    """
    try:
        args_parser = argparse.ArgumentParser(
            description="Debug or run code in normal mode.",
            prog="{}".format(os.path.basename(__file__)),
            allow_abbrev=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        args_parser.add_argument(
            "--version", "-V",
            dest="version",
            version="%(prog)s {}".format(__VERSION__),
            action="version",
            help="Show version of script."
        )
        args_parser.add_argument(
            "--debug", "-d", action="store_true", help="show debug output."
        )

        return args_parser.parse_args()
    except Exception as excep1:
        logger.error(
            "[E] while getting the arguments in arg_parse ftn. Error: "
            "{}".format(excep1)
        )
        sys.exit(1)


def is_article_valid(article: str) -> bool:
    """Check article format is valid or not. Return True for valid article
    otherwise false.

    e.g: 10-15 is article containing  pages from 10 to 15. Check whether
    hyphen '-' exist between ranges then check page range contains only
    integers.
    """
    pass


def check_overlapping_articles(article_1: str, article_2: str) -> str:
    """Check which pages of 2 articles are overlapping and return those pages.

    article_1: First article contains the page range from magzine. e.g: 10-15
    article_2: 2nd article contains the page range from magzine. e.g: 12-15
    return overlapping articles i.e 12-15
    """
    pass


def seperate_valid_invalid_articles_from_line(
        file_line: str) -> tuple[str, str]:
    """Seperate valid and invalid articles from each line.

    file_line: it is a line string
    Returns the tuple containing two string elements.
    Two articles are seperated by comma ';'
    i.e ("<valid_article_1, valid_article_2>",
    <invalid_article_1, invalid_article_2>)
    """
    pass


def read_articles_from_file(file_name: str) -> list[tuple[str, str]]:
    """Read articles from file line by line and seperate valid and invalid
    articles into two files w.r.t to each line.

    """
    pass


def main():
    """Calls the relative ftn"""
    args = get_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


if __name__ == "__main__":
    main()
