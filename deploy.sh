#!/bin/bash

# === 設定專案資訊 ===
REPO_URL="https://github.com/miku0219/ME2025_Midterm3.git"  # 改成你的 Git Repository URL
PROJECT_DIR="order_management"      # 專案資料夾名稱
VENV_DIR=".venv"                     # 虛擬環境名稱
APP_FILE="app.py"                    # 主程式

# === 檢查專案資料夾是否存在 ===
if [ ! -d "$PROJECT_DIR" ]; then
    echo "首次執行：Clone 專案..."
    git clone "$REPO_URL" "$PROJECT_DIR"
fi

cd "$PROJECT_DIR" || exit

# === 檢查虛擬環境是否存在 ===
if [ ! -d "$VENV_DIR" ]; then
    echo "建立虛擬環境..."
    python3 -m venv "$VENV_DIR"
fi

# === 啟動虛擬環境 ===
source "$VENV_DIR/bin/activate"

# === 安裝/更新套件 ===
echo "安裝或更新 requirements.txt 中的套件..."
pip install --upgrade pip
pip install -r requirements.txt

# === 專案更新 (git pull) ===
if [ -d ".git" ]; then
    echo "更新專案版本..."
    git pull
fi

# === 找出是否已經有 app.py 運行，並重啟 ===
APP_PID=$(pgrep -f "python.*$APP_FILE")
if [ ! -z "$APP_PID" ]; then
    echo "重啟 app.py (PID: $APP_PID)..."
    kill -9 $APP_PID
fi

# === 啟動應用程式 (背景執行) ===
echo "啟動 app.py..."
nohup python "$APP_FILE" > app.log 2>&1 &

echo "部署完成！"
