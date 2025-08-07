from flask import Blueprint, request, jsonify
from db.database import get_db
from models import Clipe
from flask_jwt_extended import jwt_required

clipes_bp = Blueprint('clipes', __name__, url_prefix='/clipes')
db = get_db()

@clipes_bp.route('', methods=['GET'])
@jwt_required()
def get_clipes():
    # Implement logic to retrieve all clipes from the database
    clipes = db.query(Clipe).all()
    return jsonify([clipe.to_dict() for clipe in clipes])

@clipes_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_clipe(id):
    # Implement logic to retrieve a specific clipe by ID from the database
    clipe = db.query(Clipe).filter(Clipe.id == id).first()
    if clipe:
        return jsonify(clipe.to_dict())
    return jsonify({'message': 'Clipe not found'})

@clipes_bp.route('', methods=['POST'])
@jwt_required()
def create_clipe():
    # Implement logic to create a new clipe in the database
    data = request.get_json()
    nome = data['nome']
    artista_id = data['artista_id']
    new_clipe = Clipe(nome=nome, artista_id=artista_id)
    db.add(new_clipe)
    db.commit()
    return jsonify(new_clipe.to_dict())

@clipes_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_clipe(id):
    # Implement logic to update an existing clipe in the database
    data = request.get_json()
    clipe = db.query(Clipe).filter(Clipe.id == id).first()
    if clipe:
        nome = data.get('nome')
        artista_id = data.get('artista_id')
        if nome:
            clipe.nome = nome
        if artista_id:
            clipe.artista_id = artista_id
        db.commit()
        return jsonify(clipe.to_dict())
    return jsonify({'message': 'Clipe not found'})

@clipes_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_clipe(id):
    # Implement logic to delete a specific clipe by ID from the database
    clipe = db.query(Clipe).filter(Clipe.id == id).first()
    if clipe:
        db.delete(clipe)
        db.commit()
        return jsonify({'message': f'Clipe with id {id} deleted successfully'})
    return jsonify({'message': 'Clipe not found'})
