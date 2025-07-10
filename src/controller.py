from flask import Flask, request, jsonify, abort
from src.data_handler import DataHandler

app = Flask(__name__)
# Si más adelante cambias a SQLAlchemy, aquí iría la configuración de la base de datos.
handler = DataHandler()

@app.route('/usuarios', methods=['GET'])
def get_usuario():
    alias = request.args.get('alias')
    if not alias:
        abort(422)
    try:
        user = handler.get_user(alias)
        return jsonify(user), 200
    except KeyError:
        abort(404)

@app.route('/usuarios', methods=['POST'])
def post_usuario():
    data = request.get_json() or {}
    alias = data.get('contacto')
    name = data.get('nombre')
    if not alias or not name:
        abort(422)
    try:
        user = handler.create_user(alias, name)
        return jsonify(user), 201
    except ValueError:
        abort(422)

@app.route('/tasks', methods=['POST'])
def post_task():
    data = request.get_json() or {}
    title = data.get('nombre')
    description = data.get('descripcion')
    usuario = data.get('usuario')
    rol = data.get('rol')
    if not all([title, description, usuario, rol]):
        abort(422)
    try:
        task = handler.create_task(title, description, usuario, rol)
        return jsonify({"id": task['id']}), 201
    except KeyError:
        abort(404)

@app.route('/tasks/<task_id>', methods=['POST'])
def update_task(task_id):
    data = request.get_json() or {}
    new_state = data.get('estado')
    if not new_state:
        abort(422)
    try:
        task = handler.update_task_state(task_id, new_state)
        return jsonify(task), 200
    except KeyError:
        abort(404)
    except ValueError:
        abort(422)

@app.route('/tasks/<task_id>/users', methods=['POST'])
def manage_task_user(task_id):
    data = request.get_json() or {}
    usuario = data.get('usuario')
    rol = data.get('rol')
    accion = data.get('accion')
    if not all([usuario, rol, accion]):
        abort(422)
    try:
        if accion == 'adicionar':
            task = handler.assign_user(task_id, usuario, rol)
        elif accion == 'remover':
            task = handler.remove_user(task_id, usuario)
        else:
            abort(422)
        return jsonify(task), 200
    except KeyError:
        abort(404)
    except ValueError:
        abort(422)

@app.route('/tasks/<task_id>/dependencies', methods=['POST'])
def manage_dependency(task_id):
    data = request.get_json() or {}
    dep_id = data.get('dependencytaskid')
    accion = data.get('accion')
    if not dep_id or not accion:
        abort(422)
    try:
        if accion == 'adicionar':
            task = handler.add_dependency(task_id, dep_id)
        elif accion == 'remover':
            task = handler.remove_dependency(task_id, dep_id)
        else:
            abort(422)
        return jsonify(task), 200
    except KeyError:
        abort(404)
    except ValueError:
        abort(422)

if __name__ == '__main__':
    app.run(debug=True)
