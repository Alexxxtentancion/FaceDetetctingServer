import os

from aiohttp import web

from routes import setup_routes


def create_app():
    app = web.Application()
    setup_routes(app)
    return app


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    web.run_app(create_app(), port=port)
