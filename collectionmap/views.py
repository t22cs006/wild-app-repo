# collectionmap/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from wildlife.constants import CENTER_LAT, CENTER_LON, GRID_SIZE, MIN_LAT, MAX_LAT, MIN_LON, MAX_LON, HALF_LAT_SPAN, HALF_LON_SPAN
from trophy.models import Trophy, UserTrophy
from .models import PuzzleImage
from accounts.models import UserProfile
from posts.models import Post
from django.db.models import Count, F

@login_required
def collectionmap_view(request):
    """
    個人のコレクションマップを表示するビュー。
    実際のデータは /collectionmap/api/my/ から JS が取得する。
    """
    context = {
        'CENTER_LAT': CENTER_LAT,
        'CENTER_LON': CENTER_LON,
        'GRID_SIZE': GRID_SIZE,
        'MIN_LAT': MIN_LAT,
        'MAX_LAT': MAX_LAT,
        'MIN_LON': MIN_LON,
        'MAX_LON': MAX_LON,
        'HALF_LAT_SPAN': HALF_LAT_SPAN,
        'HALF_LON_SPAN': HALF_LON_SPAN,
    }
    return render(request, "collectionmap/collectionmap.html", context)


@login_required
def mycollection_view(request):
    """
    統合されたマイコレクションビュー。
    探索マップ、コレクションパズル、トロフィーの3つのモードを統合。
    """
    mode = request.GET.get('mode', 'explore')  # デフォルトは探索モード
    puzzle = PuzzleImage.objects.first()

    # 基本的な地図定数
    context = {
        'CENTER_LAT': CENTER_LAT,
        'CENTER_LON': CENTER_LON,
        'GRID_SIZE': GRID_SIZE,
        'MIN_LAT': MIN_LAT,
        'MAX_LAT': MAX_LAT,
        'MIN_LON': MIN_LON,
        'MAX_LON': MAX_LON,
        'HALF_LAT_SPAN': HALF_LAT_SPAN,
        'HALF_LON_SPAN': HALF_LON_SPAN,
        'current_mode': mode,
        "puzzle": puzzle,
    }

    # トロフィーモードの場合、トロフィーデータを追加
    if mode == 'trophy':
        user = request.user
        trophies = Trophy.objects.all()
        obtained_trophy_ids = set(
            UserTrophy.objects.filter(user=user)
            .values_list('trophy_id', flat=True)
        )
        user_trophies = UserTrophy.objects.filter(user=user).select_related('trophy')

        # 統計情報の計算
        total_trophies = trophies.count()
        obtained_count = len(obtained_trophy_ids)
        remaining_count = total_trophies - obtained_count

        # --- トロフィーのカテゴライズ ---
        from collections import defaultdict
        grouped_trophies = defaultdict(list)
        
        # カテゴリ定義のマッピング
        CATEGORY_MAP = {
            'login_days': '継続の証',
            'consecutive_post_days': '継続の証',
            'present_count': '出現の証',
            'absent_count': '不在の証',
            'rare_found': '発見の証',
            'species': '発見の証', # species_ は前方一致で判定
            'rank_post_count': '名誉の証',
            'trophy_count': '名誉の証',
            'rank_trophies': '名誉の証',
        }

        # レア度順のソート用マッピング
        RARITY_ORDER = {'bronze': 1, 'silver': 2, 'gold': 3, 'legend': 4}

        for trophy in trophies:
            # カテゴリ決定
            category = 'その他'
            if trophy.condition_type.startswith('species_'):
                category = '発見の証'
            else:
                category = CATEGORY_MAP.get(trophy.condition_type, 'その他')
            
            grouped_trophies[category].append(trophy)

        # 各カテゴリ内でレア度順にソート (bronze -> legend)
        for cat in grouped_trophies:
            grouped_trophies[cat].sort(key=lambda t: RARITY_ORDER.get(t.rarity, 0))

        # 表示したいカテゴリ順序を定義
        display_categories = ['継続の証', '出現の証', '不在の証', '発見の証', '名誉の証', 'その他']
        # 実際にデータがあるものだけをリスト化: [(カテゴリ名, [trophy, ...]), ...]
        sorted_grouped_trophies = []
        for cat_name in display_categories:
            if cat_name in grouped_trophies and grouped_trophies[cat_name]:
                sorted_grouped_trophies.append((cat_name, grouped_trophies[cat_name]))
        
        # 'その他' 以外の未定義カテゴリがあれば追加
        for cat_name, items in grouped_trophies.items():
            if cat_name not in display_categories:
                sorted_grouped_trophies.append((cat_name, items))

        context.update({
            "trophies": trophies, # 互換性のため残す
            "grouped_trophies": sorted_grouped_trophies, # 新しい構造
            "obtained_trophy_ids": obtained_trophy_ids,
            "user_trophies": user_trophies,
            "total_trophies": total_trophies,
            "obtained_count": obtained_count,
            "remaining_count": remaining_count,
        })

        # --- プロフィール・統計情報の追加 ---
        profile, _ = UserProfile.objects.get_or_create(user=user)
        
        # 種類別発見数
        species_data = Post.objects.filter(user=user, presence='present').values('species').annotate(count=Count('id'))
        species_counts = {item['species']: item['count'] for item in species_data}
        
        # ランキング計算
        my_post_count = profile.present_count + profile.absent_count
        rank_post_count = UserProfile.objects.annotate(
            total_posts=F('present_count') + F('absent_count')
        ).filter(total_posts__gt=my_post_count).count() + 1
        
        my_trophy_count = UserTrophy.objects.filter(user=user).count()
        rank_trophies = UserTrophy.objects.values('user').annotate(cnt=Count('id')).filter(cnt__gt=my_trophy_count).count() + 1
        
        context.update({
            "user_profile": profile,
            "species_counts": species_counts,
            "rank_post_count": rank_post_count,
            "rank_trophies": rank_trophies,
        })

    return render(request, "collectionmap/mycollection.html", context)
