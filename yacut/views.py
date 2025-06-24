import aiohttp
from flask import Response, abort, flash, redirect, render_template, request
from urllib.parse import parse_qs, urlparse

from . import app
from .error_handlers import NotFound, ShortIDException, UnexpectedBehavior
from .forms import UploadForm, URLForm
from .models import URLMap
from .settings import SHORT_ID_MAX_LENGTH
from .yandex_disk import upload_multiple_files


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short = form.custom_id.data or None
        try:
            url_map = URLMap.create(
                original=form.original_link.data, short=short
            )
        except ShortIDException as error:
            flash(error, 'error')
        except UnexpectedBehavior:
            abort(500)
        else:
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
            URLMap.create(original=item['download_link']) for item in uploaded
        ]
        names = [item['filename'] for item in uploaded]
        links = [f'{request.url_root}{obj.short}' for obj in url_maps]
        for item in zip(names, links):
            flash(item, 'info')
    return render_template('upload.html', form=form)


@app.route(f'/<re("[A-Za-z0-9]{{1,{SHORT_ID_MAX_LENGTH}}}"):short_id>')
async def short_link_redirect_view(short_id):
    try:
        url_map = URLMap.retrieve_by_short_id(short=short_id)
    except NotFound:
        abort(404)
    if url_map.original.startswith('https://downloader.disk.yandex.ru'):
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
                        f'attachment; filename="{filename}"'
                    }
        except aiohttp.ClientResponseError:
            abort(500)
        return Response(content, headers=headers)
    return redirect(url_map.original)
