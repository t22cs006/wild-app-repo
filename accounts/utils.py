from django.db.models import Count, F
from trophy.models import Trophy, UserTrophy
from accounts.models import UserProfile
from posts.models import Post
from collectionmap.models import UserGridCollection
from datetime import date, timedelta

def check_trophies(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    trophies = Trophy.objects.all() # アクティブなものだけに絞るべきかもだが、一旦全取得
    
    # ----------------------------------------------------
    # 事前集計: 毎回クエリ発行を避けるため
    # ----------------------------------------------------
    
    # 1. 連続投稿日数 (UserProfileから取得)
    consecutive_post_days = profile.consecutive_post_days

    # 2. 種類別発見数
    species_data = Post.objects.filter(user=user, presence='present').values('species').annotate(count=Count('id'))
    species_counts = {item['species']: item['count'] for item in species_data}

    # 3. トロフィー獲得数 と 順位
    my_trophy_count = UserTrophy.objects.filter(user=user).count()
    # 自分より多くトロフィーを持っている人の数 + 1
    rank_trophies = UserTrophy.objects.values('user').annotate(cnt=Count('id')).filter(cnt__gt=my_trophy_count).count() + 1

    # 4. 総投稿数 (present + absent) と 順位
    my_post_count = profile.present_count + profile.absent_count
    
    # 自分より投稿数が多い人の数 + 1
    rank_post_count = UserProfile.objects.annotate(
        total_posts=F('present_count') + F('absent_count')
    ).filter(total_posts__gt=my_post_count).count() + 1
    
    # 5. グリッド収集数 (ユニークな場所での投稿数)
    grid_collection_count = UserGridCollection.objects.filter(user=user).count()

    # ----------------------------------------------------
    # トロフィー判定ループ
    # ----------------------------------------------------
    new_trophies = []

    for t in trophies:
        # すでに取得済みならスキップ
        if UserTrophy.objects.filter(user=user, trophy=t).exists():
            continue

        achieved = False

        if t.condition_type == "present_count":
            if profile.present_count >= t.condition_value:
                achieved = True

        elif t.condition_type == "absent_count":
            if profile.absent_count >= t.condition_value:
                achieved = True

        elif t.condition_type == "rare_found":
            if profile.rare_found >= t.condition_value:
                achieved = True

        elif t.condition_type == "login_days":
            if profile.login_days >= t.condition_value:
                achieved = True

        elif t.condition_type == "consecutive_post_days":
            if consecutive_post_days >= t.condition_value:
                achieved = True

        # condition_type 例: "species_シカ", "species_イノシシ"
        elif t.condition_type.startswith("species_"):
            target_species = t.condition_type.replace("species_", "")
            count = species_counts.get(target_species, 0)
            if count >= t.condition_value:
                achieved = True

        # --- 新規・修正箇所 ---

        # 投稿数ランク (上位X位以内)
        elif t.condition_type == "rank_post_count":
            # 足切り導入:
            # 1. 最低でも5件以上の投稿が必要（0件で1位になるのを防ぐ）
            # 2. ログイン日数が3日以上（ぽっと出がいきなりランカーになるのを防ぐ）
            if my_post_count >= 5 and profile.login_days >= 3:
                if 0 < rank_post_count <= t.condition_value:
                    achieved = True

        # トロフィー獲得数
        elif t.condition_type == "trophy_count":
            if my_trophy_count >= t.condition_value:
                achieved = True

        # トロフィー数ランク (上位X位以内)
        elif t.condition_type == "rank_trophies":
            # 足切り導入: 最低3個以上 かつ ログイン3日以上
            if my_trophy_count >= 3 and profile.login_days >= 3:
                if 0 < rank_trophies <= t.condition_value:
                    achieved = True

        # 総投稿数
        elif t.condition_type == "total_post_count":
            if my_post_count >= t.condition_value:
                achieved = True

        # 未開拓エリア投稿数
        elif t.condition_type == "pioneer_count":
            if profile.pioneer_count >= t.condition_value:
                achieved = True

        # 久しぶり投稿数 (リバイバル)
        elif t.condition_type == "revival_count":
            if profile.revival_count >= t.condition_value:
                achieved = True

        # パズルピース収集数 (グリッド数)
        elif t.condition_type == "grid_collection_count":
            if grid_collection_count >= t.condition_value:
                achieved = True

        if achieved:
            UserTrophy.objects.create(user=user, trophy=t)
            new_trophies.append(t)
            
    return new_trophies

def update_login_days(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    today = date.today()

    # すでに今日ログイン処理済みなら何もしない（連続ログインリセット防止）
    if profile.last_login_date == today:
        return

    # 昨日ログインしていた場合のみ +1
    if profile.last_login_date == today - timedelta(days=1):
        profile.login_days += 1
    else:
        # 初回または連続が途切れた場合は 1日目にする
        profile.login_days = 1

    profile.last_login_date = today
    profile.save()
