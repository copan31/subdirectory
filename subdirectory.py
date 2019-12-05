# coding: utf-8
from pathlib import Path
import argparse
import csv
import re

class Item():
    def __init__(self, path, name, level, type, size, file_count, error_info):
        self.path=path
        self.name=name
        self.level=level
        self.type=type
        self.total_size=size
        self.total_file_count=file_count
        self.error_info=error_info
    
    @classmethod
    def head(cls):
        return ["Path", "Name", "Type", "Level", "Total_size", "Total_file_count", "Error_info"]
    
    def __str__(self):
        return ",".join([str(self.path), str(self.name), str(self.type), str(self.level), str(self.total_size), str(self.total_file_count), str(self.error_info)])

    def list(self):
        return [str(self.path), str(self.name), str(self.type), str(self.level), str(self.total_size), str(self.total_file_count), str(self.error_info)]

    def add_total_size(self, size):
        self.total_size+=size
    
    def add_total_file_count(self, file_count):
        self.total_file_count+=file_count

def check_folder_name(folder):
    is_invalid=False
    for c in r"~\"#%&*:<>?/\{|}.":
        if c in folder.name:
            is_invalid=True
    
    if is_invalid:
        return "INVALID_NAME"
    else:
        return "NONE"

def check_file_name(file):
    # check for the file name except for the file extension
    is_invalid=False
    for c in r"~\"#%&*:<>?/\{|}.":
        if c in file.stem:
            is_invalid=True
    if is_invalid:
        return "INVALID_NAME"
    
    for c in r"":
        if c in file.suffix:
            is_invalid=True
    if is_invalid:
        return "iNVALID_EXTENSION"

    return "NONE"

def find_folder(folder, l, level):
    l[str(folder)]=Item(folder.parent, str(folder.name), level, "folder", 0, 0, check_folder_name(folder))

def find_file(file, l, level):
    l[str(file.resolve())]=Item(file.parent, str(file.name), level, "file", file.stat().st_size, 0, check_file_name(file))

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

def look_into_the_folder(path, l, level):
    p = Path(path)
    find_folder(p, l, level)

    # 指定されたパス以下のファイルを再帰的にチェックする
    for file in p.iterdir():
        if file.is_dir(): # フォルダのケース
            # 子フォルダへ
            look_into_the_folder(file, l, level+1)
        elif file.is_file(): # ファイルのケース
            find_file(file, l, level+1)
    
    # フォルダ内の探索が終わり親フォルダへ
    goto_parent_folder(p, l)

def subdirecory(path):
    l={}
    look_into_the_folder(path, l, 0)
    
    # output a csv file
    with open("result.csv", "w", newline="") as f:
        writer=csv.writer(f)
        writer.writerow(Item.head())
        for item in l.values():
            writer.writerow(item.list())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This program looks into the folder. And then, it outputs a csv file that include folder info and file info.")
    parser.add_argument("--path", help="Specify the path that you want to look into. If it's not specified, this program will look into the current path")
    args = parser.parse_args()

    path=""
    if args.path:
        path=Path(args.path)
    else:
        path=Path.cwd()

    subdirecory(path)