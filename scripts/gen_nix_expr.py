import json
import os
import shutil
from hashlib import sha256

import db

target_dir = "./pypi"


def dict_to_nix(d: dict) -> str:
    return json.dumps(d, indent=2, sort_keys=True)\
        .replace(" '", ' "') \
        .replace("';", '";') \
        .replace("'\n", '"\n') \
        .replace('":', '" = ')\
        .replace('"\n', '";\n') \
        .replace(',', ';') \
        .replace('}\n', '};\n')


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


def dump_to_nix_expr(bucket_dict: dict):
    if os.path.isdir(target_dir):
        shutil.rmtree(target_dir)
    os.mkdir(target_dir)
    for bucket, dic in bucket_dict.items():
        with open(f"{target_dir}/{bucket}.nix", 'w') as f:
            f.write(dict_to_nix(dic))


def release_name_len(sdist_release):
    return len(sdist_release['filename'])


def find_favorite_archive(sdist_releases, f_types):
    ok_releases = []
    for sdist_rel in sdist_releases:
        for t in f_types:
            if sdist_rel['filename'].endswith(t):
                ok_releases.append(sdist_rel)
    for t in f_types:
        releases_with_type = [rel for rel in sdist_releases if rel['filename'].endswith(t)]
        if releases_with_type:
            return min(releases_with_type, key=release_name_len)
    return None


def main():
    nix_dict = {}
    pkgs = db.Package.select()
    for pkg in pkgs:
        name = pkg.name.lower()
        meta = json.loads(pkg.metadata)
        releases_dict = {}
        # iterate over versions of current package
        for release_ver, release in meta['releases'].items():
            f_types = ('tar.gz', '.tgz', '.zip', '.tar.bz2')
            sdist_releases = [f for f in release if f['packagetype'] == "sdist"]
            if sdist_releases:
                src_release = find_favorite_archive(sdist_releases, f_types)
                if src_release:
                    releases_dict[release_ver] = dict(
                        sha256=src_release['digests']['sha256'],
                        url=src_release['url']
                    )
        if releases_dict:
            nix_dict[name] = releases_dict
    with open("pypi.json", 'w') as f:
        json.dump(nix_dict, f, indent=2)
    dump_to_nix_expr(split_into_buckets(nix_dict))


if __name__ == "__main__":
    main()
