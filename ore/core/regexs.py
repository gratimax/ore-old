# Regex that includes a few other characters other than word characters
EXTENDED_CHAR_REGEX = r'[a-zA-Z0-9._][a-zA-Z0-9.\-_]*'

# A regex that validates only a name that contains the extended characters
EXTENDED_NAME_REGEX = r'^' + EXTENDED_CHAR_REGEX + r'$'

# A regex that permits spaces along with the extended characters, but not
# at the ends
TRIM_NAME_REGEX = r'^' + EXTENDED_CHAR_REGEX + \
    r'([\w.\-_ ]*' + EXTENDED_CHAR_REGEX + r')?$'


EXTENDED_URL_REGEX = EXTENDED_NAME_REGEX[1:-1]
TRIM_URL_REGEX = TRIM_NAME_REGEX[1:-1]
