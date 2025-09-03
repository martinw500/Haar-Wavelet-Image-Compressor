
# Haar Wavelet Image Compressor

A simple Python GUI tool for image compression using Haar wavelet transforms.

---

**Overview**

- Load an image, adjust compression with two sliders (Threshold & Iterations), and see original vs. compressed results.
- Supports `.png`, `.jpg`, `.jpeg`, `.bmp`.

---

**How It Works**

- **Haar Wavelet:** Compresses by averaging/differencing pixel values, reducing detail and file size.
- **Threshold:** Higher = more compression, less detail.
- **Iterations:** More = stronger compression, more loss.

---

**Features**

- Easy-to-use GUI
- Real-time preview
- Adjustable compression

---

**Installation**

```bash
git clone https://github.com/martinw500/Haar-Wavelet-Image-Compressor.git
cd Haar-Wavelet-Image-Compressor
pip install -r requirements.txt
```

---

**Usage**

```bash
python ImageCompressor.py
```
1. Load an image.
2. Adjust sliders.
3. Click Process Image.

---

**Internals**

- Applies Haar transform, thresholds small values, then reconstructs the image.
- Works on each RGB channel separately.

---

**Contributing & License**

Pull requests welcome! MIT License.
