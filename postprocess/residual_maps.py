import os

import numpy as np
from PIL import Image
from tqdm import tqdm


SUPPORTED_EXTS = {".png", ".tif", ".tiff", ".jpg", ".jpeg", ".bmp"}


def build_file_map(directory):
    file_map = {}
    for filename in os.listdir(directory):
        base, ext = os.path.splitext(filename)
        if ext.lower() in SUPPORTED_EXTS:
            file_map[base] = os.path.join(directory, filename)
    return file_map


def load_grayscale(path):
    with Image.open(path) as img:
        img = img.convert("F")
        arr = np.array(img, dtype=np.float32, copy=True)

    max_value = float(np.max(arr)) if arr.size else 0.0
    if max_value > 255.0:
        arr /= 65535.0
    else:
        arr /= 255.0

    return np.clip(arr, 0.0, 1.0)


def save_grayscale_png(arr, path):
    arr_u8 = np.clip(arr * 255.0, 0.0, 255.0).astype(np.uint8)
    Image.fromarray(arr_u8, mode="L").save(path)


def compute_residual_maps(preds_dir, gt_dir, output_dir, resize):
    os.makedirs(output_dir, exist_ok=True)

    pred_map = build_file_map(preds_dir)
    gt_map = build_file_map(gt_dir)
    common_basenames = sorted(set(pred_map) & set(gt_map))

    print(f"> Found {len(common_basenames)} matching image pairs.")

    skipped = 0
    for base in tqdm(common_basenames):
        pred = load_grayscale(pred_map[base])
        gt = load_grayscale(gt_map[base])

        if pred.shape != gt.shape:
            if resize == "pred-to-gt":
                pred_img = Image.fromarray((pred * 255.0).astype(np.uint8), mode="L")
                pred_img = pred_img.resize((gt.shape[1], gt.shape[0]), Image.BICUBIC)
                pred = np.asarray(pred_img, dtype=np.float32) / 255.0
            elif resize == "gt-to-pred":
                gt_img = Image.fromarray((gt * 255.0).astype(np.uint8), mode="L")
                gt_img = gt_img.resize((pred.shape[1], pred.shape[0]), Image.BICUBIC)
                gt = np.asarray(gt_img, dtype=np.float32) / 255.0
            else:
                print(f"Skipping {base}: shape mismatch pred={pred.shape}, gt={gt.shape}")
                skipped += 1
                continue

        residual = np.abs(pred - gt)
        save_path = os.path.join(output_dir, f"{base}_residual.png")
        save_grayscale_png(residual, save_path)

    if skipped:
        print(f"> Skipped {skipped} image pairs due to shape mismatch.")


if __name__ == "__main__":
    
    PREDS_DIR  = "D:/Projects/Enhancing Ground-Based Astronomy using GenAI/data/residual_maps/preds (enhanced)"
    GT_DIR     = "D:/Projects/Enhancing Ground-Based Astronomy using GenAI/data/residual_maps/ground_truth (hubble)"
    OUTPUT_DIR = "D:/Projects/Enhancing Ground-Based Astronomy using GenAI/data/residual_maps/maps"
    RESIZE     = "pred-to-gt"  # Options: "none", "pred-to-gt", "gt-to-pred"

    compute_residual_maps(PREDS_DIR, GT_DIR, OUTPUT_DIR, RESIZE)
