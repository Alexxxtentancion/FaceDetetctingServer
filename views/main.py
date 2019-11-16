import os

import dlib

from skimage import io
from scipy.spatial import distance
from aiohttp.web import json_response


async def test(request):
    return json_response(data={'status': 'ok'}, headers={'Access-Control-Allow-Origin': 'http://localhost:3000'}, status=200)


async def compare_images(request):
    data = await request.post()
    first_image = data['image1']
    second_image = data['image2']
    with open(first_image.filename, 'wb') as f:
        f.write(first_image.file.read())
    with open(second_image.filename, 'wb') as f:
        f.write(second_image.file.read())

    sp, frm = request.app['sp'], request.app['frm']
    first_face_descriptor = process_image(first_image.filename, sp, frm)
    second_face_descriptor = process_image(second_image.filename, sp, frm)
    a = distance.euclidean(first_face_descriptor, second_face_descriptor)
    if a < 0.6:
        res = 1
    else:
        res = 0
    return json_response(data={'status': 'ok', 'data': res, 'distance': a},headers={'Access-Control-Allow-Origin': 'http://localhost:3000'}, status=200)


def process_image(filename, sp, frm):
    detector = dlib.get_frontal_face_detector()
    img = io.imread(filename)
    dets = detector(img, 1)

    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
    shape = sp(img, d)

    face_descriptor = frm.compute_face_descriptor(img, shape)

    return face_descriptor
