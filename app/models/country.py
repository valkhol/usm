class Country:
    _id: str
    _name: str

    def __init__(self, *, id: str, name: str):
        if not id:
            raise ValueError('Country id can not be empty!')

        if not name:
            raise ValueError('Country name can not be empty!')

        self._id = id.lower()
        self._name = name

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self):
        return f'Country: {self._id} - {self._name}'
