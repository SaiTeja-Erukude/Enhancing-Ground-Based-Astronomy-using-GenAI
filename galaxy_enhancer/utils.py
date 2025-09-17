import os
import requests
import numpy    as np
from   PIL      import Image
Image.LOAD_TRUNCATED_IMAGES = True


LEGACY_DOWNLOAD_URL = "https://www.legacysurvey.org/viewer/cutout.fits?ra={ra}&dec={dec}&layer=hsc-dr2&pixscale=0.04"
WORKAREA_PATH       = "workarea"
OUTPUTS_PATH        = "outputs"
MODEL_PATH          = "model/galaxy_enhancer_cgan.h5"


def print_welcome_text():
    print("\n" + "=" * 60)
    print("🌌  Welcome to Galaxy Enhancer  🌌".center(50))
    print("   Explore the cosmos like never before!".center(50))
    print("=" * 60 + "\n")
    print()


def get_user_input():
    ra = input("🔭  Enter Right Ascension (RA) in degrees: ")
    dec = input("🌠  Enter Declination (Dec) in degrees: ")
    return ra, dec


def download_fits(ra, dec) -> str:  
    try:
        _url = LEGACY_DOWNLOAD_URL.format(ra=ra, dec=dec)
        response = requests.get(_url, timeout=10)
        response.raise_for_status()

        save_filename = f"{ra}_{dec}.fits"
        save_path = os.path.join(WORKAREA_PATH, save_filename)        
        with open(save_path, "wb") as f:
            f.write(response.content)
        
        return save_filename

    except Exception as ex:
        return ex


def delete_workare_file(file_name):
    try:
        file_path = os.path.join(WORKAREA_PATH, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as ex:
        return ex


def convert_fits_to_tif(fits_name):
    from   astropy.io       import fits
    import tifffile

    if not fits_name.lower().endswith((".fits")):
        return None
    
    try:
        fits_path = os.path.join(WORKAREA_PATH, fits_name)
        with fits.open(fits_path, memmap=False) as hdul:
            data = hdul[0].data.copy()
        
        gray = np.mean(data, axis=0)
        gray_flipped = np.flipud(gray)
        
        # Normalize to 0–65535 and convert to 16-bit
        gray_flipped -= np.min(gray_flipped)
        gray_flipped /= np.max(gray_flipped)
        gray_flipped *= 65535
        gray_16bit = gray_flipped.astype(np.uint16)
        
        tif_name = os.path.splitext(fits_name)[0] + ".tif"
        tif_path = os.path.join(WORKAREA_PATH, tif_name)
        
        tifffile.imwrite(tif_path, gray_16bit)
        
        delete_workare_file(fits_name)
        return tif_name
        
    except Exception as ex:
        return ex
    
    

def preprocess_image(image_path, target_size=(256, 256)):
    """
    Load and preprocess a 16-bit grayscale or RGB image as RGB for model input.
    """
    img = Image.open(image_path)
    img = img.resize(target_size)

    # Convert to grayscale if needed
    img = img.convert("I")  # 32-bit signed integer pixels (safe for 16-bit)
    img_np = np.array(img)

    # If it's 16-bit or more, scale to 8-bit
    if img_np.dtype == np.uint16 or img_np.max() > 255:
        img_np = (img_np / 256).astype(np.uint8)

    # Convert grayscale to RGB by stacking the single channel
    img_rgb = np.stack([img_np] * 3, axis=-1)  # shape: (H, W, 3)

    # Convert to float32 and normalize to [-1, 1]
    img_rgb = img_rgb.astype(np.float32)
    img_rgb = (img_rgb - 127.5) / 127.5

    # Add batch dimension
    return np.expand_dims(img_rgb, axis=0)


def postprocess_image(image_tensor):
    """
    Converts model output tensor (in [-1, 1]) to a displayable 8-bit PIL Image.
    """
    image_tensor = (image_tensor + 1) / 2.0  # Scale to [0, 1]
    image_tensor = np.clip(image_tensor[0], 0, 1)  # Remove batch, clip to valid range
    return Image.fromarray((image_tensor * 255).astype(np.uint8))


def enhance(tif_name):
    try:
        from keras.models import load_model
        
        model = load_model(MODEL_PATH)
        print("✅ cGAN model loaded successfully!")
        
        image_size = (256, 256)
        tif_path   = os.path.join(WORKAREA_PATH, tif_name)
        src_image  = preprocess_image(tif_path, target_size=image_size)

        enhanced_image = model.predict(src_image, verbose=0)
        output_img     = postprocess_image(enhanced_image)

        output_name = os.path.splitext(tif_name)[0] + ".png"
        output_path = os.path.join(OUTPUTS_PATH, output_name)
        output_img.save(output_path)
        
        delete_workare_file(tif_name)
        return output_path
        
    except Exception as ex:
        print(ex)
        return None