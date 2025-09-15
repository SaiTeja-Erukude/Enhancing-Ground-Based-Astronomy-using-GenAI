import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from tqdm import tqdm


def to_grayscale(img):
    """
    Convert an image to grayscale.
    If image is already grayscale, returns it unchanged.
    """
    if img.ndim == 2:
        return img  # Already grayscale
    elif img.ndim == 3:
        return np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
    else:
        raise ValueError("Unsupported image shape for grayscale conversion.")


def visualize_comparison(ground_image, pred_image, space_image, save_path=None):
    """
    Display side-by-side comparisons of ground input, model output, and space telescope image.
    Optionally save the comparison figure.
    """
    images = [ground_image, pred_image, space_image]
    titles = ["Ground Telescope", "Enhanced Output", "Space Telescope"]

    plt.figure(figsize=(12, 4))
    for i, (img, title) in enumerate(zip(images, titles)):
        plt.subplot(1, 3, i + 1)
        plt.imshow(img, cmap='gray')
        plt.title(title, fontdict={"fontsize": 10})
        plt.axis("off")

    plt.subplots_adjust(top=0.85, bottom=0.15, wspace=0.05)

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    
    plt.close()


def build_file_map(directory):
    """
    Build a mapping from base filename (without extension) to full path.
    Supports any image extension.
    """
    supported_exts = ['.png', '.tif', '.tiff', '.jpg', '.jpeg']
    file_map = {}
    for fname in os.listdir(directory):
        base, ext = os.path.splitext(fname)
        if ext.lower() in supported_exts:
            file_map[base] = os.path.join(directory, fname)
    return file_map


if __name__ == "__main__":

    ground_dir = "/home/e/erukude/Enhancing Ground-Based Astronomy using GenAI/data/test/legacy-jpg-64298"
    preds_dir  = "/home/e/erukude/Enhancing Ground-Based Astronomy using GenAI/cGAN/20K images/predictions/60epochs_64298"
    space_dir  = "/home/e/erukude/Enhancing Ground-Based Astronomy using GenAI/data/raw/hubble-tif-84462"
    save_dir   = "/home/e/erukude/Enhancing Ground-Based Astronomy using GenAI/cGAN/20K images/predictions/60epochs_comparisions_64298"

    os.makedirs(save_dir, exist_ok=True)

    # Build base-filename-to-path maps
    ground_map = build_file_map(ground_dir)
    pred_map   = build_file_map(preds_dir)
    space_map  = build_file_map(space_dir)

    # Intersect base filenames that are available in all three maps
    common_basenames = sorted(set(ground_map) & set(pred_map) & set(space_map))

    print(f"> Found {len(common_basenames)} common image sets.")

    for base in tqdm(common_basenames):
        ground_path = ground_map[base]
        pred_path   = pred_map[base]
        space_path  = space_map[base]

        ground_img = to_grayscale(mpimg.imread(ground_path))
        pred_img   = to_grayscale(mpimg.imread(pred_path))
        space_img  = to_grayscale(mpimg.imread(space_path))

        save_path = os.path.join(save_dir, f"{base}.png")  # Save all comparisons as PNG

        visualize_comparison(ground_img, pred_img, space_img, save_path)