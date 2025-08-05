from flask import Blueprint, request, jsonify
from db.database import get_db
from models import Tag
from flask_jwt_extended import jwt_required

tags_bp = Blueprint('tags', __name__, url_prefix='/tags')
db = get_db()

@tags_bp.route('', methods=['GET'])
#@jwt_required()
def get_tags():
    # Implement logic to retrieve all tags from the database
    tags = db.query(Tag).all()
    return jsonify([tag.to_dict() for tag in tags])

@tags_bp.route('/<int:id>', methods=['GET'])
#@jwt_required()
def get_tag(id):
    # Implement logic to retrieve a specific tag by ID from the database
    tag = db.query(Tag).filter(Tag.id == id).first()
    if tag:
        return jsonify(tag.to_dict())
    return jsonify({'message': 'Tag not found'})

@tags_bp.route('', methods=['POST'])
#@jwt_required()
def create_tag():
    # Implement logic to create a new tag in the database
    data = request.get_json()
    codigo = data['codigo']
    descricao = data['descricao']
    new_tag = Tag(codigo=codigo, descricao=descricao)
    db.add(new_tag)
    db.commit()
    return jsonify(new_tag.to_dict())

@tags_bp.route('/<int:id>', methods=['PUT'])
#@jwt_required()
def update_tag(id):
    # Implement logic to update an existing tag in the database
    data = request.get_json()
    tag = db.query(Tag).filter(Tag.id == id).first()
    if tag:
        codigo = data.get('codigo')
        descricao = data.get('descricao')
        if codigo:
            tag.codigo = codigo
        if descricao:
            tag.descricao = descricao
        db.commit()
        return jsonify(tag.to_dict())
    return jsonify({'message': 'Tag not found'})

@tags_bp.route('/<int:id>', methods=['DELETE'])
#@jwt_required()
def delete_tag(id):
    # Implement logic to delete a specific tag by ID from the database
    tag = db.query(Tag).filter(Tag.id == id).first()
    if tag:
        db.delete(tag)
        db.commit()
        return jsonify({'message': f'Tag with id {id} deleted successfully'})
    return jsonify({'message': 'Tag not found'})
