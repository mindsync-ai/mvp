from flask_babel import gettext

class FieldErrors(Exception):
    def __init__(self, values):
        self.__values = values

    def to_dict(self):
        return self.__values


class FieldError(Exception):
    def __init__(self, name, status):
        self.name = name
        self.status = status


class EmptyFieldError(FieldError):
    def __init__(self, name):
        self.name = name
        self.status = gettext('Value could not be empty')


class BadFormatError(FieldError):
    def __init__(self, name):
        self.name = name
        self.status = gettext('Bad value format')


class ValueTooSmallError(FieldError):
    def __init__(self, name):
        self.name = name
        self.status = gettext('Value is too small')


class ValueTooBigError(FieldError):
    def __init__(self, name):
        self.name = name
        self.status = gettext('Value is too big')


class DuplicateValueError(FieldError):
    def __init__(self, name, status=None):
        self.name = name
        self.status = status if status else gettext('Duplicate value found')


class InvalidValueError(FieldError):
    def __init__(self, name, status=None):
        self.name = name
        self.status = status if status else gettext('Invalid value found')
