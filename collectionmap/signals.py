# collectionmap/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from posts.models import Post
from .models import UserGridCollection
from maps.utils_grid import latlon_to_grid


@receiver(post_save, sender=Post)
def update_user_collection(sender, instance, created, **kwargs):
    """
    Post が保存されたときに、ユーザーのコレクションを更新する。
    """
    if not created:
        return  # 新規作成時のみ処理

    user = instance.user
    lat = instance.lat
    lon = instance.lon
    presence = instance.presence  # "present" or "absent"

    # グリッド番号を計算
    gx, gy = latlon_to_grid(lat, lon)

    # コレクションを取得 or 作成
    collection, _ = UserGridCollection.objects.get_or_create(
        user=user,
        gx=gx,
        gy=gy
    )

    # カウントを更新
    if presence == "present":
        collection.present_count += 1
    else:
        collection.absent_count += 1

    collection.save()
