import os
import numpy as np
from keras.models import load_model
from tqdm import tqdm
from PIL import Image

# Fix for truncated TIFF files
Image.LOAD_TRUNCATED_IMAGES = True


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
        print(f"{os.path.basename(image_path)} is 16-bit. Converting to 8-bit.")
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


if __name__ == "__main__":
    test_dir   = ""
    output_dir = ""
    model_path = ""

    os.makedirs(output_dir, exist_ok=True)

    model = load_model(model_path)
    print("cGAN model loaded successfully!")

    supported_exts = (".png", ".jpg", ".jpeg", ".tif", ".tiff")
    image_size = (256, 256)

    for filename in tqdm(os.listdir(test_dir)):
        if not filename.lower().endswith(supported_exts):
            continue

        image_path = os.path.join(test_dir, filename)
        src_image = preprocess_image(image_path, target_size=image_size)

        generated_image = model.predict(src_image, verbose=0)
        output_img = postprocess_image(generated_image)

        output_filename = os.path.join(output_dir, os.path.splitext(filename)[0] + ".png")
        output_img.save(output_filename)