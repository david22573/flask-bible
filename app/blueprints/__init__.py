from . import bible


def register_blueprints(app):
    app.register_blueprint(bible.bp)
