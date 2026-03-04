from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Trophy, UserTrophy


@login_required
def trophy_list(request):
    """
    ユーザーのトロフィー一覧を表示するビュー。
    取得済みトロフィーと未取得トロフィーを区別して表示。
    """
    user = request.user

    # 全てのトロフィーを取得
    trophies = Trophy.objects.all()

    # ユーザーが取得済みのトロフィーIDを取得
    obtained_trophy_ids = set(
        UserTrophy.objects.filter(user=user)
        .values_list('trophy_id', flat=True)
    )

    # 取得済みのUserTrophyオブジェクトを取得（詳細情報が必要な場合）
    user_trophies = UserTrophy.objects.filter(user=user).select_related('trophy')

    # 統計情報の計算
    total_trophies = trophies.count()
    obtained_count = len(obtained_trophy_ids)
    remaining_count = total_trophies - obtained_count

    context = {
        "trophies": trophies,
        "obtained_trophy_ids": obtained_trophy_ids,
        "user_trophies": user_trophies,
        "total_trophies": total_trophies,
        "obtained_count": obtained_count,
        "remaining_count": remaining_count,
    }
    return render(request, "trophy/trophy_list.html", context)
