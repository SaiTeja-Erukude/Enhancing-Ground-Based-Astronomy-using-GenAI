import os
import cv2
from   PIL        import Image
from   tqdm       import tqdm
import numpy      as np


def resize_16bit_image(pil_img, target_size):
    arr = np.array(pil_img)
    resized = cv2.resize(arr, target_size, interpolation=cv2.INTER_LINEAR)
    return Image.fromarray(resized.astype(np.uint16), mode="I;16")


def concatenate_images(image1_path: str, image2_path: str, output_path: str) -> bool:
    """
    Desc:
        Concatenates two images side-by-side (horizontally) and saves the result to a specified path.
    Parameters:
        image1_path (str): File path to the first image (will appear on the left).
        image2_path (str): File path to the second image (will appear on the right).
        output_path (str): File path where the resulting concatenated image will be saved.
    Returns:
        bool: True if the images were successfully concatenated and saved, False if an error occurred.
    """
    try:
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)

        # Validate mode
        if image1.mode != "I;16" or image2.mode != "I;16":
            print(f"[!] Unsupported image mode(s): {image1.mode}, {image2.mode}. Expected 'I;16'.")
            return False

        # Match sizes by resizing both to the same (max) height and width
        target_width  = max(image1.width, image2.width)
        target_height = max(image1.height, image2.height)
        target_size   = (target_width, target_height)

        image1_resized = resize_16bit_image(image1, target_size)
        image2_resized = resize_16bit_image(image2, target_size)

        # Create output canvas
        total_width = target_width * 2
        output_img = Image.new("I;16", (total_width, target_height))

        # Paste both images side by side
        output_img.paste(image1_resized, (0, 0))
        output_img.paste(image2_resized, (target_width, 0))

        # Save as 16-bit TIFF
        output_img.save(output_path, format="TIFF")
        
        
    except Exception as concat_ex:
        print(f"Error occurred while concatenating: {concat_ex}")
    


if __name__ == "__main__":
    
    legacy_images = "../data/train/legacy"    
    hubble_images = "../data/train/hubble"
    output_path   = "../data/train/concat"
    
    # Make sure output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    for filename in tqdm(os.listdir(legacy_images)):
        
        legacy_img_path   = os.path.join(legacy_images, filename)
        hubble_img_path   = os.path.join(hubble_images, filename)
        output_image_path = os.path.join(output_path, filename)
        
        # Check if both files exist
        if os.path.exists(hubble_img_path):
            concatenate_images(
                legacy_img_path, 
                hubble_img_path, 
                output_image_path
            )