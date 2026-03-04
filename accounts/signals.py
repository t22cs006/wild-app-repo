from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UserProfile
from .utils import check_trophies, update_login_days

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(user_logged_in)
def on_user_logged_in(sender, user, request, **kwargs):
    """
    ログイン時に呼ばれる処理
    連続ログイン日数の更新のみ行う
    （トロフィー更新は loading 画面で非同期に行う）
    """
    update_login_days(user)


