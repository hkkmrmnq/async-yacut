from flask import jsonify, request

from . import app, db
from .error_handlers import APIException
from .models import URLMap
from .validators import valid_short_id
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def cerate_short_id():
    data = request.get_json(silent=True)
    if not data:
        raise APIException('Отсутствует тело запроса')
    if 'url' not in data:
        raise APIException('\"url\" является обязательным полем!')
    if 'custom_id' in data and data['custom_id']:
        if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            raise APIException(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        if valid_short_id(data['custom_id']):
            short_id = data['custom_id']
        else:
            raise APIException('Указано недопустимое имя для короткой ссылки')
    else:
        short_id = get_unique_short_id()
    url_map = URLMap(original=data['url'], short=short_id)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(
        {'url': url_map.original,
         'short_link': f'{request.url_root}{url_map.short}'}
    ), 201


@app.route('/api/id/<string:short_id>/')
def get_full_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise APIException('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
