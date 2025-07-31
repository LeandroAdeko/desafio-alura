from flask import Blueprint, request, jsonify
from db.database import Database
from services.auth import token_required

avaliacoes_modelo_bp = Blueprint('avaliacoes_modelo', __name__, url_prefix='/avaliacoes_modelo')
db = Database()

@avaliacoes_modelo_bp.route('/', methods=['GET'])
@token_required
def get_avaliacoes_modelo():
    # Implement logic to retrieve all avaliacoes_modelo from the database
    query = "SELECT * FROM avaliacoes_modelo"
    result = db.execute_query(query)
    return jsonify(result)

@avaliacoes_modelo_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_avaliacao_modelo(id):
    # Implement logic to retrieve a specific avaliacao_modelo by ID from the database
    result = db.get_by_id("avaliacoes_modelo", id)
    return jsonify(result)

@avaliacoes_modelo_bp.route('/', methods=['POST'])
@token_required
def create_avaliacao_modelo():
    # Implement logic to create a new avaliacao_modelo in the database
    data = request.get_json()
    recall_spam = data['recall_spam']
    f1_macro = data['f1_macro']
    acuracia_total = data['acuracia_total']
    passou_threshold = data['passou_threshold']
    query = "INSERT INTO avaliacoes_modelo (recall_spam, f1_macro, acuracia_total, passou_threshold) VALUES (%s, %s, %s, %s)"
    params = (recall_spam, f1_macro, acuracia_total, passou_threshold)
    db.execute_query(query, params)
    return jsonify({'message': 'Avaliacao modelo created successfully'})

@avaliacoes_modelo_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_avaliacao_modelo(id):
    # Implement logic to update an existing avaliacao_modelo in the database
    data = request.get_json()
    recall_spam = data.get('recall_spam')
    f1_macro = data.get('f1_macro')
    acuracia_total = data.get('acuracia_total')
    passou_threshold = data.get('passou_threshold')
    update_data = {}
    if recall_spam:
        update_data['recall_spam'] = recall_spam
    if f1_macro:
        update_data['f1_macro'] = f1_macro
    if acuracia_total:
        update_data['acuracia_total'] = acuracia_total
    if passou_threshold:
        update_data['passou_threshold'] = passou_threshold
    db.update_data("avaliacoes_modelo", id, update_data)
    return jsonify({'message': f'Avaliacao modelo with id {id} updated successfully'})

@avaliacoes_modelo_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_avaliacao_modelo(id):
    # Implement logic to delete a specific avaliacao_modelo by ID from the database
    where_condition = f"id = {id}"
    db.delete_data("avaliacoes_modelo", where_condition)
    return jsonify({'message': f'Avaliacao modelo with id {id} deleted successfully'})
