#!/bin/bash

# 停止 funasr-server 服务
echo "Stopping funasr-server..."

# 查找 funasr-server 进程的 PID
pid=$(ps -ef | grep "funasr-server" | grep -v grep | awk '{print $2}')

if [ -n "$pid" ]; then
    kill $pid
    echo "funasr-server stopped."
else
    echo "funasr-server is not running."
fi

