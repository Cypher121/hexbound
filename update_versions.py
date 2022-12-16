import json
import os
from distutils.dir_util import copy_tree
from sys import argv


def update_version(version_name: str):
    copy_tree('latest', version_name)

    if os.path.exists('versions.json'):
        with open('versions.json', 'r') as fh:
            versions = json.load(fh)
    else:
        versions = {
            'latest': 'latest/docs.json',
            'versions': []
        }

    version_file = f'{version_name}/docs.json'

    if version_file not in versions['versions']:
        versions['versions'].append(version_file)

    with open('versions.json', 'w') as fh:
        json.dump(versions, fh)


if __name__ == '__main__':
    if argv[1] == 'ref':
        version = argv[2].replace('refs/tags/', '')
    elif argv[1] == 'version':
        version = argv[2]
    else:
        raise Exception(f'Unknown version type: {argv[1]}')

    update_version(version)
