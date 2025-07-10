class Usuario:
    def __init__(self, id: str, alias: str, name: str):
        self.id = id
        self.alias = alias
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "alias": self.alias,
            "name": self.name
        }
