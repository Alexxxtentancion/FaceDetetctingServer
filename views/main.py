import aiohttp
import dlib
from skimage import io
from scipy.spatial import distance
from aiohttp.web import json_response


async def test(request):
    return json_response(data={'status': 'ok'}, status=200)


async def compare_images(request):
    data = await request.post()
    first_image = data['image1']
    second_image = data['image2']
    first_filename = first_image.filename
    second_filename = second_image.filename
    first_data = first_image.file.read()
    second_data = second_image.file.read()
    # image = data['image'].file
    # file = image.read()
    with open(first_filename, 'wb') as f:
        f.write(first_data)
    with open(second_filename, 'wb') as f:
        f.write(second_data)

    first_face_descriptor = process_iamge(first_filename)
    second_face_descriptor = process_iamge(second_filename)
    a = distance.euclidean(first_face_descriptor, second_face_descriptor)
    if a < 0.6:
        res = "Same"
    else:
        res = "Other"
    return json_response(data={'status': 'ok', 'data': res, 'distance': a}, status=200)


def process_iamge(filename):
    sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    detector = dlib.get_frontal_face_detector()
    img = io.imread(filename)
    dets = detector(img, 1)

    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
    shape = sp(img, d)

    face_descriptor = facerec.compute_face_descriptor(img, shape)

    return face_descriptor

