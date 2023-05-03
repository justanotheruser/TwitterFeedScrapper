import logging
import re
from typing import Union

logger = logging.getLogger('TwitterFeedScrapper')


class ScrapingUtilities:
    """
    This class contains all utility methods that help cleaning or extracting
    data from raw data.

    @staticmethod
    def method_name(parameters)
    """

    @staticmethod
    def parse_name(string) -> Union[str, None]:
        """Extract name from the given string.
           Example:
           Input: jack(@jack)
           Output: jack
        """
        try:
            return string.split("(")[0].strip()
        except Exception as ex:
            logger.exception("Error at parse_name : {}".format(ex))

    @staticmethod
    def extract_digits(string) -> Union[int, None]:
        """Extracts first digits from the string.

        Args:
          string (str): string containing digits.

        Returns:
          int: digit that was extracted from the passed string
        """
        try:
            return int(re.search(r'\d+', string).group(0))
        except Exception as ex:
            logger.exception("Error at extract_digits : {}".format(ex))

    @staticmethod
    def set_value_or_none(value, string) -> Union[str, None]:
        return string + str(value) + " " if value is not None else None
