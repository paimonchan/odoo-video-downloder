import contextlib

class Field:
    _type       = False
    _value      = False
    _name       = False
    _context    = dict()

    def __init__(self, type, default_value = False):
        self._type = type
        self._value = default_value

    def __set_name__(self, record, name):
        self._name = name
        record.add_fields(record, self)

    def __get__(self, record, owner):
        if len(record._entries) == 0 or not record._empty:
            return record.get_field_value(self._name)
        if len(record._entries) == 1:
            return record._entries[0].get_field_value(self._name)
        raise ValueError('Expected Singleton')
    
    def __set__(self, record, value):
        if len(record._entries) == 0 or not record._empty:
            return record.write({self._name: value})
        if len(record._entries) == 1:
            return record._entries[0].write({self._name: value})
        raise ValueError('Expected Singleton')

    @contextlib.contextmanager
    def with_context(self, context):
        """
        used context to access original property from object data.
        because when access self._entries[0].attribute, the attribute is owned by self, not the _entries[0]
        """
        orig_context = self._context
        try:
            self._context = context
            yield
        finally:
            self._context = orig_context