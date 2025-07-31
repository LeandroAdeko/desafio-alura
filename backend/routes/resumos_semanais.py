from flask import Blueprint, request, jsonify
from db.database import Database
from services.auth import token_required

resumos_semanais_bp = Blueprint('resumos_semanais', __name__, url_prefix='/resumos_semanais')
db = Database()

@resumos_semanais_bp.route('/', methods=['GET'])
@token_required
def get_resumos_semanais():
    # Implement logic to retrieve all resumos_semanais from the database
    query = "SELECT * FROM resumos_semanais"
    result = db.execute_query(query)
    return jsonify(result)

@resumos_semanais_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_resumo_semanal(id):
    # Implement logic to retrieve a specific resumo_semanal by ID from the database
    result = db.get_by_id("resumos_semanais", id)
    return jsonify(result)

@resumos_semanais_bp.route('/', methods=['POST'])
@token_required
def create_resumo_semanal():
    # Implement logic to create a new resumo_semanal in the database
    data = request.get_json()
    semana_ref = data['semana_ref']
    texto_resumo = data['texto_resumo']
    query = "INSERT INTO resumos_semanais (semana_ref, texto_resumo) VALUES (%s, %s)"
    params = (semana_ref, texto_resumo)
    db.execute_query(query, params)
    return jsonify({'message': 'Resumo semanal created successfully'})

@resumos_semanais_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_resumo_semanal(id):
    # Implement logic to update an existing resumo_semanal in the database
    data = request.get_json()
    semana_ref = data.get('semana_ref')
    texto_resumo = data.get('texto_resumo')
    update_data = {}
    if semana_ref:
        update_data['semana_ref'] = semana_ref
    if texto_resumo:
        update_data['texto_resumo'] = texto_resumo
    db.update_data("resumos_semanais", id, update_data)
    return jsonify({'message': f'Resumo semanal with id {id} updated successfully'})

@resumos_semanais_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_resumo_semanal(id):
    # Implement logic to delete a specific resumo_semanal by ID from the database
    where_condition = f"id = {id}"
    db.delete_data("resumos_semanais", where_condition)
    return jsonify({'message': f'Resumo semanal with id {id} deleted successfully'})
