#!/usr/bin/env python
#
# written by: Muhammad Zahid  Feb.2022
# muhammadzahid11@gmail.com


import argparse
import logging
import os
import sys
from typing import List, Tuple, Dict, Union


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


def get_args() -> Dict[str, Union[bool, str]]:
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
        # 'Action' is positional argument.
        args_parser.add_argument(
            "--file",
            "-f",
            type=str,
            required=True,
            dest="file",
            metavar="file_name",
            help='Specify the file name including the path.'
        )

        return args_parser.parse_args()

    except Exception as excep1:
        logger.error(
            "[E] while getting the arguments in arg_parse ftn. Error: "
            "{}".format(excep1)
        )
        sys.exit(1)


def is_str_emp(str2):
    """Check whether string is empty or not, return True if empty.

    otherwise return False.
    """
    try:
        str1 = str(str2)
        logger.debug("'{}' string converted into '{}'".format(str2, str1))
        if (str1 == "None") or len(str1) == 0:
            logger.debug("'{}' was empty".format(str1))
            return True

        logger.debug("'{}' string is not empty.".format(str1))
        return False
    except (ValueError, Exception) as ex:
        logger.debug("[D] {} exception occurs.while converting "
                     "into string. Exception: {}".format(str2, ex))


def is_article_valid(article: str) -> tuple[bool, int, int]:
    """Check article format is valid or not. Return tuple.

    Return tuple (<True_for_valid_article otherwise>,
    start_page_article, end_page_article)
    e.g: 10-15 is article containing  pages from 10 to 15. Check whether
    hyphen '-' exist between ranges then check page range contains only
    integers.
    """
    start_page = end_page = None
    if not is_str_emp(article) and '-' in article:
        start_page, end_page = article.split('-')
    try:
        start_page = int(start_page)
        end_page = int(end_page)
        if (isinstance(start_page, int) and isinstance(end_page, int)
                and end_page >= start_page):
            return (True, start_page, end_page)
        else:
            logger.debug("[D] Article '{}' contains invalid start or "
                         "end page numbers.".format(article))
            return (False, start_page, end_page)

    except (ValueError, Exception) as ex:
        logger.debug("[D] {} Article start or end page is not a "
                     "number. Exception: {}".format(article, ex))


def check_overlapping_articles(article_1: str,
                               article_2: str) -> Tuple[bool, str]:
    """Check which pages of 2 articles are overlapping and return those pages.

    article_1: First article contains the page range from magzine. e.g: 10-15
    article_2: 2nd article contains the page range from magzine. e.g: 12-15
    return overlapping articles i.e 12-15
    """
    try:
        art_1_is_valid, art_1_start_pg, art_1_end_pg = is_article_valid(
            article_1)
        art_2_is_valid, art_2_start_pg, art_2_end_pg = is_article_valid(
            article_2)
        if art_1_is_valid and art_2_is_valid:
            art_1_pg_gen = range(art_1_start_pg, art_1_end_pg+1)
            art_2_pg_gen = range(art_2_start_pg, art_2_end_pg+1)
            overlap_pgs = list(set(art_1_pg_gen) & set(art_2_pg_gen))

            if len(overlap_pgs) != 0:
                overlap_art_strt_pg = min(overlap_pgs)
                overlap_art_end_pg = max(overlap_pgs)
                output = ("Overlapping pages b/W '{}' & '{}' : '{}-{}'"
                          "".format(article_1, article_2,
                                    overlap_art_strt_pg, overlap_art_end_pg))
                logger.debug("[D] {}".format(output))
                return (True,
                        "{}-{}".format(
                            overlap_art_strt_pg, overlap_art_end_pg)
                        )
            else:
                output = ("There are no Overlapping pages b/W '{}' & '{}'"
                          "".format(article_1, article_2))
                logger.debug("[D] {}".format(output))
                return (False, None)
    except Exception as ex:
        logger.error("[E] During checking of overlapping pages b/W '{}' and "
                     "'{}' error occured. Exception: {}".format(
                         article_1, article_2, ex))


