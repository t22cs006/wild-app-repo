Wild App（市民参加型・野生動物観測投稿Webアプリ）

本リポジトリは、卒業研究で開発した投稿型Webアプリ（Django）である。
スマートフォンのブラウザから観測記録（発見／不在）を投稿し、投稿密度ヒートマップおよびトロフィー表示により行動を支援する。

【主な機能】
- 観測記録の投稿（発見／不在）
- 一括不在投稿（複数地点をまとめて不在として登録）
- 投稿密度ヒートマップ表示（Leaflet + OpenStreetMap）
- 危険区域グリッドの表示（安全配慮のための上書き表示）
- トロフィー表示（Myコレクション）と獲得条件の提示

【開発・動作環境（概要）】
- 開発：Windows 11 / Visual Studio Code
- バックエンド：Python / Django
- フロントエンド：HTML / JavaScript
- 地図表示：Leaflet（背景地図：OpenStreetMap）
- 動作想定：スマートフォンのブラウザ

【セットアップ手順（Windows / PowerShell）】
前提：プロジェクトルート（manage.py と requirements.txt がある場所）で実行する。

1) 仮想環境の作成と有効化
python -m venv venv
.\venv\Scripts\Activate.ps1

2) 依存パッケージのインストール
pip install --upgrade pip
pip install -r requirements.txt

3) DB初期化（マイグレーション）
python manage.py makemigrations
python manage.py migrate

4) 管理者ユーザー作成（admin）
python manage.py createsuperuser

5) トロフィー初期データ作成
python scripts\create_trophies.py

6) 開発サーバ起動
python manage.py runserver

【動作確認（ブラウザ）】
- トップ： http://127.0.0.1:8000/
- 管理画面： http://127.0.0.1:8000/admin/

【ディレクトリ構成（主要）】
- wildlife/ : Djangoプロジェクト設定
- posts/ : 投稿（発見／不在／一括不在）
- maps/ : ヒートマップ表示
- dangergrid/ : 危険区域グリッド
- trophy/ : トロフィー定義・判定・表示
- collectionmap/ : MYコレクション（パズル表示）
- accounts/ : ユーザー・利用状況集計
- scripts/ : 管理用スクリプト（例：トロフィー生成）

【注意】
- 本リポジトリは卒業研究の成果物として公開している。実運用を行う場合は、SECRET_KEY などの設定を環境変数で管理すること。
- OpenStreetMap を表示する場合は、クレジット表記（© OpenStreetMap contributors）を維持すること。

【ライセンス・クレジット】
- Map data © OpenStreetMap contributors
- Licence: ODbL 1.0（https://www.openstreetmap.org/copyright）