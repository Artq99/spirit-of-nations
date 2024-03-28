def check_none(obj: object, arg_name: str) -> None:
    """
    Check if the given object is None and throw an error if it is.

    :param obj: object to check
    :param arg_name: name of the argument
    """
    if obj is None:
        raise TypeError("Argument '{}' cannot be None.".format(arg_name))


def check_str_empty(obj: str, arg_name: str) -> None:
    """
    Check if the given string is None or empty and throw an error if it is.

    :param obj: string to check
    :param arg_name: name of the argument
    """
    check_none(obj, arg_name)
    if len(obj) == 0:
        raise ValueError("Argument '{}' cannot be an empty string.".format(arg_name))
