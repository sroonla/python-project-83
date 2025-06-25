#!/usr/bin/env bash
set -e

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Debug info
echo "Python path: $(which python)"
echo "Python version: $(python --version)"
echo "PATH: $PATH"

# Install dependencies globally
uv pip install --system -e .

# List installed packages
uv pip freeze