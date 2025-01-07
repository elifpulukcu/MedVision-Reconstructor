# MedVision Reconstructor

**MedVision Reconstructor** is a Python application designed for reconstructing medical images via **Radon Transform**, **Filtered Back-Projection (FBP)**, and **Simultaneous Algebraic Reconstruction Technique (SART)**. The project includes a user-friendly interface built with [PySide6](https://doc.qt.io/qtforpython/) that lets you load medical images, select reconstruction parameters (angle range, filters), and visualize both the sinogram and reconstructed images.

---

## Features

1. **Interactive GUI (PySide6)**
   - Intuitive interface for loading images and setting reconstruction parameters.  
   - Real-time visualization of sinograms and reconstruction outputs.

2. **Multiple Reconstruction Methods**  
   - **Filtered Back-Projection (FBP)** with multiple filters:
     - `ramp`, `shepp-logan`, `cosine`, `hamming`, `hann`
   - **SART (Simultaneous Algebraic Reconstruction Technique)**
   
3. **Radon Transform & Sinogram Generation**  
   - Leverages [scikit-image](https://scikit-image.org/) for computing radon transforms.

4. **Animation of Incremental Reconstruction**  
   - Enables an angle-by-angle view of how reconstruction quality evolves.

5. **Test Script**  
   - A standalone script (`test.py`) that demonstrates sinogram creation and reconstruction with FBP or SART.

---

## Project Structure

Below is the directory structure for **MedVision-Reconstructor**:

```
MedVision-Reconstructor/
 ├── images/                         # Folder containing sample medical images
 ├── medical_env/                    # (Optional) Virtual environment folder
 ├── src/
 │    ├── main.py                    # Main GUI application (PySide6)
 │    ├── MI.py                      # Reconstruction class (Radon, FBP, SART)
 │    └── test.py                    # Test script for demonstration
 ├── .gitignore
 ├── LICENSE
 ├── README.md
 └── requirements.txt
```

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/elifpulukcu/MedVision-Reconstructor.git
   cd MedVision-Reconstructor
   ```

2. **(Optional) Create & Activate a Virtual Environment**  
   ```bash
   python -m venv medical_env
   source medical_env/bin/activate      # On Unix / Mac
   # or
   medical_env\Scripts\activate         # On Windows
   ```

3. **Install Dependencies**  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   If no `requirements.txt` exists, install the main libraries manually:
   ```bash
   pip install PySide6 matplotlib scikit-image numpy
   ```

---

## Usage

### 1. Launching the GUI

Run the **main application** to open the GUI:

```bash
cd src
python main.py
```

**Key Interface Elements**:

1. **Load Image**  
   - Select `.png`, `.jpg`, `.jpeg`, or `.bmp` images from your filesystem.
2. **Maximum Angle**  
   - Enter the maximum angle (e.g., `180`) for radon transform sampling.
3. **Reconstruction Method**  
   - Choose among the following filters for FBP:
     - `ramp`, `shepp-logan`, `cosine`, `hamming`, `hann`  
   - Or select **SART** for algebraic reconstruction.
4. **Calculate**  
   - Computes the sinogram and reconstructs the image based on the selected method.  
   - Displays the sinogram and reconstructed image.
5. **Show Animation**  
   - Iterates through angles in steps (from 10° up to the specified angle) to visualize progressive reconstruction.

### 2. Test Script

A separate **test script** (`test.py`) demonstrates the reconstruction steps in a non-GUI fashion:

```bash
cd src
python test.py
```

This script will:
- Load a specified image from the `images/` directory (you can change the path in the code).  
- Generate a sinogram using the **Radon Transform**.  
- Perform **Filtered Back-Projection (FBP)** and **SART** reconstructions.  
- Display the original image, the sinogram, and reconstruction results side by side.

---

## Implementation Details

### `MI.py` (Core Reconstruction Logic)
1. **Class `MI`**  
   - **Constructor**: Accepts `image`, `maxAngle`, and `filterName`. Converts RGB to grayscale if necessary.  
   - **`processImage`**: Rescales the image (default scale factor of `0.4`) and prepares angles for radon transform.  
   - **`radonTransform`**: Performs the **Radon Transform** (`scikit-image.transform.radon`).  
   - **`filteredBackProjection`**: Uses **iradon** with the specified filter to reconstruct the image from its sinogram.  
   - **`sart`**: Applies **iradon_sart** for algebraic reconstruction.

### `main.py` (GUI)
1. **PySide6 Window**  
   - **Load Image** button uses a `QFileDialog` to select and display an image.  
   - **Calculate** calls either `filteredBackProjection` or `sart`, then renders the sinogram and reconstruction with `matplotlib`.  
   - **Show Animation** demonstrates incremental reconstruction from small angles up to the user-specified maximum.

### `test.py` (Testing & Demonstration)
1. **Command-Line Runner**  
   - Reads an image from `images/`.  
   - Generates sinogram and performs both FBP and SART reconstructions.  
   - Displays comparative results via `matplotlib`.

---

## Planned Improvements

1. **Algorithmic Expansion**  
   - Investigate other iterative methods like **ART**, **TV-based** methods, or deep-learning approaches.

2. **Performance Optimization**  
   - Potential GPU acceleration using [CuPy](https://cupy.dev/) or PyTorch for large-scale reconstructions.

3. **Dataset & Demo**  
   - Include more diverse images in `images/` to showcase various organ/tissue reconstructions.

4. **Parameter Tuning**  
   - User-adjustable SART parameters (relaxation, iterations) through the GUI.

5. **CLI Extension**  
   - Offer a robust command-line interface for batch processing or pipeline integration.

---

## License

Distributed under the [MIT License](LICENSE). Feel free to use, modify, and distribute this code for personal or commercial projects, subject to the terms of the license.

---

## Disclaimer

This repository is intended for **educational and research** purposes. The authors do not guarantee the suitability of this software for clinical or diagnostic use.

---

## Author

Developed by [Elif Pulukçu](https://github.com/elifpulukcu).  
Contributions and pull requests are welcome—please open an [issue](https://github.com/elifpulukcu/MedVision-Reconstructor/issues) or submit a PR for improvements.
