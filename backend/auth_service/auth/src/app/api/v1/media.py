from flask import Blueprint, url_for

media = Blueprint("media", __name__)


@media.route("/<image>")
def index(image):
    return url_for("index", image=image, _external=True)
