from flask import Blueprint, request, jsonify
from db.database import Database
from services.auth import token_required

albuns_bp = Blueprint('albuns', __name__, url_prefix='/albuns')
db = Database()

@albuns_bp.route('/', methods=['GET'])
@token_required
def get_albuns():
    # Implement logic to retrieve all albuns from the database
    query = "SELECT * FROM albuns"
    result = db.execute_query(query)
    return jsonify(result)

@albuns_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_album(id):
    # Implement logic to retrieve a specific album by ID from the database
    result = db.get_by_id("albuns", id)
    return jsonify(result)

@albuns_bp.route('/', methods=['POST'])
@token_required
def create_album():
    # Implement logic to create a new album in the database
    data = request.get_json()
    nome = data['nome']
    artista_id = data['artista_id']
    query = "INSERT INTO albuns (nome, artista_id) VALUES (%s, %s)"
    params = (nome, artista_id)
    db.execute_query(query, params)
    return jsonify({'message': 'Album created successfully'})

@albuns_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_album(id):
    # Implement logic to update an existing album in the database
    data = request.get_json()
    nome = data.get('nome')
    artista_id = data.get('artista_id')
    update_data = {}
    if nome:
        update_data['nome'] = nome
    if artista_id:
        update_data['artista_id'] = artista_id
    db.update_data("albuns", id, update_data)
    return jsonify({'message': f'Album with id {id} updated successfully'})

@albuns_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_album(id):
    # Implement logic to delete a specific album by ID from the database
    where_condition = f"id = {id}"
    db.delete_data("albuns", where_condition)
    return jsonify({'message': f'Album with id {id} deleted successfully'})
