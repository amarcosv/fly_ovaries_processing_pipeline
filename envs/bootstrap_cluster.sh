#!/usr/bin/env bash
#
# bootstrap_cluster.sh
#
# One-shot setup for a Linux GPU cluster node:
#   1. Install Miniforge (conda/mamba) if not already present
#   2. Install pixi if not already present
#   3. Run `pixi install` for the cellpose3 and cellpose4 environments
#      defined in pixi.toml (same directory as this script)
#
# Safe to re-run: each step is skipped if already done.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MINIFORGE_PREFIX="${MINIFORGE_PREFIX:-$HOME/miniforge3}"

log() { printf '[%(%Y-%m-%d %H:%M:%S)T] %s\n' -1 "$*"; }

# ---------------------------------------------------------------------------
# 1. Miniforge (skip entirely if any conda is already on PATH)
# ---------------------------------------------------------------------------
if command -v conda >/dev/null 2>&1; then
  log "conda already found on PATH ($(command -v conda)), skipping Miniforge install."
elif [[ -x "$MINIFORGE_PREFIX/bin/conda" ]]; then
  log "Miniforge already installed at $MINIFORGE_PREFIX, skipping."
  # shellcheck disable=SC1091
  source "$MINIFORGE_PREFIX/etc/profile.d/conda.sh"
else
  log "Downloading Miniforge installer"
  tmp_installer="$(mktemp -d)/Miniforge3-Linux-x86_64.sh"
  wget -O "$tmp_installer" https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh

  log "Installing Miniforge to $MINIFORGE_PREFIX (batch mode, license auto-accepted)"
  bash "$tmp_installer" -b -p "$MINIFORGE_PREFIX"
  rm -rf "$(dirname "$tmp_installer")"

  # shellcheck disable=SC1091
  source "$MINIFORGE_PREFIX/etc/profile.d/conda.sh"
  "$MINIFORGE_PREFIX/bin/conda" init bash >/dev/null
fi

# ---------------------------------------------------------------------------
# 2. pixi
# ---------------------------------------------------------------------------
export PATH="$HOME/.pixi/bin:$PATH"

if command -v pixi >/dev/null 2>&1; then
  log "pixi already installed: $(pixi --version)"
else
  log "Installing pixi"
  curl -fsSL https://pixi.sh/install.sh | sh
fi

# ---------------------------------------------------------------------------
# 3. Install the cellpose environments
# ---------------------------------------------------------------------------
cd "$SCRIPT_DIR"
log "Installing cellpose3 environment"
pixi install -e cellpose3
pixi run -e cellpose3 check-gpu
pixi run -e cellpose3 check-cellpose

log "Installing cellpose4 environment"
pixi install -e cellpose4
pixi run -e cellpose4 check-gpu
pixi run -e cellpose4 check-cellpose

log "Done. Use: pixi shell -e cellpose3   (or cellpose4)   from $SCRIPT_DIR"
log "Restart your shell (or 'source ~/.bashrc') to pick up conda/pixi on PATH permanently."
