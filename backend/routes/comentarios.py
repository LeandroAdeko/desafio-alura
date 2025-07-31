from flask import Blueprint, request, jsonify
from db.database import Database
from services.auth import token_required
import uuid

comentarios_bp = Blueprint('comentarios', __name__, url_prefix='/comentarios')
db = Database()

@comentarios_bp.route('/', methods=['GET'])
@token_required
def get_comentarios():
    # Implement logic to retrieve all comentarios from the database
    query = "SELECT * FROM comentarios"
    result = db.execute_query(query)
    return jsonify(result)

@comentarios_bp.route('/<uuid:id>', methods=['GET'])
@token_required
def get_comentario(id):
    # Implement logic to retrieve a specific comentario by ID from the database
    query = "SELECT * FROM comentarios WHERE id = %s"
    result = db.fetch_one(query, (str(id),))
    return jsonify(result)

@comentarios_bp.route('/', methods=['POST'])
@token_required
def create_comentario():
    # Implement logic to create a new comentario in the database
    data = request.get_json()
    texto = data['texto']
    categoria = data['categoria']
    confianca = data['confianca']
    origem = data['origem']
    artista_id = data.get('artista_id')
    album_id = data.get('album_id')
    clipe_id = data.get('clipe_id')
    show_id = data.get('show_id')
    comentario_id = uuid.uuid4()
    query = "INSERT INTO comentarios (id, texto, categoria, confianca, origem, artista_id, album_id, clipe_id, show_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    params = (comentario_id, texto, categoria, confianca, origem, artista_id, album_id, clipe_id, show_id)
    db.execute_query(query, params)
    return jsonify({'message': 'Comentario created successfully'})

@comentarios_bp.route('/<uuid:id>', methods=['PUT'])
@token_required
def update_comentario(id):
    # Implement logic to update an existing comentario in the database
    data = request.get_json()
    texto = data.get('texto')
    categoria = data.get('categoria')
    confianca = data.get('confianca')
    origem = data.get('origem')
    artista_id = data.get('artista_id')
    album_id = data.get('album_id')
    clipe_id = data.get('clipe_id')
    show_id = data.get('show_id')
    update_data = {}
    if texto:
        update_data['texto'] = texto
    if categoria:
        update_data['categoria'] = categoria
    if confianca:
        update_data['confianca'] = confianca
    if origem:
        update_data['origem'] = origem
    if artista_id:
        update_data['artista_id'] = artista_id
    if album_id:
        update_data['album_id'] = album_id
    if clipe_id:
        update_data['clipe_id'] = clipe_id
    if show_id:
        update_data['show_id'] = show_id
    db.update_data("comentarios", str(id), update_data)
    return jsonify({'message': f'Comentario with id {id} updated successfully'})

@comentarios_bp.route('/<uuid:id>', methods=['DELETE'])
@token_required
def delete_comentario(id):
    # Implement logic to delete a specific comentario by ID from the database
    where_condition = f"id = '{id}'"
    db.delete_data("comentarios", where_condition)
    return jsonify({'message': f'Comentario with id {id} deleted successfully'})
