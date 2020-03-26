from src.app import server
from src.exception import errors
from .health import api as health_blueprint
from .nse import api as nse_blueprint

app = server.get_app()

app.register_blueprint(health_blueprint)
app.register_blueprint(nse_blueprint)
app.register_blueprint(errors)
