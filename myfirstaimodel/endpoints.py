from flask import (
    Blueprint, request, render_template
)

bp = Blueprint("endpoints", __name__, url_prefix="/", template_folder="templates")


@bp.route("/", methods=("GET",))
def index():
    return render_template("index.html"), 200
