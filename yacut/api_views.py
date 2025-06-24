from flask import jsonify, request

from . import app
from .error_handlers import (APIException, NotFound, ShortIDException,
                             UnexpectedBehavior)
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def cerate_short_id():
    data = request.get_json(silent=True)
    if not data:
        raise APIException('Отсутствует тело запроса')
    if 'url' not in data:
        raise APIException('\"url\" является обязательным полем!')
    short = data.get('custom_id', None)
    try:
        url_map = URLMap.create(original=data['url'], short=short)
    except ShortIDException as error:
        raise APIException(error.args[0])
    except UnexpectedBehavior:
        raise APIException('Что-то пошло не так...', 500)
    return jsonify(
        {'url': url_map.original,
         'short_link': f'{request.url_root}{url_map.short}'}
    ), 201


@app.route('/api/id/<string:short_id>/')
def get_full_url(short_id):
    try:
        url_map = URLMap.retrieve_by_short_id(short_id)
    except NotFound as error:
        raise APIException(error.args[0], 404)
    return jsonify({'url': url_map.original}), 200
