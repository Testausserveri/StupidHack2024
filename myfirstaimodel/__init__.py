import os
from flask import Flask


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__, instance_path=os.path.join(os.getcwd(), "instance"))

    app.config.from_mapping(
        TESTING=testing,
        SECRET_KEY="balls",
    )

    from . import endpoints
    app.register_blueprint(endpoints.bp)

    return app