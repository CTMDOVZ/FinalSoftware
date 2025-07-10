import json
import os
import uuid
from src.models.usuario import Usuario
from src.models.tarea import Tarea
from src.models.asignacion import Asignacion

class DataHandler:
    def __init__(self, filepath: str = None):
        base = os.path.dirname(__file__)
        default = os.path.abspath(os.path.join(base, '..', 'data.json'))
        self.filepath = filepath or default
        if not os.path.exists(self.filepath):
            self._init_file()
        self._load()

    def _init_file(self):
        data = {"users": [], "tasks": []}
        with open(self.filepath, 'w') as f:
            json.dump(data, f)

    def _load(self):
        with open(self.filepath, 'r') as f:
            data = json.load(f)
        self.users = data.get("users", [])
        self.tasks = data.get("tasks", [])

    def _save(self):
        data = {"users": self.users, "tasks": self.tasks}
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def create_user(self, alias: str, name: str):
        if any(u['alias'] == alias for u in self.users):
            raise ValueError("Alias ya existe")
        user = Usuario(str(uuid.uuid4()), alias, name)
        self.users.append(user.to_dict())
        self._save()
        return user.to_dict()

    def get_user(self, alias: str):
        user = next((u for u in self.users if u['alias'] == alias), None)
        if not user:
            raise KeyError("Usuario no encontrado")
        assigned = [t for t in self.tasks if any(a['usuario']==alias for a in t.get('assignments', []))]
        u = user.copy()
        u['tasks'] = assigned
        return u

    def get_task(self, task_id: str):
        task = next((t for t in self.tasks if t['id'] == task_id), None)
        if not task:
            raise KeyError("Tarea no encontrada")
        return task

    def create_task(self, title: str, description: str, usuario_alias: str, rol: str):
        if not any(u['alias']==usuario_alias for u in self.users):
            raise KeyError("Usuario no encontrado")
        tarea = Tarea(str(uuid.uuid4()), title, description)
        asign = Asignacion(tarea.id, usuario_alias, rol)
        tarea.assignments.append(asign.to_dict())
        self.tasks.append(tarea.to_dict())
        self._save()
        return tarea.to_dict()

    def update_task_state(self, task_id: str, new_state: str):
        task = self.get_task(task_id)
        if new_state == "Finalizada":
            for dep in task.get('dependencies', []):
                d = self.get_task(dep)
                if d['status'] != "Finalizada":
                    raise ValueError("Dependencia pendiente")
        tarea = Tarea(task['id'], task['title'], task['description'], task['status'])
        tarea.assignments = task.get('assignments', [])
        tarea.dependencies = task.get('dependencies', [])
        tarea.update_state(new_state)
        task['status'] = tarea.status
        self._save()
        return task

    def assign_user(self, task_id: str, usuario_alias: str, rol: str):
        task = self.get_task(task_id)
        if not any(u['alias']==usuario_alias for u in self.users):
            raise KeyError("Usuario no encontrado")
        if any(a['usuario']==usuario_alias for a in task['assignments']):
            raise ValueError("Usuario ya asignado")
        task['assignments'].append({"usuario": usuario_alias, "rol": rol})
        self._save()
        return task

    def remove_user(self, task_id: str, usuario_alias: str):
        task = self.get_task(task_id)
        if not any(a['usuario']==usuario_alias for a in task['assignments']):
            raise ValueError("Usuario no asignado")
        task['assignments'] = [a for a in task['assignments'] if a['usuario'] != usuario_alias]
        if not task['assignments']:
            raise ValueError("La tarea debe tener al menos un usuario asignado")
        self._save()
        return task

    def add_dependency(self, task_id: str, dependencytaskid: str):
        task = self.get_task(task_id)
        if not any(t['id']==dependencytaskid for t in self.tasks):
            raise KeyError("Tarea dependencia no encontrada")
        if dependencytaskid in task.get('dependencies', []):
            raise ValueError("Dependencia ya existe")
        task.setdefault('dependencies', []).append(dependencytaskid)
        self._save()
        return task

    def remove_dependency(self, task_id: str, dependencytaskid: str):
        task = self.get_task(task_id)
        if dependencytaskid not in task.get('dependencies', []):
            raise ValueError("Dependencia no existe")
        task['dependencies'] = [d for d in task['dependencies'] if d != dependencytaskid]
        self._save()
        return task
