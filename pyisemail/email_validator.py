class EmailValidator(object):

    def is_email(self, address, diagnose=False):
        raise NotImplementedError()

    is_valid = is_email
