import random
import string

import aiohttp
from flask import Response, abort, flash, redirect, render_template, request
from urllib.parse import parse_qs, urlparse

from . import app, db
from .forms import UploadForm, URLForm
from .models import URLMap
from .settings import MAX_RETRY_FOR_SHORT_ID_GENERATION, SHORT_URL_ID_LENGTH
from .validators import valid_short_id
from .yandex_disk import upload_multiple_files

CHARACTERS = string.ascii_letters + string.digits


def short_id_available(short_id: str) -> bool:
    """Проверяет, что код для новой короткой ссылки не занят"""
    if URLMap.query.filter_by(short=short_id).first() is None:
        return True
    return False


def get_unique_short_id():
    """Генерирует идентификатор для коротких ссылок."""
    for _ in range(MAX_RETRY_FOR_SHORT_ID_GENERATION):
        short_id = "".join(random.choices(CHARACTERS, k=SHORT_URL_ID_LENGTH))
        if short_id_available(short_id):
            return short_id
    abort(500)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        if form.custom_id.data:
            short_id = form.custom_id.data
            if not valid_short_id(short_id):
                flash('Указано недопустимое имя для короткой ссылки', 'error')
                return render_template('index.html', form=form)
            elif short_id == 'files' or not short_id_available(short_id):
                flash('Предложенный вариант короткой ссылки уже существует.',
                      'error')
                return render_template('index.html', form=form)
        else:
            short_id = get_unique_short_id()
        url_map = URLMap(original=form.original_link.data, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        flash('Ваша новая ссылка готова:', 'info')
        flash(f'{request.url_root}{url_map.short}', 'url')
    return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def upload_view():
    form = UploadForm()
    if form.validate_on_submit():
        try:
            uploaded = await upload_multiple_files(form.files.data)
        except aiohttp.ClientResponseError:
            abort(500)
        url_maps = [
            URLMap(
                original=item['download_link'], short=get_unique_short_id()
            ) for item in uploaded
        ]
        db.session.add_all(url_maps)
        db.session.commit()
        names = [item['filename'] for item in uploaded]
        links = [f'{request.url_root}{obj.short}' for obj in url_maps]
        for item in zip(names, links):
            flash(item, 'info')
    return render_template('upload.html', form=form)


@app.route('/<re("[A-Za-z0-9]{1,16}"):short_id>')
async def short_link_redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is not None:
        if url_map.original.startswith('https://downloader.disk.yandex.ru'):
            # не пускает после редиректа
            parsed_url = urlparse(url_map.original)
            query_params = parse_qs(parsed_url.query)
            filename = query_params.get('filename', [f'{short_id}.bin'])[0]
            try:
                async with aiohttp.ClientSession(
                    raise_for_status=True
                ) as session:
                    async with session.get(url_map.original) as response:
                        content = await response.read()
                        headers = {
                            'Content-Type':
                            response.headers.get(
                                'Content-Type', 'application/octet-stream'
                            ),
                            'Content-Disposition':
                            'attachment; '
                            f'filename="{filename}"'
                        }
            except aiohttp.ClientResponseError:
                abort(500)
            return Response(content, headers=headers)
        return redirect(url_map.original)
    abort(404)
