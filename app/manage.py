import os
from flask.cli import FlaskGroup
from flask import Flask

from views import main_blueprint


def create_app(script_info=None):
    app = Flask(
        __name__,
        template_folder="./templates"
    )

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)
    app.register_blueprint(main_blueprint)
    app.shell_context_processor({"app": app})

    return app


app = create_app()
cli = FlaskGroup(create_app=create_app)


if __name__ == "__main__":
    cli()
