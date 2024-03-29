import re
import sys
from typing import Tuple

from son import SpiritOfNationsApp


def get_resolution() -> Tuple[int, int]:
    """
    Check if the resolution has been given as an argument.
    When it has, parse it, when not, get the default value.
    :return: resolution
    """

    # Default values
    width = 1920
    height = 1080

    for arg in sys.argv:
        match = re.search('^r=(\\d+)x(\\d+)$', arg)
        if match is not None:
            width = int(match.group(1))
            height = int(match.group(2))

    return width, height


if __name__ == "__main__":
    app = SpiritOfNationsApp(get_resolution())
    app.run()
