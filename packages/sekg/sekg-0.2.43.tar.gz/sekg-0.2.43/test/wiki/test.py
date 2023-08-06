#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import time
import aiohttp
import async_timeout
import pickle
from pathlib import Path
import json
import sys

# if sys.platform == 'win32':
#     loop = asyncio.ProactorEventLoop()
#     asyncio.set_event_loop(loop)

# import wikipedia


class AyncWikiSearcher:

    API_URL = 'http://en.wikipedia.org/w/api.php'

    def __init__(self, cache=None, proxy_server=None, pool_size=128, stride=60):
        self.proxy_server = proxy_server
        self.semaphore = asyncio.Semaphore(pool_size)
        self.cache = {} if cache is None else cache
        self.stride = stride
        self.cache_size = 0

    async def __fetch(self, title, limit=5):
        if title in self.cache:
            return self.cache[title]
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srprop': '',
            'srlimit': limit,
            'srsearch': title

        }
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession() as session:
                    with async_timeout.timeout(10):
                        async with session.get(self.API_URL, params=params, proxy=self.proxy_server) as response:
                            d = await response.json()
                            result = [{"pageid": item["pageid"], "title": item["title"]} for item in d["query"]["search"]]
                            self.cache[title] = result
                            print("[Done] title: ", title)
                            return result
        except Exception as e:
            print("[Failed] title: {}, err: {}".format(title, e))
            return []

    async def __summary(self, item, limit=5):
        params = {
            'prop': 'extracts',
            'explaintext': '',
            'titles': item['title'],
            'exsentences': 5,
            'format': 'json',
            'action': 'query'
        }
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession() as session:
                    with async_timeout.timeout(10):
                        async with session.get(self.API_URL, params=params, proxy=self.proxy_server) as response:
                            d = await response.json()
                            s = d['query']['pages'][str(item['pageid'])]['extract']
                            item['summary'] = s
                            return s
        except Exception as e:
            return ""

    def save(self, save_path):
        print("Save...")
        with Path(save_path).open("wb") as f:
            pickle.dump(self.cache, f)

    def search(self, titles, save_path="cache.bin"):
        titles = list(titles)
        loop = asyncio.get_event_loop()
        tasks = [self.__fetch(title) for title in titles]
        loop.run_until_complete(asyncio.gather(*tasks))
        self.save(save_path)
        return self.cache

    def summary(self, save_path="cache.bin"):
        loop = asyncio.get_event_loop()
        tasks = [self.__summary(item) for v in self.cache.values() for item in v]
        loop.run_until_complete(asyncio.gather(*tasks))
        self.save(save_path)
        return self.cache


if __name__ == '__main__':
    searcher = AyncWikiSearcher(proxy_server="http://127.0.0.1:1080")
    start = time.time()
    with Path("terms.txt").open("r", encoding="utf-8") as f:
        terms = [line.strip() for line in f]
    result = searcher.search(terms)
    result = searcher.summary()
    end = time.time()
    print("cost time:", end - start)
    with Path("result.json").open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    # with Path("cache.bin").open("rb") as f:
    #     cache = pickle.load(f)
    # with Path("cache.json").open("w", encoding="utf-8") as f:
    #     json.dump(cache, f, indent=4)
    # start = time.time()
    # for i in range(100):
    #     wikipedia.search('apple{}'.format(i))
    # end = time.time()
    # print("cost time:", end - start)


# try:
#     apple = wikipedia.page("CNN (disambiguation)")
#     print(apple.content.encode("UTF8"))
# except Exception:
#     pass

# print(wikipedia.summary(res[1]))

# with Path("apple.wiki").open("wb") as f:
#     pickle.dump(apple, f)

# with Path("apple.wiki").open("rb") as f:
#     apple = pickle.load(f)

# print(apple.content.encode("UTF8"))
