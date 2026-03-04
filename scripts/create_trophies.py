import os
import sys
import django

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Django環境の設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wildlife.settings')
django.setup()

from trophy.models import Trophy

# 既存のデータをクリアするかどうか（重複作成エラー防止のため）
Trophy.objects.all().delete()  # 必要に応じてコメントアウトを外す

trophies_data = [
    # --- 連続ログイン ---
    {
        "name": "初ログイン！",
        "description": "初めてログインしました。ようこそ、野生動物調査の世界へ！",
        "condition_type": "login_days",
        "condition_value": 1,
        "rarity": "bronze",
        "icon": "🌟"
    },
    {
        "name": "昨日ぶり！",
        "description": "初めて2日連続でログインしました。明日も待ってます！",
        "condition_type": "login_days",
        "condition_value": 2,  # 連続1日という概念は通常ないので2日から
        "rarity": "bronze",
        "icon": "🌱"
    },
    {
        "name": "三日坊主卒業？",
        "description": "3日連続でログインしました。",
        "condition_type": "login_days",
        "condition_value": 3,
        "rarity": "bronze",
        "icon": "🥉"
    },
    {
        "name": "習慣化の達人",
        "description": "7日連続でログインしました。",
        "condition_type": "login_days",
        "condition_value": 7,
        "rarity": "silver",
        "icon": "🥈"
    },
    {
        "name": "マンスリーチャレンジャー",
        "description": "30日連続でログインしました。すごい！",
        "condition_type": "login_days",
        "condition_value": 30,
        "rarity": "gold",
        "icon": "🥇"
    },

    # --- 投稿数（出現） ---
    {
        "name": "はじめての発見",
        "description": "初めて野生動物の発見情報を投稿しました。",
        "condition_type": "present_count",
        "condition_value": 1,
        "rarity": "bronze",
        "icon": "👀"
    },
    {
        "name": "ラッキー・スリー",
        "description": "発見報告が3回に到達しました。運も実力のうち？",
        "condition_type": "present_count",
        "condition_value": 3,
        "rarity": "bronze",
        "icon": "🍀"
    },
    {
        "name": "森の観察者",
        "description": "発見報告が5回に到達しました。目が慣れてきたようです。",
        "condition_type": "present_count",
        "condition_value": 5,
        "rarity": "bronze",
        "icon": "🔭"
    },
    {
        "name": "見習い調査員",
        "description": "発見報告が10回に到達しました。",
        "condition_type": "present_count",
        "condition_value": 10,
        "rarity": "silver",
        "icon": "📝"
    },
    {
        "name": "凄腕リサーチャー",
        "description": "発見報告が20回に到達しました。確かな調査能力です。",
        "condition_type": "present_count",
        "condition_value": 20,
        "rarity": "silver",
        "icon": "🔎"
    },
    {
        "name": "フィールドの達人",
        "description": "発見報告が30回に到達しました。動物たちの気配を感じ取れます。",
        "condition_type": "present_count",
        "condition_value": 30,
        "rarity": "gold",
        "icon": "🧙"
    },
    {
        "name": "ベテラン調査員",
        "description": "発見報告が50回に到達しました。地域のエキスパートです。",
        "condition_type": "present_count",
        "condition_value": 50,
        "rarity": "gold",
        "icon": "🕵️"
    },
    {
        "name": "伝説の調査員",
        "description": "発見報告が100回に到達しました。野生動物の全てを知る者。",
        "condition_type": "present_count",
        "condition_value": 100,
        "rarity": "legend",
        "icon": "👑"
    },

    # --- 投稿数（不在） ---
    {
        "name": "不在の証明",
        "description": "動物がいなかったことを初めて報告しました。これも重要なデータです。",
        "condition_type": "absent_count",
        "condition_value": 1,
        "rarity": "bronze",
        "icon": "🚫"
    },
    {
        "name": "静寂を見つめて",
        "description": "不在報告5回。少しずつ森の様子がわかってきました。",
        "condition_type": "absent_count",
        "condition_value": 5,
        "rarity": "bronze",
        "icon": "😶"
    },
    {
        "name": "忍耐の調査員",
        "description": "不在報告10回。いないこともまた、発見です。",
        "condition_type": "absent_count",
        "condition_value": 10,
        "rarity": "bronze",
        "icon": "🧘"
    },
    {
        "name": "フィールドキーパー",
        "description": "不在報告20回。地道な調査が大きな価値を生みます。",
        "condition_type": "absent_count",
        "condition_value": 20,
        "rarity": "silver",
        "icon": "🛡️"
    },
    {
        "name": "静寂の記録者",
        "description": "不在報告50回。静かな森を見守り続けました。",
        "condition_type": "absent_count",
        "condition_value": 50,
        "rarity": "silver",
        "icon": "🍃"
    },
    {
        "name": "不在の探求者",
        "description": "不在報告100回。何もない空間から真実を読み解きます。",
        "condition_type": "absent_count",
        "condition_value": 100,
        "rarity": "gold",
        "icon": "🔭"
    },
    
    # --- 総投稿数 (発見+不在) ---
    {
        "name": "フィールドウォーカー",
        "description": "発見と不在を合わせて5回の報告を行いました。",
        "condition_type": "total_post_count",
        "condition_value": 5,
        "rarity": "bronze",
        "icon": "🚶"
    },

    # --- 連続投稿日数 ---
    {
        "name": "調査開始",
        "description": "2日連続で投稿を行いました。",
        "condition_type": "consecutive_post_days",
        "condition_value": 2,
        "rarity": "bronze",
        "icon": "✨"
    },
    {
        "name": "フィールドワークの鬼",
        "description": "3日連続で何らかの投稿を行いました。",
        "condition_type": "consecutive_post_days",
        "condition_value": 3,
        "rarity": "bronze",
        "icon": "🔥"
    },
    {
        "name": "雨の日も風の日も",
        "description": "7日連続で投稿を行いました。素晴らしい継続力です。",
        "condition_type": "consecutive_post_days",
        "condition_value": 7,
        "rarity": "silver",
        "icon": "⛈️"
    },

    # --- 種類別（シカ・タヌキなど） ---
    # タヌキ
    {
        "name": "タヌキ発見！",
        "description": "タヌキを初めて発見しました。",
        "condition_type": "species_タヌキ",
        "condition_value": 1,
        "rarity": "bronze",
        "icon": "🍂"
    },
    {
        "name": "タヌキウォッチャー",
        "description": "タヌキを累計5回発見しました。",
        "condition_type": "species_タヌキ",
        "condition_value": 5,
        "rarity": "bronze",
        "icon": "🍂"
    },
    
    # キツネ
    {
        "name": "キツネ発見！",
        "description": "キツネを初めて発見しました。",
        "condition_type": "species_キツネ",
        "condition_value": 1,
        "rarity": "bronze",
        "icon": "🦊"
    },
     {
        "name": "キツネ追跡者",
        "description": "キツネを累計5回発見しました。",
        "condition_type": "species_キツネ",
        "condition_value": 5,
        "rarity": "bronze",
        "icon": "🦊"
    },
    
    # シカ
    {
        "name": "シカ発見！",
        "description": "シカを初めて発見しました。",
        "condition_type": "species_シカ",
        "condition_value": 1,
        "rarity": "bronze",
        "icon": "🦌"
    },
    {
        "name": "シカ愛好家",
        "description": "シカを累計5回発見しました。",
        "condition_type": "species_シカ",
        "condition_value": 5,
        "rarity": "bronze",
        "icon": "🦌"
    },
    {
        "name": "シカマスター",
        "description": "シカを累計20回発見しました。",
        "condition_type": "species_シカ",
        "condition_value": 20,
        "rarity": "silver",
        "icon": "🦌"
    },

    # イノシシ
    {
        "name": "イノシシ発見！",
        "description": "イノシシを初めて発見しました。",
        "condition_type": "species_イノシシ",
        "condition_value": 1,
        "rarity": "bronze",
        "icon": "🐗"
    },
    {
        "name": "うり坊ファン",
        "description": "イノシシを累計5回発見しました。",
        "condition_type": "species_イノシシ",
        "condition_value": 5,
        "rarity": "bronze",
        "icon": "🐗"
    },

    # サル
    {
        "name": "サル発見！",
        "description": "サルを初めて発見しました。",
        "condition_type": "species_サル",
        "condition_value": 1,
        "rarity": "bronze",
        "icon": "🐵"
    },
    {
        "name": "サルの監視員",
        "description": "サルを累計5回発見しました。",
        "condition_type": "species_サル",
        "condition_value": 5,
        "rarity": "bronze",
        "icon": "🐵"
    },

    # クマ
    {
        "name": "クマ遭遇",
        "description": "クマを初めて発見しました。安全に気をつけて！",
        "condition_type": "species_クマ",
        "condition_value": 1,
        "rarity": "silver",
        "icon": "🐻"
    },
    {
        "name": "森のぬし",
        "description": "クマを累計5回発見しました。",
        "condition_type": "species_クマ",
        "condition_value": 5,
        "rarity": "gold",
        "icon": "🐻"
    },

    # ハクビシン
    {
        "name": "ハクビシン発見！",
        "description": "ハクビシンを初めて発見しました。",
        "condition_type": "species_ハクビシン",
        "condition_value": 1,
        "rarity": "bronze",
        "icon": "🍈"
    },

    # アライグマ
    {
        "name": "アライグマ発見！",
        "description": "アライグマを初めて発見しました。",
        "condition_type": "species_アライグマ",
        "condition_value": 1,
        "rarity": "bronze",
        "icon": "🦝"
    },

    # --- トロフィー収集数 ---
    {
        "name": "コレクター",
        "description": "トロフィーを5個集めました。",
        "condition_type": "trophy_count",
        "condition_value": 5,
        "rarity": "bronze",
        "icon": "🎒"
    },
    {
        "name": "博物館長",
        "description": "トロフィーを10個集めました。",
        "condition_type": "trophy_count",
        "condition_value": 10,
        "rarity": "silver",
        "icon": "🏛️"
    },

    # --- 総合ランキング（投稿数） ---
    {
        "name": "トップ100",
        "description": "投稿数ランキングで100位以内に入りました。",
        "condition_type": "rank_post_count",
        "condition_value": 100,
        "rarity": "bronze",
        "icon": "🏅"
    },
    {
        "name": "トップ50",
        "description": "投稿数ランキングで50位以内に入りました。",
        "condition_type": "rank_post_count",
        "condition_value": 50,
        "rarity": "silver",
        "icon": "🥈"
    },
    {
        "name": "トップランカー",
        "description": "投稿数ランキングで3位以内に入りました。",
        "condition_type": "rank_post_count",
        "condition_value": 3,
        "rarity": "gold",
        "icon": "🏆"
    },
    {
        "name": "森の王者",
        "description": "投稿数ランキングで1位になりました！",
        "condition_type": "rank_post_count",
        "condition_value": 1,
        "rarity": "legend",
        "icon": "👑"
    },

    # --- トロフィーランキング ---
    {
        "name": "有望コレクター",
        "description": "トロフィー所持数ランキングで100位以内に入りました。",
        "condition_type": "rank_trophies",
        "condition_value": 100,
        "rarity": "bronze",
        "icon": "🎫"
    },
    {
        "name": "一流コレクター",
        "description": "トロフィー所持数ランキングで50位以内に入りました。",
        "condition_type": "rank_trophies",
        "condition_value": 50,
        "rarity": "silver",
        "icon": "🎖️"
    },
    {
        "name": "エリートコレクター",
        "description": "トロフィー所持数ランキングで3位以内に入りました。",
        "condition_type": "rank_trophies",
        "condition_value": 3,
        "rarity": "gold",
        "icon": "🏵️"
    },
    {
        "name": "生きる伝説",
        "description": "トロフィー所持数ランキングで1位になりました！",
        "condition_type": "rank_trophies",
        "condition_value": 1,
        "rarity": "legend",
        "icon": "⚜️"
    },

    # --- 未開拓地開拓 (Pioneer) ---
    {
        "name": "開拓者",
        "description": "まだ情報の少ない場所（投稿5件以下）で初めて調査を行いました。",
        "condition_type": "pioneer_count",
        "condition_value": 1,
        "rarity": "bronze",
        "icon": "🚩"
    },
    {
        "name": "冒険家",
        "description": "情報の少ない場所で5回調査を行いました。新たな地図を作るのはあなたです。",
        "condition_type": "pioneer_count",
        "condition_value": 5,
        "rarity": "silver",
        "icon": "🗺️"
    },
    {
        "name": "フロンティアスピリット",
        "description": "情報の少ない場所で20回調査を行いました。未知への挑戦に敬意を表します。",
        "condition_type": "pioneer_count",
        "condition_value": 20,
        "rarity": "gold",
        "icon": "🏔️"
    },

    # --- 久しぶりの調査 (Revival) ---
    {
        "name": "再発見の喜び",
        "description": "1ヶ月以上情報のなかった場所で調査を行いました。",
        "condition_type": "revival_count",
        "condition_value": 1,
        "rarity": "bronze",
        "icon": "🕰️"
    },
    {
        "name": "森の定点観測者",
        "description": "1ヶ月以上情報のなかった場所で5回調査を行いました。変化を見逃しません。",
        "condition_type": "revival_count",
        "condition_value": 5,
        "rarity": "silver",
        "icon": "🔭"
    },

    # --- パズル収集 (Grid Collection) ---
    {
        "name": "グリッドビギナー",
        "description": "コレクションマップのピースを5つ集めました。コレクションの始まりです。",
        "condition_type": "grid_collection_count",
        "condition_value": 5,
        "rarity": "bronze",
        "icon": "🧩"
    },
    {
        "name": "グリッドエクスプローラー",
        "description": "コレクションマップのピースを20個集めました。地図が鮮やかになってきました。",
        "condition_type": "grid_collection_count",
        "condition_value": 20,
        "rarity": "silver",
        "icon": "🗺️"
    },
    {
        "name": "グリッドマスター",
        "description": "コレクションマップのピースを50個集めました。素晴らしい収集能力です！",
        "condition_type": "grid_collection_count",
        "condition_value": 50,
        "rarity": "gold",
        "icon": "🖼️"
    }
]

created_count = 0
for data in trophies_data:
    obj, created = Trophy.objects.get_or_create(
        name=data["name"],
        defaults=data
    )
    if created:
        print(f"Created: {obj.name}")
        created_count += 1
    else:
        print(f"Skipped (exists): {obj.name}")

print(f"\n完了: {created_count} 個のトロフィーを作成しました。")
