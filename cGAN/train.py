import os 
import numpy                    as np
from os                         import listdir
from datetime                   import datetime
from pix2pix_cgan               import define_discriminator, define_generator, define_gan, train
from PIL                        import Image


def load_images(path, size=(512, 256)):
    src_list, tar_list = list(), list()

    for i, filename in enumerate(listdir(path)):
        if i % 1000 == 0:
            print(f"Images loaded: {i}.")

        image_path = os.path.join(path, filename)

        try:
            img = Image.open(image_path)
            img = img.resize(size)

            # Convert to grayscale if not already
            img = img.convert("I")  # 32-bit signed integer pixels (covers 16-bit TIFFs safely)
            img_np = np.array(img)

            # If it's 16-bit or higher, scale to 8-bit
            if img_np.dtype == np.uint16 or img_np.max() > 255:
                print(f"{filename} is 16-bit or higher. Scaling to 8-bit.")
                img_np = (img_np / 256).astype(np.uint8)  # Scale to [0,255]

            # Now convert to RGB by stacking channels
            img_rgb = np.stack([img_np] * 3, axis=-1)  # shape: (H, W, 3)
            img_rgb = img_rgb.astype(np.float32)

            # Ensure correct width
            if img_rgb.shape[1] != 512:
                print(f"Skipping {filename}: Unexpected width {img_rgb.shape[1]}")
                continue

            # Split into left (source) and right (target) images
            src_img = img_rgb[:, :256, :]
            tar_img = img_rgb[:, 256:, :]

            src_list.append(src_img)
            tar_list.append(tar_img)

        except Exception as e:
            print(f"Failed to process {filename}: {e}")
            continue

    return [np.asarray(src_list), np.asarray(tar_list)]


# dataset path
DATA_PATH = ""
EPOCHS = 100

# load dataset
[src_images, tar_images] = load_images(DATA_PATH)
print("Loaded: ", src_images.shape, tar_images.shape)


# define input shape based on the loaded dataset
image_shape = src_images.shape[1:]

# define the models
d_model = define_discriminator(image_shape)
g_model = define_generator(image_shape)
# define the composite model
gan_model = define_gan(g_model, d_model, image_shape)

# Define data
# load and prepare training images
data = [src_images, tar_images]


def preprocess_data(data):
    # load compressed arrays
    # unpack arrays
    X1, X2 = data[0], data[1]
    # scale from [0,255] to [-1,1]
    X1 = (X1 - 127.5) / 127.5
    X2 = (X2 - 127.5) / 127.5
    return [X1, X2]


dataset = preprocess_data(data)


start1 = datetime.now()
train(d_model, g_model, gan_model, dataset, n_epochs=EPOCHS, n_batch=1)
stop1 = datetime.now()

# Execution time of the model
execution_time = stop1 - start1
print("Execution time is: ", execution_time)