from flask import Blueprint, request, jsonify
from db.database import Database
from services.auth import token_required

artistas_bp = Blueprint('artistas', __name__, url_prefix='/artistas')
db = Database()

@artistas_bp.route('/', methods=['GET'])
@token_required
def get_artistas():
    # Implement logic to retrieve all artistas from the database
    query = "SELECT * FROM artistas"
    result = db.execute_query(query)
    return jsonify(result)

@artistas_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_artista(id):
    # Implement logic to retrieve a specific artista by ID from the database
    result = db.get_by_id("artistas", id)
    return jsonify(result)

@artistas_bp.route('/', methods=['POST'])
@token_required
def create_artista():
    # Implement logic to create a new artista in the database
    data = request.get_json()
    nome = data['nome']
    query = "INSERT INTO artistas (nome) VALUES (%s)"
    params = (nome,)
    db.execute_query(query, params)
    return jsonify({'message': 'Artista created successfully'})

@artistas_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_artista(id):
    # Implement logic to update an existing artista in the database
    data = request.get_json()
    nome = data.get('nome')
    update_data = {}
    if nome:
        update_data['nome'] = nome
    db.update_data("artistas", id, update_data)
    return jsonify({'message': f'Artista with id {id} updated successfully'})

@artistas_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_artista(id):
    # Implement logic to delete a specific artista by ID from the database
    where_condition = f"id = {id}"
    db.delete_data("artistas", where_condition)
    return jsonify({'message': f'Artista with id {id} deleted successfully'})
