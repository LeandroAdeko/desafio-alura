from flask import Blueprint, request, jsonify
from db.database import Database
from services.auth import token_required

shows_bp = Blueprint('shows', __name__, url_prefix='/shows')
db = Database()

@shows_bp.route('/', methods=['GET'])
@token_required
def get_shows():
    # Implement logic to retrieve all shows from the database
    query = "SELECT * FROM shows"
    result = db.execute_query(query)
    return jsonify(result)

@shows_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_show(id):
    # Implement logic to retrieve a specific show by ID from the database
    result = db.get_by_id("shows", id)
    return jsonify(result)

@shows_bp.route('/', methods=['POST'])
@token_required
def create_show():
    # Implement logic to create a new show in the database
    data = request.get_json()
    local = data['local']
    data_show = data['data']
    artista_id = data['artista_id']
    query = "INSERT INTO shows (local, data, artista_id) VALUES (%s, %s, %s)"
    params = (local, data_show, artista_id)
    db.execute_query(query, params)
    return jsonify({'message': 'Show created successfully'})

@shows_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_show(id):
    # Implement logic to update an existing show in the database
    data = request.get_json()
    local = data.get('local')
    data_show = data.get('data')
    artista_id = data.get('artista_id')
    update_data = {}
    if local:
        update_data['local'] = local
    if data_show:
        update_data['data'] = data_show
    if artista_id:
        update_data['artista_id'] = artista_id
    db.update_data("shows", id, update_data)
    return jsonify({'message': f'Show with id {id} updated successfully'})

@shows_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_show(id):
    # Implement logic to delete a specific show by ID from the database
    where_condition = f"id = {id}"
    db.delete_data("shows", where_condition)
    return jsonify({'message': f'Show with id {id} deleted successfully'})
