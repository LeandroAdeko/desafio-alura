from flask import Blueprint, request, jsonify
from db.database import get_db
from models import Album
from flask_jwt_extended import jwt_required

albuns_bp = Blueprint('albuns', __name__, url_prefix='/albuns')
db = get_db()

@albuns_bp.route('', methods=['GET'])
#@jwt_required()
def get_albuns():
    albuns = db.query(Album).all()
    return jsonify([album.to_dict() for album in albuns])

@albuns_bp.route('/<int:id>', methods=['GET'])
#@jwt_required()
def get_album(id):
    album = db.query(Album).filter(Album.id == id).first()
    if album:
        return jsonify(album.to_dict())
    return jsonify({'message': 'Album not found'})

@albuns_bp.route('', methods=['POST'])
#@jwt_required()
def create_album():
    data = request.get_json()
    nome = data['nome']
    lancamento = data['lancamento']
    artista_id = data['artista_id']
    new_album = Album(nome=nome, artista_id=artista_id, lancamento=lancamento)
    db.add(new_album)
    db.commit()
    return jsonify(new_album.to_dict())

@albuns_bp.route('/<int:id>', methods=['PUT'])
#@jwt_required()
def update_album(id):
    data = request.get_json()
    album = db.query(Album).filter(Album.id == id).first()
    if album:
        nome = data.get('nome')
        artista_id = data.get('artista_id')
        if nome:
            album.nome = nome
        if artista_id:
            album.artista_id = artista_id
        db.commit()
        return jsonify(album.to_dict())
    return jsonify({'message': 'Album not found'})

@albuns_bp.route('/<int:id>', methods=['DELETE'])
#@jwt_required()
def delete_album(id):
    album = db.query(Album).filter(Album.id == id).first()
    if album:
        db.delete(album)
        db.commit()
        return jsonify({'message': f'Album with id {id} deleted successfully'})
    return jsonify({'message': 'Album not found'})
