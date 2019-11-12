from aiohttp.web import json_response


def test(request):
    return json_response(data={'status': 'ok'}, status=200)
