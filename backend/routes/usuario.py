import logging
import bcrypt
from flask import Blueprint, request, jsonify
from db.database import get_db
from models import Usuario

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


account_bp = Blueprint('account', __name__, url_prefix="/account")
db = get_db()


def get_user_by_email(email,):
    return db.query(Usuario).filter(Usuario.email == email).first()


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


@account_bp.route('', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    db_user = get_user_by_email(data.get('email'))

    if db_user:
        return jsonify({"message": "Email already registered"}), 400
    
    hashed_password = bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt())
    data['hashed_password'] = hashed_password
    data.pop('password')
    usuario = Usuario(**data)

    db_user = Usuario(username=usuario.username, hashed_password=hashed_password.decode('utf-8'), email=usuario.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return jsonify({"message": f"Seja bem vindo, {usuario.username}"}), 200


@account_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    logging.info(data)
    
    user: Usuario = get_user_by_email(data.get('email'))

    if not user:
        return jsonify({"message": "Email ou senha incorretos"}), 401
    if not verify_password(data.get('password'), user.hashed_password):
        return jsonify({"message": "Email ou senha incorretos"}), 401
    
    access_token = create_access_token(identity=user.email)
    return jsonify({"message": "Login bem sucedido", "access_token": access_token, "is_admin": user.is_admin}), 200


@account_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = db.query(Usuario).filter(Usuario.id == id).first()
    if user:
        return jsonify(user.to_dict())
    return jsonify({'message': 'Usuario não encontrado'})


@account_bp.route('', methods=['PATCH'])
@jwt_required()
def update_password():
    data = request.get_json()
    id = data.get('id')
    user = db.query(Usuario).filter(Usuario.id == id).first()

    if not user:
        return jsonify({'message': 'Usuario não encontrado'}), 404
    
    password = data.get('password')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    if hashed_password != Usuario.hashed_password:
        return jsonify({'message': 'Senha incorreta'}), 401


    new_password = data.get('new_password')
    new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    user.hashed_password = new_hashed_password
    db.commit()
    return jsonify({'message': 'Senha atualizada'}), 200

    
@account_bp.route('', methods=['DELETE'])
@jwt_required()
def delete_usuario():
    data = request.get_json()

    usuario = db.query(Usuario).filter(Usuario.email == data.get('email')).first()

    if usuario:
        if verify_password(data.get('password'), usuario.hashed_password):
            return jsonify({'message': 'Senha incorreta'}), 400
        db.delete(usuario)
        db.commit()
        return jsonify({'message': f"Usuario '{usuario.username}' deleted successfully"}), 200
    return jsonify({'message': 'Usuario not found'}), 400


@account_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

