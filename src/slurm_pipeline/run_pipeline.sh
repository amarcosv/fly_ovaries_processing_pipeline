#!/bin/bash
# =============================================================================
# Fly ovaries processing pipeline — single folder
# Step 1: VASA segmentation  (CellPose 4, cellpose4 env)
# Step 2: TJ   segmentation  (CellPose 3, cellpose3 env)
#
# SLURM directives: add #SBATCH lines here, e.g.:
#SBATCH --job-name=fly_o_seg
#SBATCH --partition=nvidia-L40S-20
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --output=logs/%j.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=amarcosv@wi.mit.edu
# =============================================================================



# --- Configuration -----------------------------------------------------------
REPO_DIR="${REPO_DIR:-/lab/keck_scratch/Mikala/env_test/fly_ovaries_processing_pipeline}"

INPUT_FOLDER="/lab/keck_scratch/Mikala/env_test/images/raw" #point to folder with the images or folder containing all the subfolders to batch process
PREPROC_FOLDER="/lab/keck_scratch/Mikala/env_test/images/preproc" #point to main folder with all the folders containing preprocessed data
OUTPUT_FOLDER="/lab/keck_scratch/Mikala/env_test/output" #point to main folder with all the output

VASA_MODEL_PATH="/lab/keck_scratch/Mikala/env_test/models"
VASA_MODEL_NAME="VASA_082025set_cp4_xy_yz_xz_08072025_300epoch"

TJ_MODEL_PATH="/lab/keck_scratch/Mikala/env_test/models"
TJ_MODEL_NAME="TJ_xy_10222024"

TARGET_PX_SIZE="0.25,0.14,0.14"   # ZYX
CHANNEL_MAPPING="4321"             # 1:VASA 2:membrane 3:TJ 4:DAPI

echo "Running fly ovaries segmentation pipeline for VASA and TJ cells"
echo "=== Configuration ==="
echo "INPUT_FOLDER      = ${INPUT_FOLDER}"
echo "PREPROC_FOLDER    = ${PREPROC_FOLDER}"
echo "OUTPUT_FOLDER     = ${OUTPUT_FOLDER}"
echo "VASA_MODEL_PATH   = ${VASA_MODEL_PATH}"
echo "VASA_MODEL_NAME   = ${VASA_MODEL_NAME}"
echo "TJ_MODEL_PATH     = ${TJ_MODEL_PATH}"
echo "TJ_MODEL_NAME     = ${TJ_MODEL_NAME}"



SCRIPT_DIR="${REPO_DIR}/src/slurm_pipeline"
ENVS_DIR="${REPO_DIR}/envs"

# SLURM batch jobs run a non-interactive shell that does not source
# ~/.bashrc, so the pixi PATH entry set up there never takes effect here.
# Call the pixi binary directly by its known absolute path instead
# (override PIXI_BIN beforehand if pixi is installed somewhere else).
PIXI_BIN="${PIXI_BIN:-/lab/keck_scratch/pixi/bin/pixi}"

PIXI_RUN() {
    local env="$1"; shift
    "${PIXI_BIN}" run --manifest-path "${ENVS_DIR}/pixi.toml" -e "${env}" "$@"
}

export PYTHONUNBUFFERED=1
# Set up master address and port for torchrun coordination on localhost
export MASTER_ADDR=localhost
export MASTER_PORT=$(shuf -i 29000-29900 -n 1) # Pick a random free port to avoid conflicts

# start stat collection (these lines go before running any actual gpu processing code, like af2)
group=$(dcgmi group -c gpugroup -a $CUDA_VISIBLE_DEVICES )
groupid=$(echo $group | awk '{print $10}')
dcgmi stats -g $groupid -e
dcgmi stats -g $groupid -s $SLURM_JOB_ID

# --- Step 1: VASA segmentation (CellPose 4) ----------------------------------
echo "=== [1/2] VASA segmentation — cellpose4 env ==="

echo "Running: pixi run -e cellpose4 python ${SCRIPT_DIR}/process_vasa.py --input ${INPUT_FOLDER} --preproc ${PREPROC_FOLDER} --output ${OUTPUT_FOLDER} --model-path ${VASA_MODEL_PATH} --model-name ${VASA_MODEL_NAME} --px-size ${TARGET_PX_SIZE} --channel-mapping ${CHANNEL_MAPPING} --preprocess"
PIXI_RUN cellpose4 python "${SCRIPT_DIR}/process_vasa.py" \
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

# --- Step 2: TJ segmentation (CellPose 3) ------------------------------------
echo "=== [2/2] TJ segmentation — cellpose3 env ==="

echo "Running: pixi run -e cellpose3 python ${SCRIPT_DIR}/process_tj.py --input ${INPUT_FOLDER} --preproc ${PREPROC_FOLDER} --output ${OUTPUT_FOLDER} --model-path ${TJ_MODEL_PATH} --model-name ${TJ_MODEL_NAME}"
PIXI_RUN cellpose3 python "${SCRIPT_DIR}/process_tj.py" \
    --input      "${INPUT_FOLDER}"    \
    --preproc    "${PREPROC_FOLDER}"  \
    --output     "${OUTPUT_FOLDER}"   \
    --model-path "${TJ_MODEL_PATH}"   \
    --model-name "${TJ_MODEL_NAME}"

if [ $? -ne 0 ]; then
    echo "ERROR: TJ segmentation failed."
    exit 1
fi

# end stat collection and report (these lines go after running after gpu code)
dcgmi stats -x $SLURM_JOBID
dcgmi stats -v -j $SLURM_JOBID

echo "=== Pipeline complete ==="
