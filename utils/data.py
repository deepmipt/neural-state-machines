import os

import requests
from tqdm import tqdm


def download(dest, source):
    datapath = os.path.dirname(dest)
    os.makedirs(datapath, mode=0o755, exist_ok=True)

    dest = os.path.abspath(dest)

    r = requests.get(source, stream=True)
    total_length = int(r.headers.get('content-length', 0))

    with open(dest, 'wb') as f:
        # print('Downloading to {}'.format(dest))

        pbar = tqdm(total=total_length, unit='B', unit_scale=True)
        for chunk in r.iter_content(chunk_size=32 * 1024):
            if chunk:  # filter out keep-alive new chunks
                pbar.update(len(chunk))
                f.write(chunk)


_mark_name = '.done'


def mark_done(path):
    fname = os.path.join(path, _mark_name)
    with open(fname, 'a'):
        os.utime(fname, None)


def is_done(path):
    return os.path.isfile(os.path.join(path, _mark_name))
