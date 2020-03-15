from dynaconf import settings

from src.common import Logger

log = Logger()


def add_flask_profiler(app, pg_settings=settings["POSTGRES"]):
    try:
        if settings.PROFILER["flask-profiler"]:
            from flask_profiler import Profiler

            app.config["flask_profiler"] = {
                "enabled": settings.DEBUG,
                "storage": {
                    "engine": "sqlalchemy",
                    "db_url": pg_settings["uri"] + "/" + pg_settings["db"],
                },
                "basicAuth": {
                    "enabled": True,
                    "username": "admin",
                    "password": "admin",
                },
                "ignore": ["^/static/.*"],
            }
            log.info(
                f"flask_profiler starting at url : http://{settings.API.SERVER.url}:{settings.API.SERVER.port}/flask-profiler/"
            )
            log.info(
                f"flask_profiler starting with storage setup {app.config['flask_profiler']['storage']}"
            )
            Profiler(app)
    except ImportError:
        log.info("flask_profiler ImportError")
