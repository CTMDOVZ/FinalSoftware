import uuid

class Tarea:
    VALID_STATES = ["nuevo", "En Progreso", "Finalizada"]
    STATE_TRANSITIONS = {
        "nuevo": ["En Progreso"],
        "En Progreso": ["Finalizada", "nuevo"],
        "Finalizada": []
    }

    def __init__(self, id: str = None, title: str = "", description: str = "", status: str = "nuevo"):
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.status = status
        self.assignments = []    
        self.dependencies = []  

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "assignments": self.assignments,
            "dependencies": self.dependencies
        }

    def update_state(self, new_state: str):
        if new_state not in Tarea.VALID_STATES:
            raise ValueError(f"Estado inválido: {new_state}")
        allowed = Tarea.STATE_TRANSITIONS.get(self.status, [])
        if new_state not in allowed:
            raise ValueError(f"Transición de '{self.status}' a '{new_state}' no permitida")
        self.status = new_state
