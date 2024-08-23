from flask import (
    Blueprint, request, render_template
)

bp = Blueprint("endpoints", __name__, url_prefix="/", template_folder="templates")


@bp.route("/", methods=("GET",))
def index():
    return render_template("index.html"), 200


@bp.route("/submit", methods=("POST",))
def submit():
    print(f"data: {request.values}")
    decoded = request.get_json()

    return f"data:{request.values['data']}"