def seperate_valid_invalid_articles_from_line(
        file_line: str) -> tuple[str, str]:
    """Seperate valid and invalid articles from each line.

    file_line: it is a line string
    Returns the tuple containing two string elements.
    Two articles are seperated by comma ','
    i.e ("<valid_article_1, valid_article_2>",
    <invalid_article_1, invalid_article_2>)
    """
    try:
        split_art_ls = file_line.split(',')
        valid_art_ls = ""
        invalid_art_ls = ""
        for art in split_art_ls:
            art = art.strip()
            is_art_valid, start_pg, end_pg = is_article_valid(art)
            if is_art_valid:
                valid_art_ls = "{},{}".format(valid_art_ls, art)
            else:
                invalid_art_ls = "{},{}".format(invalid_art_ls, art)

        valid_art_ls = valid_art_ls[1:]
        invalid_art_ls = invalid_art_ls[1:]

        return (valid_art_ls, invalid_art_ls)
    except Exception as ex:
        logger.error("[E] Error occured while seperating valid & invalid "
                     "articles. Error: {}".format(ex))
        sys.exit(1)


def write_to_file(file: str, line: str) -> None:
    """Append content to specified file.
    """
    try:
        with open(file, 'a') as wf:
            wf.write("{}\n".format(line))
    except OSError as oe:
        logger.error("[E] OS error occured trying to open '{}'. Error: "
                     "{}".format(file, oe))
        sys.exit(1)
    except Exception as ex:
        logger.error("[E] Unexpected Error occured while opening '{}'"
                     "Error: {}".format(file, ex))
        sys.exit(1)


def read_articles_from_file(file_name: str) -> None:
    """Read articles from file line by line and seperate valid and invalid
    articles into two files w.r.t to each line.l

    """
    valid_art_file = "./valid_art.txt"
    invalid_art_file = "./invalid_art.txt"
    try:
        if os.path.isfile(valid_art_file):
            os.remove(valid_art_file)
        if os.path.isfile(invalid_art_file):
            os.remove(invalid_art_file)
    except Exception as ex:
        logger.error("[E] Error occured while removing '{}' or '{}'. "
                     "Please remove these files from current directory. "
                     "Error: {}".format(valid_art_file, invalid_art_file, ex))
        sys.exit(1)

    try:
        with open("{}".format(file_name), 'r') as file:
            for line in file:
                line = line.strip()

                if line != '':
                    valid_art, invalid_art = seperate_valid_invalid_articles_from_line(
                        line)
                elif line == '':
                    valid_art = invalid_art = ""
                else:
                    valid_art = ''
                    invalid_art = line

                write_to_file(valid_art_file, valid_art)
                write_to_file(invalid_art_file, invalid_art)

    except FileNotFoundError as fe:
        logger.error("[E] File not found '{}'. Error: {}".format(
            file_name, fe))
        sys.exit(1)
    except OSError as oe:
        logger.error("[E] OS error occured trying to open '{}'. Error: "
                     "{}".format(file_name, oe))
        sys.exit(1)
    except Exception as ex:
        logger.error("[E] Unexpected Error occured while opening '{}'"
                     "Error: {}".format(file_name, ex))
        sys.exit(1)


def main():
    """Calls the relative ftn"""
    args = get_args()
    file_name = args.file
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    read_articles_from_file(file_name)

    output_file = './output.txt'
    try:
        if os.path.isfile(output_file):
            os.remove(output_file)
    except Exception as ex:
        logger.error("[E] unexpected error while removing '{}' file to "
                     "save output. Error: {}".format(output_file, ex))

    try:
        valid_art = "./valid_art.txt"
        is_overlap_exist = overlap_pgs = None
        with open(valid_art, 'r') as file:
            for line in file:
                split_art = line.strip().split(',')
            for art_1 in split_art:
                for art_2 in split_art:
                    is_overlap_exist, overlap_pgs = check_overlapping_articles(
                       art_1, art_2)
                    if is_overlap_exist:
                        output = ("Overlapping pages b/W '{}' and '{}' : "
                                  "'{}'").format(
                                      art_1, art_2, overlap_pgs)
                        logger.info("{}".format(output))
                        write_to_file(output_file, output)
    except OSError as oe:
        logger.error("[E] OS error occured trying to open '{}'. Error: "
                     "{}".format(file, oe))
        sys.exit(1)
    except Exception as ex:
        logger.error("[E] Unexpected Error occured while opening '{}'"
                     "Error: {}".format(file, ex))


if __name__ == "__main__":
    main()
