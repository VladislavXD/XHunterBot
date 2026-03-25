import json
import aiohttp
import asyncio
from pathlib import Path


async def check_site(session, username, site):
    url_check = site.get("uri_check") or site.get("url")
    if not url_check:
        return None
        
    url_pretty = site.get("uri_pretty", url_check)
    url_check = url_check.replace("{account}", username)
    url_pretty = url_pretty.replace("{account}", username)

    headers = site.get("headers", {"User-Agent": "Mozilla/5.0"})

    try:
        async with session.get(url_check, headers=headers, timeout=30) as r:
            text = await r.text()

            # проверка
            if "e_code" in site and r.status == site["e_code"] and site.get("e_string", "") in text:
                return (site["name"], url_pretty)

            elif r.status == 200:
                return (site["name"], url_pretty)

    except:
        return None

async def search_wmn(username):
    # Надёжный путь к файлу данных относительно этого модуля
    data_path = Path(__file__).resolve().parent / "OSINTS" / "data" / "wmn-data.json"
    if not data_path.exists():
        raise FileNotFoundError(f"WMN data file not found: {data_path}")

    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    async with aiohttp.ClientSession() as session:
        tasks = [check_site(session, username, site) for site in data["sites"]]
        results = await asyncio.gather(*tasks)

    return [r for r in results if r]

# запуск
if __name__ == "__main__":
    print(asyncio.run(search_wmn("elonmusk")))
