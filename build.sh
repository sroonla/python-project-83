#!/usr/bin/env bash

set -e

# Установка uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Установка зависимостей
uv pip install --system -e .
