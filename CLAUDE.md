# fly_ovaries_processing_pipeline

## Project Overview
Image analysis pipeline for quantifying germ cell organization in *Drosophila* ovaries. Analyzes whole-ovary 3D fluorescence microscopy images to segment and characterize two cell populations — VASA+ germ cells and TJ+ follicle/escort cells — and quantify their spatial relationships.

## Biological Context
- **Model organism:** *Drosophila melanogaster*
- **Tissue:** Whole ovary (3D volume)
- **Markers:**
  - **VASA** (ch1): Germ cell marker — cytoplasmic
  - **Membrane** (ch2): Cell membrane label
  - **TJ** (ch3): Tight junction protein — marks follicle/escort cells
  - **DAPI** (ch4): Nucleus
- **Imaging:** Zeiss Airyscan (63x objective), CZI format, ~0.14 µm XY / ~0.25 µm Z after downsampling

## Pipeline Architecture

### Input
- Zeiss CZI files (multi-channel, 3D, Airyscan processed)
- Files follow naming convention: `*_63x*-Airyscan*.czi`

### Stage 1 — Preprocessing (`processFiles`)
- Read CZI with `aicsimageio`
- Resample each channel to target isotropic pixel size using `aicsimageprocessing.resize`
- Save per-channel OME-TIFF to `ch1/`, `ch2/`, `ch3/`, `ch4/` subfolders
- Output suffix: `_downs.tiff`

### Stage 2 — Segmentation (`processTJ`, `processVASA`, `processVASA_cp4`)
- **TJ (ch3):** Cellpose 2D with stitch-across-z (`do_3D=False`, `stitch_threshold=0.3`)
- **VASA (ch1):** Two options:
  - 2D-stitched (`processVASA`): same approach as TJ
  - True 3D (`processVASA_cp4`): `do_3D=True`, `anisotropy=1.78`, `flow3D_smooth=2`
- Custom trained Cellpose models stored in `models/`
- Normalization: percentile [1, 99], norm3D=True

### Stage 3 — Post-processing
- `processSegmentationMasks` / `processVASASegmentationMasks`: extract regionprops, compute volume and surface area (marching cubes via `skimage.measure`)
- `refine_outliers` / `refineVASASegmentationMasks`: IQR-based outlier removal (cells below Q1 - 1.5×IQR flagged as debris/fragments)
- Outputs: `_refined.tif` label images + CSV stats

### Stage 4 — Spatial Analysis (`spatial_analysis_tools.py`)
- `analyzeVASANeighbors`: face-adjacency contact detection → weighted NetworkX graph → per-cell metrics (neighbors, cluster size, surface sharing ratio, clustering coefficient)
- `computeGraphControl`: configuration model null hypothesis test (preserves degree sequence, randomizes topology, n=1000 permutations)
- `computeRipleysK`: 3D Ripley's K/L function with Monte Carlo CSR envelope (n=100 simulations)
- `paintLabelsByMetric`: maps per-cell metrics back onto label image for visualization

### Output Files
| File | Content |
|------|---------|
| `*_TJ_counts.csv` | TJ cell counts per dataset |
| `*_VASA_counts.csv` | VASA cell counts, raw and refined |
| `*_VASA_detailed_counts.csv` | Per-cell morphometrics |
| `*_VASA_neighbor_metrics.csv` | Per-cell spatial graph metrics |
| `*_VASA_neighbor_summary.csv` | Dataset-level graph summary |

## Code Organization
```
src/
  processing_tools.py       # Core pipeline functions
  spatial_analysis_tools.py # Neighbor/spatial statistics
  processing_pipeline_cp4.ipynb   # Main pipeline notebook
  refine_VASA_labels.ipynb        # VASA post-processing notebook
  neighbors_test.ipynb            # Spatial analysis notebook
models/
  VASA_xy_pipeline_bright_Mikala  # Custom Cellpose model for VASA
  TJ_xy_pipeline_norm_Mikala      # Custom Cellpose model for TJ
```

## Environment
- Conda env: `cellpose_mikala_pipeline` (Python 3.10)
- Key dependencies: `cellpose==3.0.7`, `aicsimageio==4.14.0`, `scikit-image`, `networkx`, `pandas`, `PyTorch 2.2.2 + CUDA 11.8`
- GPU required for Cellpose inference
- Full environment: `environment.yaml`

## Key Parameters
| Parameter | Value | Notes |
|-----------|-------|-------|
| Target pixel size | [0.25, 0.14, 0.14] µm | Z, Y, X after downsampling |
| Anisotropy (3D) | 1.78 | Z/XY ratio for Cellpose cp4 |
| TJ diameter | 19.59 px | Cellpose expected diameter |
| VASA diameter | 39 px | Cellpose expected diameter (2D mode) |
| Min cell size | 100 voxels | Debris filter |
| Outlier filter | Q1 - 1.5×IQR | Applied to `num_pixels` |
| Stitch threshold | 0.3 | Cross-z mask stitching |

## Conventions
- Channel IDs are 1-indexed in file paths (`ch1`–`ch4`), 0-indexed in `aicsimageio` API calls
- Dataset name parsed from filename: `maskFile.split('_ch')[0]`
- Date parsed from filename: `maskFile.split('_')[0]`
- Label images saved as `uint16` (refined as `uint8` with LZW compression)
- All spatial metrics use physical units (µm, µm², µm³)
