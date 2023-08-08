import os
import time
import json
import pickle
import hashlib
import logging

logging.basicConfig(
    level=logging.WARNING,
    filename="work.log",
    format="%(levelname)s - - %(asctime)s - %(message)s",
)
time_start = time.time()

logging.info("Starting job")

available_drives = []
file_paths = []


def get_available_drives():
    global available_drives
    for n in range(ord("A"), ord("Z") + 1):
        drive = chr(n) + ":\\"
        if os.path.exists(drive):
            available_drives.append(drive)


def hash_file(file_path, algorithm="sha256"):
    logging.info(f"Hashing {file_path}")
    hash_obj = hashlib.new(algorithm)
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(1024):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        logging.warning(f"{str(e)}")


if os.name == "nt":
    get_available_drives()
else:
    available_drives = ["/"]

logging.info("Discovering all files")

for drive in available_drives:
    for root, sub_folder, files in os.walk(drive):
        if "$" in root:
            continue
        for file_name in files:
            path = os.path.join(root, file_name)
            file_paths.append(path)

logging.info(f"Found {len(file_paths)} files")

path_with_hash = []

for path in file_paths:
    c_index = file_paths.index(path) + 1
    file_hash = hash_file(path)
    current_object = {"path": path, "hash": file_hash}
    path_with_hash.append(current_object)

with open("file_paths.pickle", "wb+") as f:
    pickle.dump(file_paths, file=f)

with open("path_with_hash.pickle", "wb+") as f:
    pickle.dump(path_with_hash, file=f)

with open("output.json", "w+", encoding="utf-8") as f:
    print(json.dumps(path_with_hash, indent=2, ensure_ascii=True), file=f)

logging.info("Completed in {(time.time() - time_start):.2f} ms")
