#!/usr/bin/env bash
# 停止头脑风暴服务器并清理
# 用法: stop-server.sh <session_dir>
#
# 结束服务器进程。仅当会话目录位于 /tmp（临时）时才删除；
# 持久目录（.superpowers/）保留，便于日后查看线框。

SESSION_DIR="$1"

if [[ -z "$SESSION_DIR" ]]; then
  echo '{"error": "用法: stop-server.sh <session_dir>"}'
  exit 1
fi

STATE_DIR="${SESSION_DIR}/state"
PID_FILE="${STATE_DIR}/server.pid"

if [[ -f "$PID_FILE" ]]; then
  pid=$(cat "$PID_FILE")

  # 先尝试优雅停止，仍存活则强制结束
  kill "$pid" 2>/dev/null || true

  # 等待优雅退出（约 2 秒内）
  for i in {1..20}; do
    if ! kill -0 "$pid" 2>/dev/null; then
      break
    fi
    sleep 0.1
  done

  # 若仍在运行，升级为 SIGKILL
  if kill -0 "$pid" 2>/dev/null; then
    kill -9 "$pid" 2>/dev/null || true

    # 稍候以使 SIGKILL 生效
    sleep 0.1
  fi

  if kill -0 "$pid" 2>/dev/null; then
    echo '{"status": "failed", "error": "进程仍在运行"}'
    exit 1
  fi

  rm -f "$PID_FILE" "${STATE_DIR}/server.log"

  # 仅删除 /tmp 下的临时目录
  if [[ "$SESSION_DIR" == /tmp/* ]]; then
    rm -rf "$SESSION_DIR"
  fi

  echo '{"status": "stopped"}'
else
  echo '{"status": "not_running"}'
fi
