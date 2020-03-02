from src.server import Server

server = Server()
app = server.get_app()
# Import atx-data-processor routes to add blueprint to server
import src.routes  # noqa: E731
