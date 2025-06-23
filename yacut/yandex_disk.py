import asyncio
import urllib

import aiohttp
from werkzeug.datastructures import FileStorage

from .settings import AUTH_HEADERS, DOWNLOAD_LINK_URL, REQUEST_UPLOAD_URL


async def _get_upload_link(
        session: aiohttp.ClientSession, filename: str
) -> str:
    # flake8: noqa: <CODE>
    payload = {'path': f'app:/{filename}', 'overwrite': 'True'}
    async with session.get(
        headers=AUTH_HEADERS,
        params=payload,
        url=REQUEST_UPLOAD_URL
    ) as response:
        data = await response.json()
        return data['href']


async def _upload_file(
        session: aiohttp.ClientSession, file: FileStorage, upload_url: str
) -> str:
    file_data = file.read()
    async with session.put(
        data=file_data,
        url=upload_url,
    ) as response:
        location = response.headers['Location']
        location = urllib.parse.unquote(location)
        return location.replace('/disk', '')


async def _get_download_link(
        session: aiohttp.ClientSession, location: str
) -> str:
    async with session.get(
        headers=AUTH_HEADERS,
        url=DOWNLOAD_LINK_URL,
        params={'path': f'{location}'}
    ) as response:
        data = await response.json()
        return data['href']


async def upload_one_file(
        session: aiohttp.ClientSession, file_data: FileStorage
) -> dict[str, str]:
    upload_url = await _get_upload_link(session, file_data.filename)
    location = await _upload_file(session, file_data, upload_url)
    download_link = await _get_download_link(session, location)
    result = {'filename': file_data.filename, 'download_link': download_link}
    return result


async def upload_multiple_files(
        files_data: list[FileStorage]
) -> list[dict[str, str]]:
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        tasks = [upload_one_file(session, file) for file in files_data]
        results = await asyncio.gather(*tasks)
    return results
