import os
import shutil
from tqdm import tqdm

src  = ""
dest = ""

os.makedirs(dest, exist_ok=True)

all_files = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]

for file in tqdm(all_files):
    src_path  = os.path.join(src, file)
    dest_path = os.path.join(dest, file)

    shutil.copy(src_path, dest_path)