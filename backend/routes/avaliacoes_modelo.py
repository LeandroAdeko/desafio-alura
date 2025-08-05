from flask import Blueprint, request, jsonify
from db.database import get_db
from models import AvaliacaoModelo
from flask_jwt_extended import jwt_required

avaliacoes_modelo_bp = Blueprint('avaliacoes_modelo', __name__, url_prefix='/avaliacoes_modelo')
db = get_db()

@avaliacoes_modelo_bp.route('', methods=['GET'])
#@jwt_required()
def get_avaliacoes_modelo():
    # Implement logic to retrieve all avaliacoes_modelo from the database
    avaliacoes_modelo = db.query(AvaliacaoModelo).all()
    return jsonify([avaliacao_modelo.to_dict() for avaliacao_modelo in avaliacoes_modelo])

@avaliacoes_modelo_bp.route('/<int:id>', methods=['GET'])
#@jwt_required()
def get_avaliacao_modelo(id):
    # Implement logic to retrieve a specific avaliacao_modelo by ID from the database
    avaliacao_modelo = db.query(AvaliacaoModelo).filter(AvaliacaoModelo.id == id).first()
    if avaliacao_modelo:
        return jsonify(avaliacao_modelo.to_dict())
    return jsonify({'message': 'Avaliacao modelo not found'})

@avaliacoes_modelo_bp.route('', methods=['POST'])
#@jwt_required()
def create_avaliacao_modelo():
    # Implement logic to create a new avaliacao_modelo in the database
    data = request.get_json()
    recall_spam = data['recall_spam']
    f1_macro = data['f1_macro']
    acuracia_total = data['acuracia_total']
    passou_threshold = data['passou_threshold']
    new_avaliacao_modelo = AvaliacaoModelo(recall_spam=recall_spam, f1_macro=f1_macro, acuracia_total=acuracia_total, passou_threshold=passou_threshold)
    db.add(new_avaliacao_modelo)
    db.commit()
    return jsonify(new_avaliacao_modelo.to_dict())

@avaliacoes_modelo_bp.route('/<int:id>', methods=['PUT'])
#@jwt_required()
def update_avaliacao_modelo(id):
    # Implement logic to update an existing avaliacao_modelo in the database
    data = request.get_json()
    avaliacao_modelo = db.query(AvaliacaoModelo).filter(AvaliacaoModelo.id == id).first()
    if avaliacao_modelo:
        recall_spam = data.get('recall_spam')
        f1_macro = data.get('f1_macro')
        acuracia_total = data.get('acuracia_total')
        passou_threshold = data.get('passou_threshold')
        if recall_spam:
            avaliacao_modelo.recall_spam = recall_spam
        if f1_macro:
            avaliacao_modelo.f1_macro = f1_macro
        if acuracia_total:
            avaliacao_modelo.acuracia_total = acuracia_total
        if passou_threshold:
            avaliacao_modelo.passou_threshold = passou_threshold
        db.commit()
        return jsonify(avaliacao_modelo.to_dict())
    return jsonify({'message': 'Avaliacao modelo not found'})

@avaliacoes_modelo_bp.route('/<int:id>', methods=['DELETE'])
#@jwt_required()
def delete_avaliacao_modelo(id):
    # Implement logic to delete a specific avaliacao_modelo by ID from the database
    avaliacao_modelo = db.query(AvaliacaoModelo).filter(AvaliacaoModelo.id == id).first()
    if avaliacao_modelo:
        db.delete(avaliacao_modelo)
        db.commit()
        return jsonify({'message': f'Avaliacao modelo with id {id} deleted successfully'})
    return jsonify({'message': 'Avaliacao modelo not found'})
