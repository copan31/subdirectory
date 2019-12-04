from pathlib import Path


def print_all_file(path):
    """再帰的にiterdir()を呼び出し、全てのファイルを出力する。"""
    if path.is_dir():
        for p in path.iterdir():
            print_all_file(p)
    elif path.is_file():
        print(path.resolve())  # わかりやすいよう、絶対パスに


path = Path('')
print_all_file(path)