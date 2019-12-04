# coding: utf-8
from pathlib import Path

l={}

class Item():
    def __init__(self, path, name, type, size):
        self.path=path
        self.name=name
        self.type=type
        self.size=size
    
    def __str__(self):
        return ",".join([self.path, self.name, self.type, self.size])

    def add_size(self, size):
        self.size+=size

def down(path, folder):
    #print("down: " + str(folder))
    l[str(folder)]=Item(path, str(folder), "folder", 0)

def up(folder):
    #print("up: " + str(folder))
    if str(folder) in l:
        item=l[str(folder)]
        item.add_size(0)
    else:
        print(str(folder))

def search_files(path):
    p = Path(path)

    # 指定されたパス以下のファイルを再帰的にチェックする
    for file in p.iterdir():
        if file.is_dir(): # フォルダのケース
            # 子フォルダへ
            down(path, file)
            search_files(file)
        elif file.is_file(): # ファイルのケース
            # resolve() を使って絶対パスを表示する
            print('{:}\t{}'.format(file.stat().st_size, file.resolve()))
    
    # フォルダ内の探索が終わり親フォルダへ
    up(p.parent)

if __name__ == '__main__':
    # hayato のデスクトップ以下にあるサイズが 1MB 以上のファイルを表示する
    path = ''
    search_files(path)
    print(l)