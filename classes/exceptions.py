class MainException(Exception):
    def __init__(self, message, code=None):
        super(MainException, self).__init__(message)
        self.code = code
        self.message = message

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message


class AccessDeniedException(MainException):
    def __init__(self, message, code=403):
        # Call the base class constructor with the parameters it needs
        super(AccessDeniedException, self).__init__(message, code)


class UnSupportedFileException(MainException):
    def __init__(self, file_type, code=403):
        # Call the base class constructor with the parameters it needs
        super(UnSupportedFileException, self).__init__(
            "The type of the file is `%s` which is not correct as you defind in argument type" % file_type, code)


class UnKnownFileTypeException(MainException):
    def __init__(self, file_type, code=403):
        # Call the base class constructor with the parameters it needs
        super(UnKnownFileTypeException, self).__init__("%s Unknown file extension" % file_type, code)


class NotFoundException(MainException):
    def __init__(self, message, code=404):
        # Call the base class constructor with the parameters it needs
        super(NotFoundException, self).__init__(message, code)


class BashScriptException(MainException):
    def __init__(self, message, code=404):
        # Call the base class constructor with the parameters it needs
        super(BashScriptException, self).__init__(message, code)


class InvalidIPFSHashException(MainException):
    def __init__(self, message, code=301):
        # Call the base class constructor with the parameters it needs
        super(InvalidIPFSHashException, self).__init__('%s is invalid IPFS Hash' % message, code)
