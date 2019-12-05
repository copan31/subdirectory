# coding: utf-8
from pathlib import Path
import csv

class Item():
    def __init__(self, path, name, level, type, total_size, total_file_count):
        self.path=path
        self.name=name
        self.level=level
        self.type=type
        self.total_size=total_size
        self.total_file_count=total_file_count
    
    @classmethod
    def head(cls):
        return ["パス", "名称", "タイプ", "階層", "総サイズ", "総ファイル数"]
    
    def __str__(self):
        return ",".join([str(self.path), str(self.name), str(self.type), str(self.level), str(self.total_size), str(self.total_file_count)])

    def list(self):
        return [str(self.path), str(self.name), str(self.type), str(self.level), str(self.total_size), str(self.total_file_count)]

    def add_total_size(self, total_size):
        self.total_size+=total_size
    
    def add_total_file_count(self, total_file_count):
        self.total_file_count+=total_file_count

def find_folder(folder, l, level):
    #print("down: " + str(folder))
    l[str(folder)]=Item(folder.parent, str(folder.name), level, "folder", 0, 0)

def find_file(file, l, level):
    l[str(file.resolve())]=Item(file.parent, str(file.name), level, "file", file.stat().st_size, 0)

def goto_parent_folder(folder, l):
    # フォルダ内のファイル、フォルダのsizeを合計する。
    total_size=0
    total_file_count=0
    for file in folder.iterdir():
        total_size+=l[str(file)].total_size
        if file.is_dir():  
            total_file_count+=l[str(file)].total_file_count
        elif file.is_file():
            total_file_count+=1

    # 合計値をフォルダのサイズに加算する。
    l[str(folder)].add_total_size(total_size)
    # 合計値をフォルダのファイル数に加算する。
    l[str(folder)].add_total_file_count(total_file_count)

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