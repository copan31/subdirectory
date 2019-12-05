from pathlib import Path

SUFFIXES = {
    1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
    1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
}


def approximate_size(size, a_kilobyte_is_1024_bytes=True):
    """Convert a file size to human-readable form.

    http://diveintopython3-ja.rdy.jp/your-first-python-program.html

    Keyword arguments:
    size -- file size in bytes
    a_kilobyte_is_1024_bytes -- if True (default), use multiples of 1024
                                if False, use multiples of 1000

    Returns: string

    """
    if size < 0:
        raise ValueError('number must be non-negative')

    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
    for suffix in SUFFIXES[multiple]:
        size /= multiple
        if size < multiple:
            return '{0:.1f} {1}'.format(size, suffix)

    raise ValueError('number too large')


def _get_size(path_obj):
    """そのパスのサイズを返す。

    Pathオブジェクトを受け取ります。

    ファイルだった場合はそのファイルサイズを、
    ディレクトリだった場合は再帰的に取得したファイルサイズを返します。

    """
    if path_obj.is_file():
        return path_obj.stat().st_size
    elif path_obj.is_dir():
        return sum(_get_size(p) for p in path_obj.iterdir())


def get_size(target_path='.'):
    """Pathオブジェクトとサイズをyieldで返す。

    サイズを取得したいパスを与えると、中にあるパスの一覧とそれぞれのサイズを
    yieldで返します。

    """
    for path in Path(target_path).iterdir():
        size = _get_size(path)
        yield path, approximate_size(size)


if __name__ == '__main__':
    for name, size in get_size():
        print(name, size)