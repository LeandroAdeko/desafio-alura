from flask import Blueprint, request, jsonify
from db.database import get_db
from models import ComentarioTag
from flask_jwt_extended import jwt_required

comentario_tags_bp = Blueprint('comentario_tags', __name__, url_prefix='/comentario_tags')
db = get_db()

@comentario_tags_bp.route('', methods=['GET'])
@jwt_required()
def get_comentario_tags():
    comentario_tags = db.query(ComentarioTag).all()
    return jsonify([comentario_tag.to_dict() for comentario_tag in comentario_tags])

@comentario_tags_bp.route('/<uuid:comentario_id>/<int:tag_id>', methods=['GET'])
@jwt_required()
def get_comentario_tag(comentario_id, tag_id):
    comentario_tag = db.query(ComentarioTag).filter(ComentarioTag.comentario_id == comentario_id, ComentarioTag.tag_id == tag_id).first()
    if comentario_tag:
        return jsonify(comentario_tag.to_dict())
    return jsonify({'message': 'Comentario_tag not found'})

@comentario_tags_bp.route('', methods=['POST'])
@jwt_required()
def create_comentario_tag():
    data = request.get_json()
    comentario_id = data['comentario_id']
    tag_id = data['tag_id']
    new_comentario_tag = ComentarioTag(comentario_id=comentario_id, tag_id=tag_id)
    db.add(new_comentario_tag)
    db.commit()
    return jsonify(new_comentario_tag.to_dict())

@comentario_tags_bp.route('/<uuid:comentario_id>/<int:tag_id>', methods=['DELETE'])
@jwt_required()
def delete_comentario_tag(comentario_id, tag_id):
    comentario_tag = db.query(ComentarioTag).filter(ComentarioTag.comentario_id == comentario_id, ComentarioTag.tag_id == tag_id).first()
    if comentario_tag:
        db.delete(comentario_tag)
        db.commit()
        return jsonify({'message': f'Comentario_tag with comentario_id {comentario_id} and tag_id {tag_id} deleted successfully'})
    return jsonify({'message': 'Comentario_tag not found'})
