from src.app import server
from .health import api as health_blueprint

app = server.get_app()

app.register_blueprint(health_blueprint)
