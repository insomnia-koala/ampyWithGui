import os
import json

dirs = []
files = []

def walk(path):
    if path == "":
        #print("/")
        dirs.append("/")
    else:
        dirs.append(path)
        #print(path)
    
    rootDir = os.listdir(path)
    for index in rootDir:
        if os.stat(path + "/" + index)[0] == 16384:
            walk(path + "/" + index)
        else:
            #(path + "/" + index)
            files.append(path + "/" + index)


if __name__ == "__main__":
    walk("")
    print(json.dumps(dirs))
    print(json.dumps(files))