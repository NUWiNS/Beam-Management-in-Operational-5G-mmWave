# Artifact for: Beam Management in Operational 5G mmWave Networks  
ACM CoNEXT 2025 

---

## Overview

This artifact reproduces all figures from our paper **"Beam Management in Operational 5G mmWave Networks"**, the first large-scale empirical study of beam switching, coherence time, and beam directionality in commercial 5G mmWave deployments.

The artifact includes:
- Preprocessed real-world datasets (`.pkl` files),
- Python scripts to reproduce figures
- A master script to generate all figures at once.

All results should be able reproduced using standard Python packages on any Unix-like machine with no special hardware or proprietary software.

---

## Directory Structure

```text
.
├── pkl/           # Preprocessed data (23 pickle files)
├── plots/         # Output directory for generated plots (40+ PDFs)
├── scripts/       # Individual scripts, each generates one figure (e.g., "# Fig. 13(c)")
├── reproduce_all.sh   # Master script to reproduce all figures
└── README.md      # This file
```

---

## System Requirements

- OS: Linux or macOS (Unix-based)
- Python: 3.6 or newer
- Disk space: < 25 MB
- No GPU, sudo privileges, or special hardware required

---

## Dependencies

Install the minimal required Python packages:

```bash
pip install numpy matplotlib
```

We also use `pickle` from the Python standard library (no installation needed).

---

## Reproducing All Figures

Follow these steps to reproduce every figure in the paper:

### Step 1: Clone the Repository

```bash
git clone https://github.com/NUWiNS/Beam-Management-in-Operational-5G-mmWave.git
cd Beam-Management-in-Operational-5G-mmWave
```

### Step 2: Install Dependencies

```bash
pip install numpy matplotlib
```

### Step 3: Run All Scripts

```bash
chmod +x reproduce.sh
./reproduce.sh
```

This will:
- Automatically run all scripts in the `scripts/` directory
- Print the figure being generated (e.g., `📊 Fig. 13(c)`)
- Print where each figure is saved (e.g., `💾 ../plots/box_drive_walk_mcs.pdf`)
- Save all plots to the `plots/` directory

> Total runtime: ~5 minutes  
> Output: figures in PDF format that are similar to what we used in the paper

---

## Expected Output

- Each script outputs one figure corresponding to a paper figure.
- Files are saved as high-quality `.pdf` in `plots/`.
- Console output confirms figure generation and includes numerical statistics (means, percentiles, etc.).
- Outputs are deterministic with no randomness or variation.

---

## Customization

Each script in `scripts/` is self-contained and easy to modify:
- Change `save_flag` or `show_flag` at the bottom of the script
- Adjust plot styles via matplotlib
- Swap out `.pkl` inputs to run custom or ablated experiments

---

## Troubleshooting

- Ensure you're running from the project root directory.
- Confirm Python version is 3.6+:
  ```bash
  python3 --version
  ```
- If plots don’t appear, check that `save_flag = 1` is set in the script.
- Make sure the `plots/` directory exists and is writable.

---

## Citation

If you use this artifact in your own work, please cite our paper

---

## Contact

**Phuc Dinh**  
Email: `dinh.p[at]northeastern.edu`  
GitHub: [https://github.com/NUWiNS](https://github.com/NUWiNS)

---

