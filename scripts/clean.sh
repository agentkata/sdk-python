#!/bin/sh

set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
rm -rf "$ROOT_DIR/build" "$ROOT_DIR/dist" "$ROOT_DIR"/*.egg-info
