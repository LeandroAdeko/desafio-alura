from flask import Blueprint, request, jsonify
from db.database import execute_query
import logging


query_bp = Blueprint('query', __name__, url_prefix='/query')

@query_bp.route('', methods=['POST'])
def execute_sql_query():
    try:
        query = request.json.get('query')
        if not query:
            return jsonify({'error': 'Query não fornecida'}), 400

        result = execute_query(query)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
