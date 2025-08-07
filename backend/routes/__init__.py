from routes.albuns import albuns_bp
from routes.artistas import artistas_bp
from routes.comentario_tags import comentario_tags_bp
from routes.comentarios import comentarios_bp
from routes.shows import shows_bp
from routes.usuario import account_bp
from routes.tags import tags_bp
from routes.clipes import clipes_bp
from routes.query import query_bp


blueprints = [
    albuns_bp,
    artistas_bp,
    comentario_tags_bp,
    account_bp,
    comentarios_bp,
    shows_bp,
    tags_bp,
    clipes_bp,
    query_bp
]
