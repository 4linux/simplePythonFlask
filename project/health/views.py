from flask import Blueprint, current_app, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from project import db


health_blueprint = Blueprint("health", __name__)


@health_blueprint.route('/health', methods=['GET'])
def health():
    """A aplicacao esta no ar. Nao consulta o banco de dados."""
    return jsonify(status='ok', version=current_app.config['APP_VERSION'])


@health_blueprint.route('/ready', methods=['GET'])
def ready():
    """A aplicacao consegue atender requisicoes, ou seja, o banco responde."""
    try:
        db.session.execute(text('SELECT 1'))
    except SQLAlchemyError:
        return jsonify(status='unavailable', database='down'), 503
    return jsonify(status='ok', database='up')
