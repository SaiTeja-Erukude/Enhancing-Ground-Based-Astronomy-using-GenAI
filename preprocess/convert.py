import os
from   PIL              import Image
from   tqdm             import tqdm
from   astropy.io       import fits
import numpy            as np
import tifffile


def convert_fits_to_tif(in_dir, out_dir):
    
    for filename in tqdm(os.listdir(in_dir)):
        if filename.lower().endswith((".fits")):
            fits_path = os.path.join(in_dir, filename)
            data = fits.getdata(fits_path)
            
            gray = np.mean(data, axis=0)
            gray_flipped = np.flipud(gray)
            
            # Normalize to 0–65535 and convert to 16-bit
            gray_flipped -= np.min(gray_flipped)
            gray_flipped /= np.max(gray_flipped)
            gray_flipped *= 65535
            gray_16bit = gray_flipped.astype(np.uint16)
            
            tif_filename = os.path.splitext(filename)[0] + ".tif"
            tif_path = os.path.join(out_dir, tif_filename)
            
            tifffile.imwrite(tif_path, gray_16bit)
    
    
    
def convert_tif_to_jpg(in_dir, out_dir):
    
    for filename in tqdm(os.listdir(in_dir)):
        if filename.lower().endswith(('.tif', '.tiff')):
            tiff_path = os.path.join(in_dir, filename)
            jpg_filename = os.path.splitext(filename)[0] + ".jpg"
            jpg_path = os.path.join(out_dir, jpg_filename)

            try:
                with Image.open(tiff_path) as img:
                    # Convert 16-bit grayscale to 8-bit
                    if img.mode == 'I;16':
                        img = img.point(lambda i: i * (1.0 / 256)).convert('L')
                    elif img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    elif img.mode == 'I':
                        img = img.convert("L")
                    elif img.mode not in ("RGB", "L"):
                        print(
                            f"Unknown mode {img.mode} for {filename}, attempting conversion to RGB.")
                        img = img.convert("RGB")

                    img.save(jpg_path, "JPEG")
                    print(f"Converted: {filename} → {jpg_filename}")

            except Exception as e:
                print(f"Failed to convert {filename}: {e}")



if __name__ == "__main__":

    INPUT_DIR  = "/home/e/erukude/Enhancing Ground-Based Astronomy using GenAI/data/test/legacy-fits-64298"
    OUTPUT_DIR = "/home/e/erukude/Enhancing Ground-Based Astronomy using GenAI/data/test/legacy-tif-64298"
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    convert_fits_to_tif(INPUT_DIR, OUTPUT_DIR)
