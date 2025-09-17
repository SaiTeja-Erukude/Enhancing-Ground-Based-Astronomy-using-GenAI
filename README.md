# 🌌 Galaxy Enhancer

> **Enhance ground-based astronomical images with the power of Generative AI.**

This project allows you to download ground-based telescope image data using celestial coordinates (RA/Dec), convert it into a usable image format, and enhance it using a custom-trained Conditional Generative Adversarial Network.

The cGAN model was trained on paired images from ground-based and space-based telescopes, with the goal of transforming ground-based observations to match the quality and clarity of space-based imagery.

---

## ✨ Features

- 🔭 Input celestial coordinates (RA, Dec)
- 📡 Download raw **FITS** files from public astronomical databases
- 🖼️ Convert FITS to 8-bit **TIF** format
- 🤖 Enhance the image using a pre-trained **cGAN (Conditional GAN)** model
- 💾 Save the enhanced image in `.png` format

---

## 📷 Sample Outputs
Coming soon ...

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/SaiTeja-Erukude/Enhancing-Ground-Based-Astronomy-using-GenAI.git
cd galaxy-enhancer
```

### 2. Set Up a Virtual Environment

```bash
python3.8 -m venv .venv
.venv\Scripts\activate  # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🛰️ Usage
```bash
python main.py
```