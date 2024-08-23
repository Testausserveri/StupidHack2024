from flask import (
    Blueprint, request, render_template
)

from . import backend

bp = Blueprint("endpoints", __name__, url_prefix="/", template_folder="templates")


@bp.route("/", methods=("GET",))
def index():
    return render_template("index.html"), 200


@bp.route("/correct", methods=("POST",))
def correct():
    word = request.form.get("word")

    return "kissa", 200


@bp.route("/submit", methods=("POST",))
def submit():
    input = request.form.get("input")

    response = backend.aimodel(input)
    return response, 200
