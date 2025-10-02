import os
import random
import shutil
from tqdm import tqdm


def move_all(src, dest):
    # Get file list from src
    all_files = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]

    for file in tqdm(all_files):
        src_path = os.path.join(src, file)
        dest_path = os.path.join(dest, file)

        # Move from src1 to dest1
        shutil.move(src_path, dest_path)
    
    return


def process_n_random_file_pairs(
    src1: str, dest1: str,
    src2: str, dest2: str,
    n: int,
    mode: str
):
    """
    Desc:
        Copies 'n' random files from 'src1' to 'dest1' and the same filenames from 'src2' to 'dest2'.
    Args:
        src1 (str): Source directory 1.
        dest1 (str): Destination directory 1.
        src2 (str): Source directory 2.
        dest2 (str): Destination directory 2.
        n (int): Number of files to move.
        mode (str): Either copy or move
    """
    try:
        # Validate source directories
        if not os.path.isdir(src1):
            print(f"Directory '{src1}' does not exist.")
            return False
        if not os.path.isdir(src2):
            print(f"Directory '{src2}' does not exist.")
            return False

        # Create destination directories if they don't exist
        os.makedirs(dest1, exist_ok=True)
        os.makedirs(dest2, exist_ok=True)

        # Get file list from src1
        all_files = [f for f in os.listdir(src1) if os.path.isfile(os.path.join(src1, f))]

        if len(all_files) < n:
            n = len(all_files)
            print(f"{n} files to {mode}.")

        # Select random files
        files_to_copy = random.sample(all_files, n)

        for file in tqdm(files_to_copy):
            src1_path = os.path.join(src1, file)
            dest1_path = os.path.join(dest1, file)

            src2_path = os.path.join(src2, file.replace(".fits", ".tif"))
            dest2_path = os.path.join(dest2, file.replace(".fits", ".tif"))

            # Proceed only if the file exists in both src1 and src2
            if os.path.exists(src1_path) and os.path.exists(src2_path):
                
                if mode.lower() == "copy":
                    shutil.copy(src1_path, dest1_path)
                    shutil.copy(src2_path, dest2_path)
                elif mode.lower() == "move":
                    shutil.move(src1_path, dest1_path)
                    shutil.move(src2_path, dest2_path)
                    
            else:
                print(f"Skipping '{file}': Not found in src2 ('{src2_path}')")

    except Exception as e:
        print(f"Error occurred while copying files: {str(e)}")
        
        
        


if __name__ == "__main__":
    
    src1  = ""
    dest1 = ""
    
    src2  = ""
    dest2 = ""
    
    n    = 3420
    mode = "move"

    process_n_random_file_pairs(src1, dest1, src2, dest2, n, mode)