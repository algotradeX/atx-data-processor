from src.app import server
from src.exception import errors
from .health import api as health_blueprint
from .nsc import api as nsc_blueprint

app = server.get_app()

app.register_blueprint(health_blueprint)
app.register_blueprint(nsc_blueprint)
app.register_blueprint(errors)
