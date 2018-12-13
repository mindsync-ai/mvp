from app.data_tables.decorators import serialize_properties


class BazDataDescriptor(object):
    def __get__(self, obj, type):
        return self.__value

    def __set__(self, obj, value):
        self.__value = value


@serialize_properties
class Foo:
    @property
    def bar(self):
        return self.__value

    @bar.setter
    def bar(self, value):
        self.__value = value

    baz = BazDataDescriptor()


def test_to_dict_method():
    f = Foo()
    f.bar = 123
    f.baz = 'qwerty'
    assert f.to_dict() == dict(bar=123, baz='qwerty')
