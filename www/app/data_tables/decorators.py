import inspect


def string_to_bool(func):
   def wrapper(self, value):
       value = True if value == 'true' else value
       value = False if value == 'false' else value
       func(self, value)
   return wrapper


def serialize_properties(cls):
    prop_names = [name for name, _ in inspect.getmembers(cls, inspect.isdatadescriptor) if not name.startswith('_')]

    def to_dict(self):
        return {prop_name: getattr(self, prop_name) for prop_name in prop_names}

    cls.to_dict = to_dict

    return cls
