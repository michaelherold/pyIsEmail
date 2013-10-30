class EmailValidator(object):

    """Abstract email validator to subclass from.

    You should not instantiate an EmailValidator, as it merely provides the
    interface for is_email, not an implementation.

    """

    def is_email(self, address, diagnose=False):
        """Interface for is_email method.

        Keyword arguments:
        address    -- address to check.
        diagnose   -- flag to report a diagnose or just True/False
        """
        raise NotImplementedError()

    is_valid = is_email
