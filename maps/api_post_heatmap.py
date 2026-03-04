# maps/api_post_heatmap.py

from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required

from posts.models import Post
from maps.utils_grid import latlon_to_grid

def _aggregate_posts(filter_presence=None):
    """
    投稿をグリッド単位で集計する内部関数。
    filter_presence:
        "present" → いた
        "absent" → いなかった
        None → 両方（total）
    """
    now = timezone.now()
    one_month_ago = now - timedelta(days=30)

    qs = Post.objects.filter(timestamp__gte=one_month_ago)

    if filter_presence in ("present", "absent"):
        qs = qs.filter(presence=filter_presence)

    grid_counts = {}

    for post in qs:
        gx, gy = latlon_to_grid(post.lat, post.lon)
        key = f"{gx},{gy}"

        if key not in grid_counts:
            grid_counts[key] = 0

        grid_counts[key] += 1

    return grid_counts

@login_required
def heatmap_present(request):
    """直近1ヶ月の present（いた）投稿のヒートマップ"""
    data = _aggregate_posts(filter_presence="present")
    return JsonResponse(data)

@login_required
def heatmap_absent(request):
    """直近1ヶ月の absent（いなかった）投稿のヒートマップ"""
    data = _aggregate_posts(filter_presence="absent")
    return JsonResponse(data)

@login_required
def heatmap_total(request):
    """直近1ヶ月の total（present + absent）投稿のヒートマップ"""
    data = _aggregate_posts(filter_presence=None)
    return JsonResponse(data)

@login_required
def heatmap_recommend(request):
    """
    直近1ヶ月の投稿から「投稿が少ない」「present が少ない」グリッドを返す。
    ＝探索おすすめスポット
    """
    # 1. 全投稿（total）
    total = _aggregate_posts(filter_presence=None)

    # 2. present のみ
    present = _aggregate_posts(filter_presence="present")

    # 3. 全グリッドのキー集合
    all_keys = set(total.keys()) | set(present.keys())

    # 4. スコア計算（例：total が少ない + present が少ない）
    recommend = {}

    for key in all_keys:
        total_count = total.get(key, 0)
        present_count = present.get(key, 0)

        # ★ スコア例：投稿が少ないほど高評価
        score = (0 - total_count) + (0 - present_count)

        # total=0 & present=0 の完全空白地帯は特におすすめ
        if total_count == 0 and present_count == 0:
            score -= 5  # もっと優先したいなら調整

        recommend[key] = {
            "total": total_count,
            "present": present_count,
            "score": score,
        }

    return JsonResponse(recommend)
