#!/usr/bin/env bash

# Configure, build and run all tests

set -euo pipefail

PROJECT_DIR=$(
  cd "$(dirname "$0")"/../..
  pwd
)

conan install \
  --build missing \
  --env CONAN_CMAKE_GENERATOR=Ninja \
  "${PROJECT_DIR}" \
  "$@"

conan build \
  --build \
  --configure \
  --test \
  "${PROJECT_DIR}"
