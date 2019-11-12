from views.main import test, compare_images


def setup_routes(app):
    app.router.add_get(r'/test', test)
    app.router.add_post(r'/compare', compare_images)
