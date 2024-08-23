from flask import (
    Blueprint, request, render_template
)

from . import backend

bp = Blueprint("endpoints", __name__, url_prefix="/", template_folder="templates")


@bp.route("/", methods=("GET",))
def index():
    return render_template("index.html"), 200


@bp.route("/options", methods=("GET",))
def options():
    pass


@bp.route("/correct", methods=("POST",))
def correct():
    word = request.form.get("word")

    return "kissa", 200


@bp.route("/submit", methods=("POST",))
def submit():
    input1 = request.form.get("input1")
    input2 = request.form.get("input2")
    input3 = request.form.get("input3")
    input4 = request.form.get("input4")

    response = backend.aimodel(input1, input2, input3, input4)
    return response, 200
