# syntax=docker/dockerfile:1
ARG NODE_IMAGE=node:22.22.0-bookworm-slim
FROM ${NODE_IMAGE} AS toolchain
ARG TARGETARCH
# The pinned Blender release supplies a Linux x86-64 archive.
RUN test "$TARGETARCH" = amd64
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl xz-utils python3 python3-pil fonts-dejavu-core \
    libx11-6 libxrender1 libxxf86vm1 libxfixes3 libxi6 libxkbcommon0 libsm6 libice6 \
    libgl1 libegl1 libdbus-1-3 libgomp1 libasound2 \
    && rm -rf /var/lib/apt/lists/*
RUN curl --fail --location --retry 3 \
      https://download.blender.org/release/Blender4.2/blender-4.2.3-linux-x64.tar.xz \
      -o /tmp/blender.tar.xz \
    && echo '3a64efd1982465395abab4259b4091d5c8c56054c7267e9633e4f702a71ea3f4  /tmp/blender.tar.xz' | sha256sum -c - \
    && mkdir /opt/blender \
    && tar -xJf /tmp/blender.tar.xz -C /opt/blender --strip-components=1 \
    && rm /tmp/blender.tar.xz \
    && /opt/blender/blender --version
ENV BLENDER_BIN=/opt/blender/blender
WORKDIR /project

FROM toolchain AS models
COPY source/ source/
COPY shared/ shared/
COPY rooms/ rooms/
COPY house/ house/
COPY scripts/ scripts/
# The catalog also validates that navigation adapters exist.
COPY web/lib/rooms/ web/lib/rooms/
RUN python3 scripts/build.py all --assets-only

FROM toolchain AS dependencies
COPY web/package.json web/package-lock.json web/
RUN cd web && npm ci

FROM models AS build
COPY --from=dependencies /project/web/node_modules/ web/node_modules/
COPY web/ web/
RUN cd web && npm run build && npm run typecheck
RUN cd web && npx playwright test tests/first-floor.spec.ts tests/doors.spec.ts tests/shared-assets.spec.ts tests/public-asset.spec.ts tests/portals.spec.ts tests/upper-floor.spec.ts tests/ladders.spec.ts tests/wire-attic.spec.ts
RUN python3 scripts/build.py export /artifacts

# Pages needs only the website, not editable Blender scenes or reports.
FROM scratch AS pages
COPY --from=build /project/web/dist/client/ /

# Export files, without shipping Blender or node_modules with the website.
FROM scratch AS artifacts
COPY --from=build /artifacts/ /
