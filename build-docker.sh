#!/bin/bash

VERSION="$(cat ./VERSION)"
echo "$VERSION"

docker build . \
    --platform=linux/amd64 \
    --tag "registry.pwt5ca.me/zener/zener:$VERSION" \
    --tag "registry.pwt5ca.me/zener/zener:latest" \
    --push
