import asyncio
import json
import xmlrpc.client
from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep
from typing import List

import requests

import db

base_url = "https://pypi.org/pypi"


def run_in_parallel(func, args_list: List[tuple], workers=10):
    loop = asyncio.get_event_loop()
    thread_pool = ThreadPoolExecutor(max_workers=workers)
    sync_coros = []
    for args in args_list:
        sync_coros.append(
            loop.run_in_executor(thread_pool, func, *args)
        )
    return loop.run_until_complete(asyncio.gather(*sync_coros))


def all_packages():
    xmlclient = xmlrpc.client.ServerProxy(base_url)
    return xmlclient.list_packages_with_serial()


def pkg_meta(name, ident=None):
    if ident:
        print(f"fetching meta info for pkg id: {ident}, named: '{name}'")
    resp = requests.get(f"{base_url}/{name}/json")
    resp.raise_for_status()
    return resp.json()


def save_pkg_meta(name, ident=None):
    if not db.Package.select().where(db.Package.name == name).exists():
        api_success = False
        while not api_success:
            try:
                data = pkg_meta(name, ident=ident)
                api_success = True
            except:
                print("Warning! problems accessing pypi api. Will retry in 5s")
                sleep(5)
        db.Package(name=name, metadata=json.dumps(data, indent=2)).save()


def crawl_pkgs_meta(packages, workers=10):
    args_list = [(pkgs, idx) for idx, pkgs in enumerate(packages)]
    return run_in_parallel(save_pkg_meta, args_list, workers=workers)


def main():
    crawl_pkgs_meta(all_packages(), workers=30)


if __name__ == "__main__":
    main()
