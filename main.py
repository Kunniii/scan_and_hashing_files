from os.path import exists, join
from os import name, walk
import hashlib
from time import time
from json import dumps

time_start = time()

available_drives = []
file_paths = []

def get_available_drives():
    global available_drives
    for n in range(ord('D'), ord('D')+1):
        drive = chr(n)+":\\"
        if (exists(drive)):
            available_drives.append(drive)

def hash_file(file_path, algorithm='sha256'):
    hash_obj = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        while chunk := f.read(1024):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

if name == "nt":
    get_available_drives()

print(f"[ + ] Found {len(available_drives)} drives")

for drive in available_drives:
    for root, sub_folder, files in walk(drive):
        for file_name in files:
            path = join(root, file_name)
            print(f"[ - ] Scanning: {path[:20]}...{path[-20:]}", end='\r')
            file_paths.append(path)
    print()

print(f"[ + ] Found {len(file_paths)} files.")

print(f"[ + ] Hashing file...")

path_with_hash = []

for path in file_paths:
    try:
        print(f"[ - ] Hashing: {path[:20]}...{path[-20:]}", end='\r')
        current_object = {
            "path": path,
            "hash": hash_file(path)
        }
        path_with_hash.append(current_object)
    except:
        ...

with open("output.json", 'w+', encoding='utf-8') as f:
    dumps(path_with_hash, indent=2, ensure_ascii=True)

print(f"\n\n>> 🟢 Completed in {(time() - time_start):.2f} ms")
