import os
 
current_dir = os.path.dirname(os.path.abspath(__file__))
total_size = 0
 
for dirpath, dirnames, filenames in os.walk(current_dir):
 
    files_paths = (os.path.join(dirpath, file) for file in filenames)
    files_size = sum(os.path.getsize(path) for path in files_paths)
 
    print("{0}のファイル合計サイズ:{1}".format(dirpath, files_size))
 
    total_size += files_size
 
print("全ての合計", total_size)