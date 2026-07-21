# Installing and running the pipeline (Mikala)

## 1. Install

**Create a folder and clone the repo**
```bash
cd /lab/keck_scratch
cd Mikala/
mkdir env_test
cd env_test/
git clone https://github.com/amarcosv/fly_ovaries_processing_pipeline.git
cd fly_ovaries_processing_pipeline/envs
chmod +x *.sh
```

**Log into a GPU node** — the install script runs GPU checks, so it needs to run on a node with a GPU, not the login node:
```bash
srun -p nvidia-t4-20 --gres=gpu:1 --cpus-per-task=6 --mem=64gb --pty bash -i
```

**Install the pixi environments**
Make sure you are on the fly_ovaries_processing_pipeline/envs folder
```bash
./install_pixi_envs.sh
```
You'll be prompted for a pixi install directory (binary + package cache). Point this at a lab share, not your home directory — same reasoning as the Miniforge install: home quotas are small, and a shared cache avoids everyone re-downloading multi-GB CUDA/torch packages.

This installs both the `cellpose3` and `cellpose4` environments and runs a GPU + cellpose sanity check for each.

## 2. Run the pipeline

```bash
cd /lab/keck_scratch/Mikala/env_test/fly_ovaries_processing_pipeline/src/slurm_pipeline
ls
```

Open `run_pipeline.sh` and edit the paths at the top (input/output data directories, job name — whatever's specific to your run) before submitting.

**Submit:**
```bash
sbatch run_pipeline.sh
```

**Check status:**
```bash
squeue --me
srun --jobid=JOBID nvidia-smi
```

**Cancel:**
```bash
scancel <jobid>
# or
scancel -n <jobname>
```

## 3. Jupyter

Go to [midori.wi.mit.edu](https://midori.wi.mit.edu).

## 4. Update the repository

```bash
cd /lab/keck_scratch/Mikala/env_test/fly_ovaries_processing_pipeline
git fetch
git reset --hard origin/main
```

> ⚠️ **Warning:** `git reset --hard` discards any local changes to tracked files, including edits to `.sh` scripts. If you've customized paths in `run_pipeline.sh` or anything else in the repo, back those up (or commit/stash them) before updating, or you'll lose them.
