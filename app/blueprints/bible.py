from flask import Blueprint, render_template

bp = Blueprint("bible", __name__)


@bp.route("/")
def home():
    return render_template("index.html")
