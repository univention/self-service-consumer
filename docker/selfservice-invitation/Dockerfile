# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base-python
ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20260702@sha256:8787ee424a1322ba25fa285f1840fe4bba62d7ec1f44a14a39b6e2024ad3e735

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
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS final
SHELL ["/bin/bash", "-uxo", "pipefail", "-c"]

ENV PYTHONUNBUFFERED=1 \
  PATH=/app/.venv/bin:$PATH

ARG USER=selfservice
RUN rm -fv /usr/lib/python*/EXTERNALLY-MANAGED && \
  rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/* && \
  groupadd -r ${USER} -g 1000 && \
  useradd -r -d /app -g ${USER} -N ${USER} -u 1000

COPY --from=build --chown=${USER}:${USER} /app /app

USER ${USER}
WORKDIR /app

CMD ["selfservice-listener"]

RUN \
  python3.13 -V && \
  python3.13 -m site && \
  python3.13 -c 'import invitation'
