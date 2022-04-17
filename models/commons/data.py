class Data:    
    __slots__           = ['_dict_entries', '_entries', 'entry']

    _fields             = dict()
    _fields_description = dict()
    _empty              = False

    id                  = False

    def __post_init__(self):
        self._entries = [self]
        self.entry = self
        self.id = id(self)
        self._dict_entries = {self.id: self}

    def __repr__(self):
        return '%s%s' % (self.__class__.__name__, (self.id))
    
    def __str__(self):
        ids = [e.id for e in self._entries]
        return '%s%s' % (self.__class__.__name__, tuple(ids))

    def __getitem__(self, key):
        # if key is string, then we redirect it into field value
        if isinstance(key,str):
            return self._fields_description[key]
        return self._entries[key]
    
    def __setitem__(self, key, value):
        if isinstance(key,str):
            self._fields_description[key] = value
        raise ValueError(f'cannot direct set classdata')

    def __or__(self, others):
        entries = list(self._entries)
        for other in others:
            if isinstance(other, Data) and self.__class__ == other.__class__:
                entries.extend(other._entries)
            else:
                raise TypeError(f'cannot union different class data')
        self._dict_entries = {e.id: e for e in entries}
        self._entries = entries
        return self
    
    def __iter__(self):
        for entry in self._entries:
            yield entry
    
    def __len__(self):
        return len(self._entries)

    def add_fields(self, field):
        self._fields_description[field._name] = field
    
    def get_field_value(self, field_name):
        return self._fields[field_name]
    
    @classmethod
    def empty(cls):
        empty_object = cls()
        empty_object._dict_entries = dict()
        empty_object._entries = []
        empty_object._empty = True
        return empty_object

    @classmethod
    def create(cls, vals):
        new_object = cls()
        new_object._fields = dict()
        for field_name, field in new_object._fields_description.items():
            new_object._fields[field_name] = vals.get(field_name) or field._value
        return new_object

    def write(self, vals):
        for key, value in vals.items():
            for record in self._entries:
                record._fields[key] = value
        return True