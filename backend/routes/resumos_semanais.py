from flask import Blueprint, request, jsonify
from db.database import get_db
from services.auth import token_required
from models import ResumoSemanal

resumos_semanais_bp = Blueprint('resumos_semanais', __name__, url_prefix='/resumos_semanais')
db = get_db()

@resumos_semanais_bp.route('/', methods=['GET'])
@token_required
def get_resumos_semanais():
    # Implement logic to retrieve all resumos_semanais from the database
    resumos_semanais = db.query(ResumoSemanal).all()
    return jsonify([resumo_semanal.to_dict() for resumo_semanal in resumos_semanais])

@resumos_semanais_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_resumo_semanal(id):
    # Implement logic to retrieve a specific resumo_semanal by ID from the database
    resumo_semanal = db.query(ResumoSemanal).filter(ResumoSemanal.id == id).first()
    if resumo_semanal:
        return jsonify(resumo_semanal.to_dict())
    return jsonify({'message': 'Resumo semanal not found'})

@resumos_semanais_bp.route('/', methods=['POST'])
@token_required
def create_resumo_semanal():
    # Implement logic to create a new resumo_semanal in the database
    data = request.get_json()
    semana_ref = data['semana_ref']
    texto_resumo = data['texto_resumo']
    new_resumo_semanal = ResumoSemanal(semana_ref=semana_ref, texto_resumo=texto_resumo)
    db.add(new_resumo_semanal)
    db.commit()
    return jsonify(new_resumo_semanal.to_dict())

@resumos_semanais_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_resumo_semanal(id):
    # Implement logic to update an existing resumo_semanal in the database
    data = request.get_json()
    resumo_semanal = db.query(ResumoSemanal).filter(ResumoSemanal.id == id).first()
    if resumo_semanal:
        semana_ref = data.get('semana_ref')
        texto_resumo = data.get('texto_resumo')
        if semana_ref:
            resumo_semanal.semana_ref = semana_ref
        if texto_resumo:
            resumo_semanal.texto_resumo = texto_resumo
        db.commit()
        return jsonify(resumo_semanal.to_dict())
    return jsonify({'message': 'Resumo semanal not found'})

@resumos_semanais_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_resumo_semanal(id):
    # Implement logic to delete a specific resumo_semanal by ID from the database
    resumo_semanal = db.query(ResumoSemanal).filter(ResumoSemanal.id == id).first()
    if resumo_semanal:
        db.delete(resumo_semanal)
        db.commit()
        return jsonify({'message': f'Resumo semanal with id {id} deleted successfully'})
    return jsonify({'message': 'Resumo semanal not found'})
