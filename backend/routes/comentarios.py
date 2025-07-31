from flask import Blueprint, request, jsonify
from db.database import get_db
from services.auth import token_required
from models import Comentario
import uuid
from services.gemini import Gemini

comentarios_bp = Blueprint('comentarios', __name__, url_prefix='/comentarios')
db = get_db()

@comentarios_bp.route('/', methods=['GET'])
@token_required
def get_comentarios():
    # Implement logic to retrieve all comentarios from the database
    comentarios = db.query(Comentario).all()
    return jsonify([comentario.to_dict() for comentario in comentarios])

@comentarios_bp.route('/<uuid:id>', methods=['GET'])
@token_required
def get_comentario(id):
    # Implement logic to retrieve a specific comentario by ID from the database
    comentario = db.query(Comentario).filter(Comentario.id == id).first()
    if comentario:
        return jsonify(comentario.to_dict())
    return jsonify({'message': 'Comentario not found'})

@comentarios_bp.route('/', methods=['POST'])
@token_required
def create_comentario():
    ai = Gemini()
    # Implement logic to create a new comentario in the database
    data = request.get_json()
    texto = data['texto']

    result = ai.classify_comment(texto)
    categoria = result.classificacao
    confianca = result.confianca

    origem = data['origem']
    artista_id = data.get('artista_id')
    album_id = data.get('album_id')
    clipe_id = data.get('clipe_id')
    show_id = data.get('show_id')
    comentario_id = uuid.uuid4()
    new_comentario = Comentario(id=comentario_id, texto=texto, categoria=categoria, confianca=confianca, origem=origem, artista_id=artista_id, album_id=album_id, clipe_id=clipe_id, show_id=show_id)
    db.add(new_comentario)
    db.commit()
    return jsonify(new_comentario.to_dict())

@comentarios_bp.route('/<uuid:id>', methods=['PUT'])
@token_required
def update_comentario(id):
    # Implement logic to update an existing comentario in the database
    data = request.get_json()
    comentario = db.query(Comentario).filter(Comentario.id == id).first()
    if comentario:
        texto = data.get('texto')
        categoria = data.get('categoria')
        confianca = data.get('confianca')
        origem = data.get('origem')
        artista_id = data.get('artista_id')
        album_id = data.get('album_id')
        clipe_id = data.get('clipe_id')
        show_id = data.get('show_id')
        if texto:
            comentario.texto = texto
        if categoria:
            comentario.categoria = categoria
        if confianca:
            comentario.confianca = confianca
        if origem:
            comentario.origem = origem
        if artista_id:
            comentario.artista_id = artista_id
        if album_id:
            comentario.album_id = album_id
        if clipe_id:
            comentario.clipe_id = clipe_id
        if show_id:
            comentario.show_id = show_id
        db.commit()
        return jsonify(comentario.to_dict())
    return jsonify({'message': f'Comentario with id {id} updated successfully'})

@comentarios_bp.route('/<uuid:id>', methods=['DELETE'])
@token_required
def delete_comentario(id):
    # Implement logic to delete a specific comentario by ID from the database
    comentario = db.query(Comentario).filter(Comentario.id == id).first()
    if comentario:
        db.delete(comentario)
        db.commit()
        return jsonify({'message': f'Comentario with id {id} deleted successfully'})
    return jsonify({'message': 'Comentario not found'})
