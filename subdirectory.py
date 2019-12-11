# coding: utf-8
from pathlib import Path
import argparse
#import unicodecsv as csv
import csv
import datetime
import re

class Item():
    rule_check=False
    def __init__(self, path, name, level, type, size, file_count):
        self.path=path
        self.name=name
        self.level=level
        self.type=type
        self.total_size=size
        self.total_file_count=file_count
        self.error_info=[]
    
    @classmethod
    def head(cls):
        ret=""
        if Item.rule_check:
            ret=["Path", "Name", "Type", "Level", "Total_size", "Total_file_count", "Error_info"]
        else:
            ret=["Path", "Name", "Type", "Level", "Total_size", "Total_file_count"]
        return ret
    
    def __str__(self):
        ret=""
        if Item.rule_check:
            ret=",".join([str(self.path), str(self.name), str(self.type), str(self.level), str(self.total_size), str(self.total_file_count), str(self.error_info)])
        else:
            ret=",".join([str(self.path), str(self.name), str(self.type), str(self.level), str(self.total_size), str(self.total_file_count)])
        return ret

    def list(self):
        ret=""
        if Item.rule_check:
            ret=[str(self.path), str(self.name), str(self.type), str(self.level), str(self.total_size), str(self.total_file_count), str(self.error_info)]
        else:
            ret=[str(self.path), str(self.name), str(self.type), str(self.level), str(self.total_size), str(self.total_file_count)]            
        return ret

    def add_total_size(self, size):
        self.total_size+=size
    
    def add_total_file_count(self, file_count):
        self.total_file_count+=file_count

    # Characters that aren't allowed in file and folder names  in OneDrive, OneDrive for Business on Office 365, and SharePoint Online
    # https://support.office.com/en-us/article/invalid-file-names-and-file-types-in-onedrive-onedrive-for-business-and-sharepoint-64883a5d-228e-48f5-b3d2-eb39e07630fa?omkt=en-US&ui=en-US&rs=en-US&ad=US
    def check_rule(self): 
        # return if the rule_check is false
        if not Item.rule_check:
            return

        # except for a extension if the type is file
        name=""
        if self.type=="folder":
            name=self.name
        elif self.type=="file":
            p=Path(str(self.path)+"\\"+self.name)
            name=p.stem 

        # check file name
        is_invalid=False
        for c in r"\"*:<>?/\|.": 
            if c in name:
                is_invalid=True
        if is_invalid:
            self.error_info.append("INVALID_NAME")

def folder_found(folder, l, level):
    l[str(folder)]=Item(folder.parent, str(folder.name), level, "folder", 0, 0)

def file_found(file, l, level):
    l[str(file.resolve())]=Item(file.parent, str(file.name), level, "file", file.stat().st_size, 0)

def goto_parent_folder(folder, l):
    # get total size and file count undor the folder
    total_size=0
    total_file_count=0
    for file in folder.iterdir():
        total_size+=l[str(file)].total_size
        if file.is_dir():  
            total_file_count+=l[str(file)].total_file_count
        elif file.is_file():
            total_file_count+=1

    item=l[str(folder)]
    item.add_total_size(total_size)
    item.add_total_file_count(total_file_count)

def look_into_the_folder(path, l, level):
    try:
        p = Path(path)
        folder_found(p, l, level)
        if(level==1):
            print("Search start: " + str(path))

        # recursive search
        for file in p.iterdir():
            if file.is_dir():
                look_into_the_folder(file, l, level+1)
            elif file.is_file():
                file_found(file, l, level+1)
        
        # after search in this path
        goto_parent_folder(p, l)
    except Exception as e:
        print("error: {e}, path: {path}".format(e=e, item=path))

if __name__ == '__main__':
    # get args
    parser = argparse.ArgumentParser(description="This program looks into the folder. And then, it outputs a csv file that include folder info and file info.")
    parser.add_argument("--path", help="Specify the path that you want to look into. If it's not specified, this program will look into the current path")
    parser.add_argument("--check_rule", action='store_true')
    args = parser.parse_args()

    # set init path
    path=""
    if args.path:
        path=Path(args.path)
    else:
        path=Path.cwd()

    # set check flag
    Item.rule_check=args.check_rule

    # start search
    l={}
    look_into_the_folder(path, l, 0)
    
    # output a csv file
    now = datetime.datetime.now()
    filename = './result_' + now.strftime('%Y%m%d_%H%M%S') + '.csv'
    with open(filename, "w", newline="", encoding='utf-8-sig') as f:
        writer=csv.writer(f)
        writer.writerow(Item.head())
        for item in l.values():
            try:
                item.check_rule()
                writer.writerow(item.list())
            except Exception as e:
                print("error: {e}, item: {item}".format(e=e, item=item))