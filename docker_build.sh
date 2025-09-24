#!/bin/bash

# 使用绝对路径避免问题
PROJECT_DIR=$(realpath .)
IMAGE="kivy/kivy:android"
TAG="latest"

echo "开始使用 Docker 构建 Android 应用..."
echo "项目目录: $PROJECT_DIR"

# 确保所有路径变量都用双引号包裹
docker run -it --rm \
  -v "$PROJECT_DIR":/host \
  -v "$HOME/.buildozer":/home/user/.buildozer \
  "$IMAGE:$TAG" \
  buildozer -v android debug