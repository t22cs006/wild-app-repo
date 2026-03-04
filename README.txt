🐾 野生動物観測アプリ（Wild App）仕様書

このアプリは、地図上で野生動物の 発見 / 不在 を記録し、そのデータを収集・可視化する Django アプリケーションです。
単なる記録だけでなく、ゲーミフィケーション（トロフィー・パズル）を通じて、ユーザーが自発的に「未開拓エリア」や「再調査が必要なエリア」へ向かうよう設計されています。

---

🚀 機能概要

1. 観測報告（Posting）
   - 単数投稿モード
     - 発見（Present） / 不在（Absent）の選択
     - 動物種の選択（AI判定のプレースホルダーあり）
     - 画像アップロード（スマホ対応：カメラ起動/ライブラリ選択）
     - 現在地取得（地図上のボタンからワンタップで入力・移動）
   - 一括投稿モード（Bulk Post）
     - 地図上で複数の移動ルート（グリッド）を選択し、まとめて「不在」として登録
     - パトロール時の効率的なデータ入力用

2. 地図・データ可視化（Visualization）
   - ヒートマップダッシュボード
     - Presentマップ： 目撃情報の密度（赤）
     - Absentマップ： 不在情報の密度（青）
     - Totalマップ： 観測密度。色が薄い場所（投稿数5未満）は開拓のチャンスとして可視化
     - Recommendマップ： 「未開拓（Pioneer）」や「再調査（Revival）」が必要な場所を戦略的に表示
   - グリッドシステム
     - 250m四方のメッシュを基準とする
     - ズームレベルに応じて 500m / 750m に自動集約表示
     - 広域表示時にクリックすると自動で詳細ズーム（Zoom 15）へ移動
   - Danger Grid
     - 立ち入り危険エリア等の情報を地図上にオーバーレイ表示

3. ゲーミフィケーション（Gamification）
   - トロフィーシステム
     ユーザーの以下の行動に対してトロフィーを付与
     - 継続性： 連続ログイン、連続投稿
     - 貢献度： 投稿数ランキング、トロフィー収集数
     - コンテキスト検知（Context-Aware）：
       - Pioneer（開拓者）： 投稿数が少ない（<=5）場所への投稿
       - Revival（再発見）： 1ヶ月以上更新がない場所への投稿
       - Grid Collection（パズル）： ユニークな場所での投稿数（5/20/50箇所）
   - MYコレクション（My Collection）
     - 自身の訪れた場所がパズルのピースとして埋まっていく「コレクションパズル」
     - 獲得したトロフィーの一覧表示
     - プロフィール・ランク確認モーダル

4. ユーザー導線（UX Design）
   - ダッシュボード
     - 「未開拓エリア」「久しぶりの場所」「コレクション収集」をミッションとして提示
     - 「いた」も「いなかった」も価値があることを明記し、投稿ハードルを下げる

---

🛠 技術スタック

- Backend: Python / Django
- Database: SQLite (開発用)
- Frontend: Django Templates, HTML/CSS/JS
- Map Engine: Leaflet.js
- Spatial Utils: Shapely, NumPy (グリッド計算)
- Image Processing: Pillow / piexif

---

💻 インストール・セットアップ手順 詳細

【A】 開発環境（ローカル Windows/Mac）

1. プロジェクトの準備
   # Gitリポジトリからクローンする場合
   git clone <repository_url>
   cd wild-app

2. 仮想環境の作成と有効化（推奨）
   # Windows (PowerShell)
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     # ※権限エラーが出る場合は: Set-ExecutionPolicy RemoteSigned Scope Process
   
   # Mac / Linux
     python3 -m venv venv
     source venv/bin/activate

3. 依存パッケージのインストール
   pip install --upgrade pip
   pip install -r requirements.txt
   
   # パッケージ確認
   pip list

4. データベースの初期化（マイグレーション）
   python manage.py migrate

5. 初期データの投入【重要】
   # トロフィーデータの作成（必須）
   python scripts/create_trophies.py
   
   # 管理者ユーザーの作成（任意）
   python manage.py createsuperuser

6. 開発サーバの起動
   python manage.py runserver
   # ブラウザで http://127.0.0.1:8000 にアクセス


【B】 本番環境（PythonAnywhere）でのデプロイ・更新手順

1. コンソールでの更新作業
   # Bash Console を開き、プロジェクトディレクトリへ移動
   cd ~/wild-app  (※ユーザー環境に合わせてパスを変更)
   
   # 最新コードを取得
   git pull origin main
   git pull #だけでいいかも

2. 仮想環境での作業
   # 事前に作成した仮想環境を有効化 (例: myenv)
   workon myenv
   # または: source /home/username/.virtualenvs/myenv/bin/activate

   # 新しいライブラリがある場合
   pip install -r requirements.txt

3. データベース・静的ファイルの更新
   # DB定義の更新
   python manage.py migrate

   # サーバー用静的ファイルの収集（CSS/JSの変更反映）
   python manage.py collectstatic --noinput

   # トロフィーデータの更新（定義追加・変更時）
   python scripts/create_trophies.py

4. アプリケーションの再起動
   # Webタブ画面下部の「Reload」ボタンを押す
   # またはコンソールでWebアプリのWSGIファイルを更新（リロードトリガー）
   # touch /var/www/username_pythonanywhere_com_wsgi.py

---

📊 ユーザビリティ評価と検証計画

本アプリケーションの有効性を検証するため、以下の観点で評価・実験を行うことを想定しています。

1. 評価の目的
   - 行動変容の確認：可視化（ヒートマップ・パズル）によって、ユーザーが自発的に「空白エリア」へ向かうか？
   - モチベーション：ゲーミフィケーション（トロフィー）が継続的な利用意欲につながるか？
   - 受容性：システムは直感的で、参加のハードルは低いか？

2. 評価手法
   A. タスクベースの観察・インタビュー
      - シナリオ：「ダッシュボードのヒートマップを確認し、次の調査目的地を決定してください」
      - 測定指標：被験者が「色の薄い場所（未開拓地）」や「おすすめエリア」を意図的に選択した割合。
   
   B. SUS (System Usability Scale) アンケート
      - システムの客観的な使いやすさを0-100点でスコアリングし、ユーザビリティ上の問題点を特定する。

   C. 独自の心理指標アンケート（5段階評価）
      - 「地図の空白（未パズル部分）を埋めたいと感じたか」
      - 「『開拓者』などのトロフィー条件が、新しい場所へ行く動機になったか」
      - 「『いた』だけでなく『いなかった』情報の投稿も重要だと理解できたか」

3. 期待される成果
   - 市民参加型調査における課題である「データの地理的・時間的な偏り」を、ゲーミフィケーションを用いたUI/UXデザインによって是正できる可能性を示す。


---

📂 ディレクトリ構造の要点

- accounts/       : ユーザープロファイル、統計情報（ログイン日数など）
- collectionmap/  : MYコレクション（パズル表示）、トロフィーボード
- maps/           : ヒートマップ表示、Danger Grid API
- posts/          : 投稿機能（作成、保存、一括登録）
- trophy/         : トロフィー定義、獲得ロジック
- scripts/        : 管理用スクリプト（トロフィー生成など）

---

📝 その他メモ
- Leaflet のタイルは OpenStreetMap を使用
- Danger Grid データは JSON 形式で管理
- 一括投稿の結果表示には Django Session を使用してデータを受け渡し
