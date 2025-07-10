class Asignacion:
    def __init__(self, task_id: str, user_alias: str, rol: str):
        self.task_id = task_id
        self.user_alias = user_alias
        self.rol = rol

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "usuario": self.user_alias,
            "rol": self.rol
        }
