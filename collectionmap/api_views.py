# collectionmap/api_views.py

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import UserGridCollection

@login_required
def my_collection_api(request):
    """
    ログインユーザーのコレクションを返す API。
    形式:
    {
        "3,5": {"present": 1, "absent": 0},
        "4,5": {"present": 0, "absent": 2},
        ...
    }
    """
    user = request.user
    collections = UserGridCollection.objects.filter(user=user)

    data = {}

    for c in collections:
        key = f"{c.gx},{c.gy}"
        data[key] = {
            "present": c.present_count,
            "absent": c.absent_count,
        }

    return JsonResponse(data)
