def enum(**enums):

    """Provide the capabilities of an enum from other languages.

    Keyword arguments:
    enums --- name/value pairs of arguments for enum names/values

    """

    return type('Enum', (), enums)
