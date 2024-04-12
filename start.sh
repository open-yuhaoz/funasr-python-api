#!/bin/bash

# 启动 funasr-server 服务
echo "Starting funasr-server..."

# 运行可执行文件
nohup ./funasr-server > funasr-server.log 2>&1 &

echo "funasr-server started."
