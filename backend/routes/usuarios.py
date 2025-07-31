from flask import Blueprint, request, jsonify
from db.database import get_db
from services.auth import token_required
from models import Usuario

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')
db = get_db()

@usuarios_bp.route('/', methods=['GET'])
@token_required
def get_usuarios():
    # Implement logic to retrieve all usuarios from the database
    usuarios = db.query(Usuario).all()
    return jsonify([usuario.to_dict() for usuario in usuarios])

@usuarios_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_usuario(id):
    # Implement logic to retrieve a specific usuario by ID from the database
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if usuario:
        return jsonify(usuario.to_dict())
    return jsonify({'message': 'Usuario not found'})

@usuarios_bp.route('/', methods=['POST'])
@token_required
def create_usuario():
    # Implement logic to create a new usuario in the database
    data = request.get_json()
    nome = data['nome']
    email = data['email']
    senha_hash = data['senha_hash']
    is_admin = data.get('is_admin', False)
    new_usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash, is_admin=is_admin)
    db.add(new_usuario)
    db.commit()
    return jsonify(new_usuario.to_dict())

@usuarios_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_usuario(id):
    # Implement logic to update an existing usuario in the database
    data = request.get_json()
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if usuario:
        nome = data.get('nome')
        email = data.get('email')
        senha_hash = data.get('senha_hash')
        is_admin = data.get('is_admin')
        if nome:
            usuario.nome = nome
        if email:
            usuario.email = email
        if senha_hash:
            usuario.senha_hash = senha_hash
        if is_admin is not None:
            usuario.is_admin = is_admin
        db.commit()
        return jsonify(usuario.to_dict())
    return jsonify({'message': 'Usuario not found'})

@usuarios_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_usuario(id):
    # Implement logic to delete a specific usuario by ID from the database
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
        return jsonify({'message': f'Usuario with id {id} deleted successfully'})
    return jsonify({'message': 'Usuario not found'})
