#!/bin/bash
# =============================================================================
# Fly ovaries processing pipeline — single folder
# Step 1: VASA segmentation  (CellPose 4, cellpose4 env)
# Step 2: TJ   segmentation  (CellPose 3, cellpose3 env)
#
# SLURM directives: add #SBATCH lines here, e.g.:
#   #SBATCH --job-name=fly_ovaries
#   #SBATCH --partition=gpu
#   #SBATCH --gres=gpu:1
#   #SBATCH --cpus-per-task=8
#   #SBATCH --mem=64G
#   #SBATCH --output=logs/%j.out
# =============================================================================

# --- Configuration -----------------------------------------------------------
INPUT_FOLDER="/path/to/raw/images"
PREPROC_FOLDER="/path/to/preprocessed"
OUTPUT_FOLDER="/path/to/output"

VASA_MODEL_PATH="/path/to/vasa/models"
VASA_MODEL_NAME="VASA_082025set_cp4_xy_yz_xz_08072025_300epoch"

TJ_MODEL_PATH="/path/to/tj/models"
TJ_MODEL_NAME="TJ_xy_10222024"

TARGET_PX_SIZE="0.25,0.14,0.14"   # ZYX
CHANNEL_MAPPING="4321"             # 1:VASA 2:membrane 3:TJ 4:DAPI

# Resolve script directory so paths work regardless of where the job is submitted
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source conda
source "$(conda info --base)/etc/profile.d/conda.sh"

# --- Step 1: VASA segmentation (CellPose 4) ----------------------------------
echo "=== [1/2] VASA segmentation — cellpose4 env ==="

conda activate cellpose4

echo "Running: python ${SCRIPT_DIR}/process_vasa.py --input ${INPUT_FOLDER} --preproc ${PREPROC_FOLDER} --output ${OUTPUT_FOLDER} --model-path ${VASA_MODEL_PATH} --model-name ${VASA_MODEL_NAME} --px-size ${TARGET_PX_SIZE} --channel-mapping ${CHANNEL_MAPPING} --preprocess"
python "${SCRIPT_DIR}/process_vasa.py" \
    --input          "${INPUT_FOLDER}"    \
    --preproc        "${PREPROC_FOLDER}"  \
    --output         "${OUTPUT_FOLDER}"   \
    --model-path     "${VASA_MODEL_PATH}" \
    --model-name     "${VASA_MODEL_NAME}" \
    --px-size        "${TARGET_PX_SIZE}"  \
    --channel-mapping "${CHANNEL_MAPPING}" \
    --preprocess

if [ $? -ne 0 ]; then
    echo "ERROR: VASA segmentation failed. Aborting pipeline."
    exit 1
fi

conda deactivate

# --- Step 2: TJ segmentation (CellPose 3) ------------------------------------
echo "=== [2/2] TJ segmentation — cellpose3 env ==="

conda activate cellpose3

echo "Running: python ${SCRIPT_DIR}/process_tj.py --input ${INPUT_FOLDER} --preproc ${PREPROC_FOLDER} --output ${OUTPUT_FOLDER} --model-path ${TJ_MODEL_PATH} --model-name ${TJ_MODEL_NAME}"
python "${SCRIPT_DIR}/process_tj.py" \
    --input      "${INPUT_FOLDER}"    \
    --preproc    "${PREPROC_FOLDER}"  \
    --output     "${OUTPUT_FOLDER}"   \
    --model-path "${TJ_MODEL_PATH}"   \
    --model-name "${TJ_MODEL_NAME}"

if [ $? -ne 0 ]; then
    echo "ERROR: TJ segmentation failed."
    exit 1
fi

conda deactivate

echo "=== Pipeline complete ==="
