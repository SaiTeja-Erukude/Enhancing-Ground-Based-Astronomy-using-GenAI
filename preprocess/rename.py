import os
from   tqdm     import tqdm
import pandas   as pd


def rename_files(input_dir: str, word: str) -> bool:
    """
    Desc: 
        This method renames the files that has {word} in the filename
    Args:
        input_dir (str): Path to the input directory 
        word (str): A word to look for in the filename
    Returns:
        True, if renaming operation is success, else False.
    """
    try:        
        if not os.path.isdir(input_dir):
            print(f"The directory {input_dir} does not exist.")
            return False
        
        for file in tqdm(os.listdir(input_dir)):
            basename, ext = os.path.splitext(file)

            if word in basename:
                new_name = f"{basename.replace(word, '')}{ext}"
                
                # Construct full paths for renaming
                old_file_path = os.path.join(input_dir, file)
                new_file_path = os.path.join(input_dir, new_name)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
        
        return True
    
    except Exception as rename_ex:
        print(f"An error occurred while renaming: {rename_ex}")
        return False
    


def rename_files_with_coords(input_dir: str, coords_csv: str) -> bool:
    try:        
        if not os.path.isdir(input_dir):
            print(f"The directory {input_dir} does not exist.")
            return False
        
        if not os.path.isfile(coords_csv):
            print(f"The file {coords_csv} does not exist.")
            return False
        
        # Load CSV
        df = pd.read_csv(coords_csv)
        
        for file in tqdm(os.listdir(input_dir)):
            basename, ext = os.path.splitext(file)
            
            # Find the row where survey_id matches img_id
            row = df[df["survey_id"] == int(basename)]
            
            ra  = row.iloc[0]["RA"]
            dec = row.iloc[0]["DEC"]
            
            new_name = f"{basename}_{ra}_{dec}{ext}"
            
            # Construct full paths for renaming
            old_file_path = os.path.join(input_dir, file)
            new_file_path = os.path.join(input_dir, new_name)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)
            
        return True
        
    except Exception as rename_ex:
        print(f"An error occurred while renaming: {rename_ex}")
        return False


def remove_id_from_filename(input_dir):
    try:        
        if not os.path.isdir(input_dir):
            print(f"The directory {input_dir} does not exist.")
            return False
        
        for file in tqdm(os.listdir(input_dir)):
            basename, ext = os.path.splitext(file)
            
            parts = len(basename.split("_"))
            if parts < 3:
                continue
            
            new_name = "_".join(basename.split("_")[1:]) + ext
            
            # Construct full paths for renaming
            old_file_path = os.path.join(input_dir, file)
            new_file_path = os.path.join(input_dir, new_name)
            
            # Remove if already exists
            if os.path.exists(new_file_path):
                os.remove(new_file_path)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)
        return True
    
    except Exception as rename_ex:
        print(f"An error occurred while renaming: {rename_ex}")
        return False



if __name__ == "__main__":
    input_dir  = ""
    coords_csv = ""
    remove_id_from_filename(input_dir)