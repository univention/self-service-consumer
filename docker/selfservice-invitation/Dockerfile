# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base-python
ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20261008@sha256:c50651cd92b620100d4a897f84e1a8976ad50915cd3ff2410c55288dab3b7246
ARG UCS_DISTROLESS_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-distroless-python
ARG UCS_DISTROLESS_IMAGE_TAG=5.3.0-build.20260917@sha256:a965bfba1bb1af8cf0c47d6e436c8a37aaa26ed15b29c9b55636839b2b8436e3

###############################################
# Stage 1: build dependencies and software
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS build
SHELL ["/bin/bash", "-uxo", "pipefail", "-c"]

# Use the glibc-based uv build (not the musl static binary shipped in the
# ghcr.io/astral-sh/uv image) so DNS resolution of internal hosts works.
ADD --checksum=sha256:6426a73c3837e6e2483ee344cbc00f36394d179afcba6183cb77437e67db4af0 \
  https://github.com/astral-sh/uv/releases/download/0.11.26/uv-x86_64-unknown-linux-gnu.tar.gz \
  /tmp/uv.tar.gz
RUN tar -xz --strip-components=1 -C /usr/local/bin/ -f /tmp/uv.tar.gz && \
  rm -f /tmp/uv.tar.gz

ENV UV_LINK_MODE=copy \
  UV_COMPILE_BYTECODE=1 \
  UV_PYTHON_DOWNLOADS=never \
  UV_PYTHON=python3.13

COPY ./pyproject.toml ./uv.lock ./README.md /app/

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache \
  uv sync \
  --locked \
  --no-dev \
  --no-install-project && \
  uv export --no-dev -o ./requirements.txt

# copy source code
COPY ./invitation /app/invitation

RUN uv sync \
  --no-dev \
  --no-editable \
  --frozen

###############################################
# Stage 2: final image
#
# Distroless: no shell, so every instruction here is exec form. The user and
# the CA bundle come from the base image.
FROM ${UCS_DISTROLESS_IMAGE}:${UCS_DISTROLESS_IMAGE_TAG} AS final

ENV PYTHONUNBUFFERED=1 \
  PATH=/app/.venv/bin:$PATH

COPY --from=build /app/.venv /app/.venv
COPY --from=build /app/requirements.txt /app/requirements.txt

WORKDIR /app

# Runs in the shipped image, so a package missing from the venv fails the build and not the pod.
RUN ["python3.13", "-c", "import invitation.__main__"]

CMD ["selfservice-listener"]
