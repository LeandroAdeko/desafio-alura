from flask import Blueprint, request, jsonify
from db.database import get_db
from models import Comentario
import uuid
from services.gemini import Gemini
from flask_jwt_extended import jwt_required
import asyncio
import aiohttp
import logging

comentarios_bp = Blueprint('comentarios', __name__, url_prefix='/comentarios')
db = get_db()

@comentarios_bp.route('', methods=['GET'])
@jwt_required()
def get_comentarios():
    # Implement logic to retrieve all comentarios from the database
    comentarios = db.query(Comentario).all()
    return jsonify([comentario.to_dict() for comentario in comentarios])

@comentarios_bp.route('/<uuid:id>', methods=['GET'])
@jwt_required()
def get_comentario(id):
    # Implement logic to retrieve a specific comentario by ID from the database
    comentario = db.query(Comentario).filter(Comentario.id == id).first()
    if comentario:
        return jsonify(comentario.to_dict())
    return jsonify({'message': 'Comentario not found'})

@comentarios_bp.route('', methods=['POST'])
@jwt_required()
def create_comentario():
    ai = Gemini()
    # Implement logic to create a new comentario in the database
    data = request.get_json()
    texto = data['texto']

    result = ai.classify_comment(texto)
    categoria = result.classificacao
    confianca = result.confianca

    artista_id = data.get('artista_id')
    album_id = data.get('album_id')
    clipe_id = data.get('clipe_id')
    show_id = data.get('show_id')
    criado_em = data.get('criado_em')
    comentario_id = uuid.uuid4()
    new_comentario = Comentario(id=comentario_id, texto=texto, categoria=categoria, confianca=confianca, artista_id=artista_id, album_id=album_id, clipe_id=clipe_id, show_id=show_id, criado_em=criado_em)
    db.add(new_comentario)
    db.commit()
    return jsonify(new_comentario.to_dict())

@comentarios_bp.route('/<uuid:id>', methods=['PUT'])
@jwt_required()
def update_comentario(id):
    # Implement logic to update an existing comentario in the database
    data = request.get_json()
    comentario = db.query(Comentario).filter(Comentario.id == id).first()
    if comentario:
        texto = data.get('texto')
        categoria = data.get('categoria')
        confianca = data.get('confianca')
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
@jwt_required()
def delete_comentario(id):
    # Implement logic to delete a specific comentario by ID from the database
    comentario = db.query(Comentario).filter(Comentario.id == id).first()
    if comentario:
        db.delete(comentario)
        db.commit()
        return jsonify({'message': f'Comentario with id {id} deleted successfully'})
    return jsonify({'message': 'Comentario not found'})

# async def create_comentario(data):
#     ai = Gemini()
#     texto = data['texto']

#     result = ai.classify_comment(texto)
#     categoria = result.classificacao
#     confianca = result.confianca

#     artista_id = data.get('artista_id')
#     album_id = data.get('album_id')
#     clipe_id = data.get('clipe_id')
#     show_id = data.get('show_id')
#     criado_em = data.get('criado_em')
#     comentario_id = uuid.uuid4()
#     new_comentario = Comentario(id=comentario_id, texto=texto, categoria=categoria, confianca=confianca, artista_id=artista_id, album_id=album_id, clipe_id=clipe_id, show_id=show_id, criado_em=criado_em)
#     return new_comentario

# async def enviar_comentarios_lote(session, comentarios):
#     db = get_db()
#     for comentario in comentarios:
#         db.add(comentario)
#     db.commit()
#     return [comentario.to_dict() for comentario in comentarios]

# @comentarios_bp.route('/lote', methods=['POST'])
# async def create_comentarios_lote():
#     data = request.get_json()  # Recebe uma lista de comentários
#     if not isinstance(data, list):
#         return jsonify({'message': 'Expected a list of comments'}), 400

#     comentarios = []
#     for comentario_data in data:
#         comentario = await create_comentario(comentario_data)
#         comentarios.append(comentario)
    
#     tentativas = 0
#     while tentativas < 2:
#         try:
#             async with aiohttp.ClientSession() as session:
#                 result = await enviar_comentarios_lote(session, comentarios)
#                 return jsonify(result), 201
#         except aiohttp.ClientResponseError as e:
#             if e.status == 503:
#                 tentativas += 1
#                 print(f"Erro 503 ao enviar lote. Tentativa {tentativas}/2. Aguardando 10 segundos...")
#                 await asyncio.sleep(10)
#             else:
#                 print(f"Erro ao enviar lote: {e}")
#                 return jsonify({'message': 'Erro ao criar lote de comentários'}), 500
#         except Exception as e:
#             print(f"Erro ao enviar lote: {e}")
#             return jsonify({'message': 'Erro ao criar lote de comentários'}), 500
#     print("Erro ao enviar lote após 2 tentativas. Abortando.")
#     return jsonify({'message': 'Erro ao criar lote de comentários após várias tentativas'}), 500
