from views.main import test


def setup_routes(app):
    app.router.add_get(r'/test', test)
