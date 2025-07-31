from flask import Blueprint, request, jsonify
from db.database import get_db
from services.auth import token_required
from models import Show

shows_bp = Blueprint('shows', __name__, url_prefix='/shows')
db = get_db()

@shows_bp.route('/', methods=['GET'])
@token_required
def get_shows():
    # Implement logic to retrieve all shows from the database
    shows = db.query(Show).all()
    return jsonify([show.to_dict() for show in shows])

@shows_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_show(id):
    # Implement logic to retrieve a specific show by ID from the database
    show = db.query(Show).filter(Show.id == id).first()
    if show:
        return jsonify(show.to_dict())
    return jsonify({'message': 'Show not found'})

@shows_bp.route('/', methods=['POST'])
@token_required
def create_show():
    # Implement logic to create a new show in the database
    data = request.get_json()
    local = data['local']
    data_show = data['data']
    artista_id = data['artista_id']
    new_show = Show(nome=data['nome'], local=local, data=data_show, artista_id=artista_id)
    db.add(new_show)
    db.commit()
    return jsonify(new_show.to_dict())

@shows_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_show(id):
    # Implement logic to update an existing show in the database
    data = request.get_json()
    show = db.query(Show).filter(Show.id == id).first()
    if show:
        local = data.get('local')
        data_show = data.get('data')
        artista_id = data.get('artista_id')
        if local:
            show.local = local
        if data_show:
            show.data = data_show
        if artista_id:
            show.artista_id = artista_id
        db.commit()
        return jsonify(show.to_dict())
    return jsonify({'message': 'Show not found'})

@shows_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_show(id):
    # Implement logic to delete a specific show by ID from the database
    show = db.query(Show).filter(Show.id == id).first()
    if show:
        db.delete(show)
        db.commit()
        return jsonify({'message': f'Show with id {id} deleted successfully'})
    return jsonify({'message': 'Show not found'})
