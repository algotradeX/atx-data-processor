from src.app import app
from dynaconf import settings

if __name__ == '__main__':
    app.run(host=settings.API.SERVER.url, port=settings.API.SERVER.port, debug=settings.DEBUG)
