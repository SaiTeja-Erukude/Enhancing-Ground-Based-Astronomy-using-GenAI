import os
import json
import requests
import pandas as pd
from tqdm import tqdm
from PIL import Image
from io import BytesIO

# Paths
HUBBLE_JSON = ""
LEGACY_PATH = ""
CSV_PATH    = ""

os.makedirs(LEGACY_PATH, exist_ok=True)

# Load image IDs from JSON
with open(HUBBLE_JSON, "r") as f:
    image_ids = json.load(f)

# Load CSV
df = pd.read_csv(CSV_PATH)

# Download and save grayscale images
for img_id in tqdm(image_ids):
    # Find the row where survey_id matches img_id
    row = df[df["survey_id"] == int(img_id)]

    if row.empty:
        print(f"[!] Warning: No match found for {img_id}")
        continue

    ra  = row.iloc[0]["RA"]
    dec = row.iloc[0]["DEC"]

    # Construct the download URL
    url = f"https://www.legacysurvey.org/viewer/cutout.fits?ra={ra}&dec={dec}&layer=hsc-dr2&pixscale=0.04"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Save jpgs
        # Convert to grayscale
        # img_gray = Image.open(BytesIO(response.content)).convert("L")
        # save_filename = f"{img_id}_{ra}_{dec}.jpg"
        # save_path = os.path.join(LEGACY_PATH, save_filename)
        # img_gray.save(save_path)

        # Save FITS
        save_filename = f"{img_id}_{ra}_{dec}.fits"
        save_path = os.path.join(LEGACY_PATH, save_filename)        
        with open(save_path, "wb") as f:
            f.write(response.content)

    except Exception as e:
        print(f"[!] Failed to download {img_id}: {e}")
