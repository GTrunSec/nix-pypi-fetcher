import json
import os
import shutil
from hashlib import sha256

import db

target_dir = "./pypi"


def split_into_buckets(d: dict) -> dict:
    buckets = {}
    hexdigits = "0123456789abcdef"
    for a in hexdigits:
        for b in hexdigits:
            buckets[a+b] = {}
    for key, val in d.items():
        bucket = sha256(key.encode()).hexdigest()[:2]
        buckets[bucket][key] = val
    return buckets


def dump_json_buckets(buckets_dict: dict):
    if os.path.isdir(target_dir):
        shutil.rmtree(target_dir)
    os.mkdir(target_dir)
    for bucket, dic in buckets_dict.items():
        with open(f"{target_dir}/{bucket}.json", 'w') as f:
            json.dump(dic, f, indent=2)


def find_favorite_format(sdist_releases, f_types):
    ok_releases = []
    for sdist_rel in sdist_releases:
        for t in f_types:
            if sdist_rel['filename'].endswith(t):
                ok_releases.append(sdist_rel)
    for t in f_types:
        releases_with_type = [rel for rel in sdist_releases if rel['filename'].endswith(t)]
        if releases_with_type:
            return min(releases_with_type, key=lambda release: len(release['filename']))
    return None


def main():
    nix_dict = {}
    pkgs = db.Package.select()
    for pkg in pkgs:
        name = pkg.name.replace('_', '-').lower()
        meta = json.loads(pkg.metadata)
        releases_dict = {}
        # iterate over versions of current package
        for release_ver, release in meta['releases'].items():
            f_types = ('tar.gz', '.tgz', '.zip', '.tar.bz2')
            sdist_releases = [f for f in release if f['packagetype'] == "sdist"]
            if sdist_releases:
                src_release = find_favorite_format(sdist_releases, f_types)
                if src_release:
                    releases_dict[release_ver] = dict(
                        sha256=src_release['digests']['sha256'],
                        url=src_release['url'].replace('https://files.pythonhosted.org/packages/', '')
                    )
        if releases_dict:
            nix_dict[name] = releases_dict
    with open("pypi.json", 'w') as f:
        json.dump(nix_dict, f, indent=2)
    dump_json_buckets(split_into_buckets(nix_dict))


if __name__ == "__main__":
    main()
