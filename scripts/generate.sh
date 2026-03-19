#!/bin/sh

set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TMP_DIR=$(mktemp -d)
OPENAPI_GENERATOR_IMAGE=${OPENAPI_GENERATOR_IMAGE:-openapitools/openapi-generator-cli:v7.19.0}
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$TMP_DIR/out"
docker run --rm           -v "$ROOT_DIR:/local"           -v "$TMP_DIR/out:/out"           "$OPENAPI_GENERATOR_IMAGE" generate           -i /local/openapi/solver.yaml           -g python           -c /local/openapi-generator.yaml           --global-property apis,models,supportingFiles,apiDocs=false,modelDocs=false,apiTests=false,modelTests=false           -o /out

rm -rf "$ROOT_DIR/agentkata_generated"
cp -R "$TMP_DIR/out/agentkata_generated" "$ROOT_DIR/agentkata_generated"
