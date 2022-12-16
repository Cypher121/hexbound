import json
import os
from distutils.dir_util import copy_tree
from sys import argv
import datetime


def iso_now():
    return datetime.datetime.now().replace(microsecond=0).isoformat()


def get_versions_or_default():
    if os.path.exists('versions.json'):
        with open('versions.json', 'r') as fh:
            return json.load(fh)
    else:
        return {
            'latest': 'latest/docs.json',
            'latestPublished': iso_now(),
            'versions': []
        }


def update_version(version_name: str):
    copy_tree('latest', version_name)

    versions = get_versions_or_default()

    version_file = f'{version_name}/docs.json'

    if all(v.id != version_name for v in versions['versions']):
        versions['versions'].append(
            {
                'id': version_name,
                'published': iso_now(),
                'path': version_file
            }
        )

    versions['versions'] = sorted(versions['versions'], key=lambda v: v['id'], reverse=True)

    with open('versions.json', 'w+') as fh:
        json.dump(versions, fh)


def update_latest():
    versions = get_versions_or_default()
    versions['latestPublished'] = iso_now()

    with open('versions.json', 'w+') as fh:
        json.dump(versions, fh)


if __name__ == '__main__':
    if argv[1] == 'ref':
        update_version(argv[2].replace('refs/tags/v', ''))
    elif argv[1] == 'version':
        update_version(argv[2])
    elif argv[1] == 'latest':
        update_latest()
    else:
        raise Exception(f'Unknown version type: {argv[1]}')
