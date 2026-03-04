from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from accounts.models import UserProfile
from datetime import date, timedelta

@receiver(post_save, sender=Post)
def update_consecutive_post_days(sender, instance, created, **kwargs):
    """
    投稿が作成されたときに連続投稿日数を更新する
    """
    if not created:
        return

    user = instance.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    today = date.today()

    # まだ今日投稿していなければ処理開始
    if profile.last_post_date != today:
        # 昨日投稿していれば連続日数+1
        if profile.last_post_date == today - timedelta(days=1):
            profile.consecutive_post_days += 1
        else:
            # 昨日投稿していなければリセット（今日が1日目）
            profile.consecutive_post_days = 1
        
        profile.last_post_date = today
        profile.save()
