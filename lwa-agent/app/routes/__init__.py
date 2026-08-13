from flask_smorest import Blueprint

api = Blueprint(
    "api",
    __name__,
    url_prefix="/api/v1",
    description="RAG API"
)

from .message import blp as MessageBlueprint
api.register_blueprint(MessageBlueprint)