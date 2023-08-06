#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import time
import aiohttp
import async_timeout

# import wikipedia


class AyncWikiSearcher:

    API_URL = 'http://en.wikipedia.org/w/api.php'

    def __init__(self, cache=None, proxy_server=None, pool_size=500):
        self.proxy_server = proxy_server
        self.semaphore = asyncio.Semaphore(pool_size)
        self.cache = {} if cache is None else cache

    async def __fetch(self, title, limit=10):
        if title in self.cache:
            return self.cache[title]
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srprop': '',
            'srlimit': limit,
            'limit': limit,
            'srsearch': title
        }
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession() as session:
                    with async_timeout.timeout(10):
                        async with session.get(self.API_URL, params=params, proxy=self.proxy_server) as response:
                            d = await response.json()
                            result = [{"pageid": ele["pageid"], "title": ele["title"]} for ele in d["query"]["search"]]
                            self.cache[title] = result
                            return result
        except Exception as e:
            print("url:", e)
            return []

    def search_titles(self, titles):
        titles = list(titles)
        loop = asyncio.get_event_loop()
        tasks = [self.__fetch(title) for title in titles]
        loop.run_until_complete(asyncio.gather(*tasks))
        return self.cache


if __name__ == '__main__':
    searcher = AyncWikiSearcher(proxy_server="http://127.0.0.1:1080")
    start = time.time()
    result = searcher.search_titles(['apple{}'.format(i) for i in range(1000)])
    end = time.time()
    print("cost time:", end - start)
    print(result)
