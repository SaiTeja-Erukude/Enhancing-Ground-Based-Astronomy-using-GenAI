from utils import (
    print_welcome_text,
    get_user_input,
    download_fits,
    convert_fits_to_tif,
    enhance
)

import os
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore', category=UserWarning, module='tensorflow')

# RA: 150.4015838
# Dec: 1.6157618

if __name__ == "__main__":
    print_welcome_text()

    ra, dec = get_user_input()
    print(f"\n📍 Received Coordinates:")
    print(f"   → Right Ascension (RA): {ra}")
    print(f"   → Declination (Dec):   {dec}")

    print("\n📥 Downloading FITS file...")
    fits = download_fits(ra, dec)
    if fits is None:
        print(f"❌ Error: Failed to download FITS file.")
        exit()

    print("🔄 Converting FITS to TIF format...")
    tif = convert_fits_to_tif(fits)
    if tif is None:
        print(f"❌ Error: Failed to convert FITS to TIF.")
        exit()

    print("✨ Enhancing the image using GenAI...")
    output_path = enhance(tif)
    if output_path is None:
        print(f"❌ Error: Failed to enhance. Try again later!")
        exit()

    print(f"\n✅ Enhancement complete!")
    print(f"📁 Output saved to: {output_path}\n")