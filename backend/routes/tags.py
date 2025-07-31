from flask import Blueprint, request, jsonify
from db.database import Database
from services.auth import token_required

tags_bp = Blueprint('tags', __name__, url_prefix='/tags')
db = Database()

@tags_bp.route('/', methods=['GET'])
@token_required
def get_tags():
    # Implement logic to retrieve all tags from the database
    query = "SELECT * FROM tags"
    result = db.execute_query(query)
    return jsonify(result)

@tags_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_tag(id):
    # Implement logic to retrieve a specific tag by ID from the database
    result = db.get_by_id("tags", id)
    return jsonify(result)

@tags_bp.route('/', methods=['POST'])
@token_required
def create_tag():
    # Implement logic to create a new tag in the database
    data = request.get_json()
    codigo = data['codigo']
    descricao = data['descricao']
    query = "INSERT INTO tags (codigo, descricao) VALUES (%s, %s)"
    params = (codigo, descricao)
    db.execute_query(query, params)
    return jsonify({'message': 'Tag created successfully'})

@tags_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_tag(id):
    # Implement logic to update an existing tag in the database
    data = request.get_json()
    codigo = data.get('codigo')
    descricao = data.get('descricao')
    update_data = {}
    if codigo:
        update_data['codigo'] = codigo
    if descricao:
        update_data['descricao'] = descricao
    db.update_data("tags", id, update_data)
    return jsonify({'message': f'Tag with id {id} updated successfully'})

@tags_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_tag(id):
    # Implement logic to delete a specific tag by ID from the database
    where_condition = f"id = {id}"
    db.delete_data("tags", where_condition)
    return jsonify({'message': f'Tag with id {id} deleted successfully'})
