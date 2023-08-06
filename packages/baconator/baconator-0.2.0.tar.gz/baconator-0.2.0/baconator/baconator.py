import random

from baconator.names import FIRST_NAMES, LAST_NAMES


def generate(delimiter: str = '-', token_len: int = 4, token: int = 0) -> str:
    """Generate a random name.

    The name is composed of 2-4 name parts, followed by a numeric token.
    The parts are seprated by a delimiter.

    Args:
        delimiter: The delimiter that separates the name parts.
            Could be arbitrary-length string.
        token_len: The length in digits of the numeric suffix.
            For example, 4  yields '0000' - '9999'.
            If token_len is 0, then no token is added.
        token: If greater than 0, then use this numeric token as a suffix
            instead of generating one. token_len is used in this case to
            left-pad the token.
            Otherwise, the token is generated randomly.

    Returns:
        A new random name.
    """
    items = [random.choice(FIRST_NAMES).replace('_', delimiter),
             random.choice(LAST_NAMES).replace('_', delimiter)]
    if token_len > 0:
        if token <= 0:
            token = random.randrange(10 ** token_len)
        items.append('{:0>{w}}'.format(token, w=token_len))
    return delimiter.join(items)
