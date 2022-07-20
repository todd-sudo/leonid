import asyncio
import json
import time
from datetime import datetime

import aiohttp


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko"
}
proxy = "http://127.0.0.1:8080"

file = open("src/data/net/data.json")
search_data = json.load(file)


async def find_username(username: str) -> dict:
    start_time = time.time()
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = []
        for u in search_data["sites"]:
            task = asyncio.ensure_future(make_request(session, u, username))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        execution_time = round(time.time() - start_time, 1)
        user_json = {
            "search-params": {
                "username": username,
                "sites-number": len(search_data["sites"]),
                "date": now,
                "execution-time": execution_time,
            },
            "sites": [],
        }
        for x in results:
            user_json["sites"].append(x)
        return user_json


async def make_request(session: aiohttp.ClientSession, u: dict, username: str):
    url = u["url"].format(username=username)
    json_body = None
    metadata = None
    if "headers" in u:
        headers.update(eval(u["headers"]))
    if "json" in u:
        json_body = u["json"].format(username=username)
        json_body = json.loads(json_body)
    try:
        async with session.request(
            u["method"], url, json=json_body, headers=headers, ssl=False
        ) as response:
            if eval(u["valid"]):
                if "metadata" in u:
                    metadata = []
                    for d in u["metadata"]:
                        try:
                            value = eval(d["value"])
                            metadata.append(
                                {"type": d["type"], "key": d["key"], "value": value}
                            )
                        except Exception as e:
                            pass
                return {
                    "id": u["id"],
                    "app": u["app"],
                    "url": url,
                    "response-status": f"{response.status} {response.reason}",
                    "status": "FOUND",
                    "error-message": None,
                    "metadata": metadata,
                }
            else:
                return {
                    "id": u["id"],
                    "app": u["app"],
                    "url": url,
                    "response-status": f"{response.status} {response.reason}",
                    "status": "NOT FOUND",
                    "error-message": None,
                    "metadata": metadata,
                }
    except Exception as e:
        return {
            "id": u["id"],
            "app": u["app"],
            "url": url,
            "response-status": None,
            "status": "ERROR",
            "error-message": repr(e),
            "metadata": metadata,
        }
