from flask import (
    Blueprint, request, render_template
)

from myfirstaimodel.corrector import corrector

from . import backend

bp = Blueprint("endpoints", __name__, url_prefix="/", template_folder="templates", static_folder="templates")


@bp.route("/", methods=("GET",))
def index():
    return render_template("index.html"), 200


@bp.route("/scribula.js", methods=("GET",))
def scribula():
    return bp.send_static_file("scribula.js")


@bp.route("/correct", methods=("POST",))
def correct():
    input = request.form.get("input")

    return corrector(input), 200


@bp.route("/submit", methods=("POST",))
def submit():
    input = request.form.get("input").split() + [""]*10

    response = backend.aimodel(input)
    return response, 200
