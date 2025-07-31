from flask import Blueprint, request, jsonify
from db.database import Database
from services.auth import token_required

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')
db = Database()

@usuarios_bp.route('/', methods=['GET'])
@token_required
def get_usuarios():
    # Implement logic to retrieve all usuarios from the database
    query = "SELECT * FROM usuarios"
    result = db.execute_query(query)
    return jsonify(result)

@usuarios_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_usuario(id):
    # Implement logic to retrieve a specific usuario by ID from the database
    result = db.get_by_id("usuarios", id)
    return jsonify(result)

@usuarios_bp.route('/', methods=['POST'])
@token_required
def create_usuario():
    # Implement logic to create a new usuario in the database
    data = request.get_json()
    nome = data['nome']
    email = data['email']
    senha_hash = data['senha_hash']
    is_admin = data.get('is_admin', False)
    query = "INSERT INTO usuarios (nome, email, senha_hash, is_admin) VALUES (%s, %s, %s, %s)"
    params = (nome, email, senha_hash, is_admin)
    db.execute_query(query, params)
    return jsonify({'message': 'Usuario created successfully'})

@usuarios_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_usuario(id):
    # Implement logic to update an existing usuario in the database
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha_hash = data.get('senha_hash')
    is_admin = data.get('is_admin')
    update_data = {}
    if nome:
        update_data['nome'] = nome
    if email:
        update_data['email'] = email
    if senha_hash:
        update_data['senha_hash'] = senha_hash
    if is_admin is not None:
        update_data['is_admin'] = is_admin
    db.update_data("usuarios", id, update_data)
    return jsonify({'message': f'Usuario with id {id} updated successfully'})

@usuarios_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_usuario(id):
    # Implement logic to delete a specific usuario by ID from the database
    where_condition = f"id = {id}"
    db.delete_data("usuarios", where_condition)
    return jsonify({'message': f'Usuario with id {id} deleted successfully'})
