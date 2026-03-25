import os
import aiohttp
import json
from pathlib import Path

SAUCENAO_ENDPOINT = 'https://saucenao.com/search.php'


async def search_saucenao(image_path: str, api_key: str, numres: int = 5):
    """Search image via SauceNAO API.

    Returns a list of results. Each result is a dict with keys:
      - similarity (str)
      - thumbnail (str)
      - index_name (str)
      - ext_urls (list)
      - title (optional)

    Raises ValueError if response indicates an error.
    """
    if not api_key:
        raise ValueError('SAUCENAO_API_KEY is required')

    params = {
        'output_type': 2,
        'api_key': api_key,
        'numres': numres,
    }

    file_path = Path(image_path)
    if not file_path.exists():
        raise ValueError('image not found')

    data = None
    async with aiohttp.ClientSession() as session:
        with file_path.open('rb') as fh:
            form = aiohttp.FormData()
            for k, v in params.items():
                form.add_field(k, str(v))
            form.add_field('file', fh, filename=file_path.name, content_type='image/jpeg')

            async with session.post(SAUCENAO_ENDPOINT, data=form, timeout=60) as resp:
                text = await resp.text()
                try:
                    data = json.loads(text)
                except Exception:
                    raise ValueError(f'Invalid response from SauceNAO: {resp.status}')

    header = data.get('header', {})
    status = header.get('status')
    if status is None:
        # normal case: results provided
        pass
    else:
        # status may be 0 for OK
        if status != 0:
            raise ValueError(f'SauceNAO error: {header}')

    results = []
    for item in data.get('results', [])[:numres]:
        h = item.get('header', {})
        d = item.get('data', {})
        res = {
            'similarity': h.get('similarity'),
            'thumbnail': h.get('thumbnail'),
            'index_name': h.get('index_name'),
            'ext_urls': d.get('ext_urls', []) if isinstance(d.get('ext_urls', []), list) else [],
            'title': d.get('title') or d.get('source') or d.get('material'),
        }
        results.append(res)

    return results


__all__ = ['search_saucenao']
