# coding: utf-8
from pathlib import Path
import csv

class Item():
    def __init__(self, path, name, level, type, size, file_count):
        self.path=path
        self.name=name
        self.level=level
        self.type=type
        self.size=size
        self.file_count=file_count
    
    @classmethod
    def head(cls):
        return ["path", "name", "level", "type", "size", "file_count"]
    
    def __str__(self):
        return ",".join([str(self.path), str(self.name), str(self.level), str(self.type), str(self.size), str(self.file_count)])

    def list(self):
        return [str(self.path), str(self.name), str(self.level), str(self.type), str(self.size), str(self.file_count)]

    def add_size(self, size):
        self.size+=size

def find_folder(folder, l, level):
    #print("down: " + str(folder))
    l[str(folder)]=Item(folder.parent, str(folder.name), level, "folder", 0, len([file for file in folder.iterdir()]))

def find_file(file, l, level):
    l[str(file.resolve())]=Item(file.parent, str(file.name), level, "file", file.stat().st_size, 0)

def goto_parent_folder(folder, l):
    # フォルダ内のファイル、フォルダのsizeを合計する。
    total_size=0
    for file in folder.iterdir():
        item=l[str(file)]
        total_size+=item.size

    # 合計値をフォルダのサイズに加算する。
    item=l[str(folder)].add_size(total_size)

def search_files(path, l, level):
    p = Path(path)
    find_folder(p, l, level)

    # 指定されたパス以下のファイルを再帰的にチェックする
    for file in p.iterdir():
        if file.is_dir(): # フォルダのケース
            # 子フォルダへ
            search_files(file, l, level+1)
        elif file.is_file(): # ファイルのケース
            find_file(file, l, level+1)
    
    # フォルダ内の探索が終わり親フォルダへ
    goto_parent_folder(p, l)

if __name__ == '__main__':    
    l={}
    path = Path.cwd()
    search_files(path, l, 0)
    
    with open("test.csv", "w", newline="") as f:
        writer=csv.writer(f)
        
        writer.writerow(Item.head())
        for item in l.values():
            writer.writerow(item.list())