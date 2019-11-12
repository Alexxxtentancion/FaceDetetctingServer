import os

from aiohttp import web
import dlib
from routes import setup_routes


def create_app():
    app = web.Application()
    app['sp'] = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    app['frm'] = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    setup_routes(app)
    return app


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    web.run_app(create_app(), port=port)
