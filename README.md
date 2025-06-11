# Haar Wavelet Image Compressor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)]()

A simple GUI-based image compression tool using Haar wavelet transforms in Python.

---

## 🖼️ Overview

When you launch the program, a window appears with:

- A **Load Image** button that opens your system's file explorer
- A **Process Image** button to apply compression
- Two image display areas (original and processed)
- Two sliders:
  - **Threshold**: removes fine details
  - **Iterations**: determines compression depth

---

## 🧠 How It Works

### 📉 Haar Wavelet Compression

Haar wavelets compress data by averaging and differencing adjacent values. Over multiple iterations, the image becomes more compressible as it reduces redundant detail.

### 🧪 Threshold

Removes small differences from the wavelet output:

- **Low threshold** = retains more detail, less compression
- **High threshold** = removes more detail, higher compression
- Example: A value like `0.1` might become `0`, reducing file size

### 🔁 Iterations

Controls how many times each row/column is compressed:

- **More iterations** = more compression, more loss
- **Fewer iterations** = clearer image, less compression
- Each iteration halves the data and increases compressibility

---

## 🚀 Features

- Intuitive GUI for loading and processing images
- Real-time visualization of compression results
- Supports `.png`, `.jpg`, `.jpeg`, and `.bmp`
- Full RGB channel compression using Haar wavelets
- Adjustable compression via sliders

---

## 📦 Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/martinw500/Haar-Wavelet-Image-Compressor.git
   cd Haar-Wavelet-Image-Compressor
   ```

2. **Create a virtual environment** (optional but recommended)  
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎮 Usage

Run the app:

```bash
python ImageCompressor.py
```

### 🖱️ Steps

1. Click **Load Image** to select an image from your computer  
2. Use sliders to adjust:
   - **Threshold** (0 → keeps more detail, higher = more compression)
   - **Iterations** (1+ → deeper compression, more quality loss)
3. Click **Process Image** to compress and display the result

---

## 🧰 Example Interface

<details>
<summary>Click to view</summary>

![GUI Screenshot](https://raw.githubusercontent.com/martinw500/Haar-Wavelet-Image-Compressor/main/docs/images/gui1.png)

</details>

---

## 🔍 Internals

The core algorithm works by:

1. Applying Haar wavelet transform across rows (`H`)
2. Applying Haar transform to columns (`HT`)
3. Thresholding small values to zero
4. Reconstructing using inverse Haar transforms (`HTinv`, `Hinv`)
5. Repeating the process on R, G, and B channels independently

Key snippet:

```python
transformed = H(channel.copy(), iteration)
transformed = HT(transformed, iteration)
transformed[np.abs(transformed) < threshold] = 0
reconstructed = HTinv(transformed.copy(), iteration)
reconstructed = Hinv(reconstructed, iteration)
```

---

## 🗂️ Project Structure

```
.
├── ImageCompressor.py         # Main app
├── requirements.txt
├── LICENSE
├── README.md
└── docs/
    └── images/
        └── gui1.png           # Screenshot for README
```

---

## 🤝 Contributing

Pull requests are welcome! If you have ideas or improvements, feel free to fork and submit.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
