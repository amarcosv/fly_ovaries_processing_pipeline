#!/usr/bin/env bash
#
# install_pixi_envs.sh
#
# Installs pixi (if not already present) and then installs the cellpose3
# and cellpose4 environments defined in pixi.toml (same directory as this
# script). Does not touch conda/Miniforge — see install_miniforge.sh for
# that, if you need it for anything else.
#
# Safe to re-run: each step is skipped/idempotent if already done.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log() { printf '[%(%Y-%m-%d %H:%M:%S)T] %s\n' -1 "$*"; }

# Binary + package cache go on a lab share (like Miniforge at
# /lab/keck_scratch/miniforge3), not $HOME, so they don't eat home quota
# and the download cache can be reused across lab members/projects.
# Set PIXI_HOME beforehand to skip this prompt (e.g. for non-interactive runs).
if [[ -z "${PIXI_HOME:-}" ]]; then
  default_pixi_home="$HOME/.pixi"
  read -rp "Path to install pixi (binary + cache) [default: $default_pixi_home]: " pixi_home_input
  PIXI_HOME="${pixi_home_input:-$default_pixi_home}"
fi
export PIXI_HOME
log "Using PIXI_HOME=$PIXI_HOME"

# ---------------------------------------------------------------------------
# 1. pixi
# ---------------------------------------------------------------------------
export PATH="$PIXI_HOME/bin:$PATH"

if command -v pixi >/dev/null 2>&1; then
  log "pixi already installed: $(pixi --version)"
else
  log "Installing pixi to $PIXI_HOME"
  curl -fsSL https://pixi.sh/install.sh | sh
fi

# ---------------------------------------------------------------------------
# 2. Install the cellpose environments
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
log "Restart your shell (or 'source ~/.bashrc') to pick up pixi on PATH permanently."
