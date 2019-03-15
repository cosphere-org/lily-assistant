
import re


def remove_white_chars(s):
    return re.sub('\s+', '', s)
