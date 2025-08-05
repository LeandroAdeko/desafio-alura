from flask import Blueprint, request, jsonify
from db.database import get_db
from flask_jwt_extended import jwt_required
from models import Artista
import logging

artistas_bp = Blueprint('artistas', __name__, url_prefix='/artistas')
db = get_db()

@artistas_bp.route('', methods=['GET'])
#@jwt_required()
def get_artistas():
    # Implement logic to retrieve all artistas from the database
    artistas = db.query(Artista).all()
    result = [artista.to_dict() for artista in artistas]
    # logging.warning(result)
    return jsonify(result)

@artistas_bp.route('/<int:id>', methods=['GET'])
#@jwt_required()
def get_artista(id):
    # Implement logic to retrieve a specific artista by ID from the database
    artista = db.query(Artista).filter(Artista.id == id).first()
    if artista:
        return jsonify(artista.to_dict())
    return jsonify({'message': 'Artista not found'})

@artistas_bp.route('', methods=['POST'])
#@jwt_required()
def create_artista():
    data = request.get_json()
    nome = data['nome']
    new_artista = Artista(nome=nome)
    db.add(new_artista)
    db.commit()
    return jsonify(new_artista.to_dict())

@artistas_bp.route('/<int:id>', methods=['PUT'])
#@jwt_required()
def update_artista(id):
    data = request.get_json()
    artista = db.query(Artista).filter(Artista.id == id).first()
    if artista:
        nome = data.get('nome')
        if nome:
            artista.nome = nome
        db.commit()
        return jsonify(artista.to_dict())
    return jsonify({'message': 'Artista not found'})

@artistas_bp.route('/<int:id>', methods=['DELETE'])
#@jwt_required()
def delete_artista(id):
    # Implement logic to delete a specific artista by ID from the database
    artista = db.query(Artista).filter(Artista.id == id).first()
    if artista:
        db.delete(artista)
        db.commit()
        return jsonify({'message': f'Artista with id {id} deleted successfully'})
    return jsonify({'message': 'Artista not found'})
