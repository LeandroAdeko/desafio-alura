from flask import Blueprint, request, jsonify
from db.database import Database
from services.auth import token_required

comentario_tags_bp = Blueprint('comentario_tags', __name__, url_prefix='/comentario_tags')
db = Database()

@comentario_tags_bp.route('/', methods=['GET'])
@token_required
def get_comentario_tags():
    # Implement logic to retrieve all comentario_tags from the database
    query = "SELECT * FROM comentario_tags"
    result = db.execute_query(query)
    return jsonify(result)

@comentario_tags_bp.route('/<uuid:comentario_id>/<int:tag_id>', methods=['GET'])
@token_required
def get_comentario_tag(comentario_id, tag_id):
    # Implement logic to retrieve a specific comentario_tag by ID from the database
    query = "SELECT * FROM comentario_tags WHERE comentario_id = %s AND tag_id = %s"
    result = db.fetch_one(query, (str(comentario_id), tag_id))
    return jsonify(result)

@comentario_tags_bp.route('/', methods=['POST'])
@token_required
def create_comentario_tag():
    # Implement logic to create a new comentario_tag in the database
    data = request.get_json()
    comentario_id = data['comentario_id']
    tag_id = data['tag_id']
    query = "INSERT INTO comentario_tags (comentario_id, tag_id) VALUES (%s, %s)"
    params = (comentario_id, tag_id)
    db.execute_query(query, params)
    return jsonify({'message': 'Comentario_tag created successfully'})

@comentario_tags_bp.route('/<uuid:comentario_id>/<int:tag_id>', methods=['DELETE'])
@token_required
def delete_comentario_tag(comentario_id, tag_id):
    # Implement logic to delete a specific comentario_tag by ID from the database
    query = "DELETE FROM comentario_tags WHERE comentario_id = %s AND tag_id = %s"
    params = (str(comentario_id), tag_id)
    db.execute_query(query, params)
    return jsonify({'message': f'Comentario_tag with comentario_id {comentario_id} and tag_id {tag_id} deleted successfully'})
