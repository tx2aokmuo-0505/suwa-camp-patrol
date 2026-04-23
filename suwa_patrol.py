name: Suwa Patrol

on:
  schedule:
    # 15分おきに実行する設定 (日本時間だと 00分, 15分, 30分, 45分)
    - cron: '*/15 * * * *'
  workflow_dispatch:      # GitHubの画面から手動で実行ボタンを押せるようにする

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write    # 履歴ファイル(txt)を保存するために必要な権限
    
    steps:
      # 1. あなたのリポジトリにあるコードを読み込む
      - name: Checkout code
        uses: actions/checkout@v4

      # 2. Pythonを使えるようにセットアップ
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.9'
          cache: 'pip'

      # 3. 必要なライブラリ(requests, bs4)をインストール
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # 4. パトロールプログラムを実行
      - name: Run script
        env:
          DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
        run: python suwa_patrol.py

      # 5. 実行結果（パトロール回数やメッセージ履歴）を保存してリポジトリに反映
      - name: Commit and push changes
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add sent_messages.txt message_history.txt
          git commit -m "Update patrol status [skip ci]" || exit 0
          git push
