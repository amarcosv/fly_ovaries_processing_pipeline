#!/usr/bin/env bash
#
# install_miniforge.sh
#
# Installs Miniforge (conda + mamba) on Linux, non-interactively.
# Skips entirely if any conda is already on PATH, or already installed
# at MINIFORGE_PREFIX (default: ~/miniforge3).
#
# Safe to re-run.
#
set -euo pipefail

MINIFORGE_PREFIX="${MINIFORGE_PREFIX:-$HOME/miniforge3}"

log() { printf '[%(%Y-%m-%d %H:%M:%S)T] %s\n' -1 "$*"; }

if command -v conda >/dev/null 2>&1; then
  log "conda already found on PATH ($(command -v conda)), skipping Miniforge install."
  exit 0
fi

if [[ -x "$MINIFORGE_PREFIX/bin/conda" ]]; then
  log "Miniforge already installed at $MINIFORGE_PREFIX, skipping."
  exit 0
fi

log "Downloading Miniforge installer"
tmp_installer="$(mktemp -d)/Miniforge3-Linux-x86_64.sh"
wget -O "$tmp_installer" https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh

log "Installing Miniforge to $MINIFORGE_PREFIX (batch mode, license auto-accepted)"
bash "$tmp_installer" -b -p "$MINIFORGE_PREFIX"
rm -rf "$(dirname "$tmp_installer")"

# shellcheck disable=SC1091
source "$MINIFORGE_PREFIX/etc/profile.d/conda.sh"
"$MINIFORGE_PREFIX/bin/conda" init bash >/dev/null

log "Done. Restart your shell (or 'source ~/.bashrc') to pick up conda on PATH."
