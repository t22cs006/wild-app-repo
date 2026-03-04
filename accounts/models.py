from django.db import models
from django.contrib.auth.models import User
from datetime import date

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # 投稿系
    present_count = models.IntegerField(default=0)
    absent_count = models.IntegerField(default=0)
    rare_found = models.IntegerField(default=0)

    # ログイン系
    login_days = models.IntegerField(default=0)
    last_login_date = models.DateField(null=True, blank=True)

    # 連続投稿系
    consecutive_post_days = models.IntegerField(default=0, help_text="連続投稿日数")
    last_post_date = models.DateField(null=True, blank=True, help_text="最終投稿日")

    # 新規開拓・久しぶり系
    pioneer_count = models.IntegerField(default=0, help_text="未開拓エリア(投稿5件以下)への投稿回数")
    revival_count = models.IntegerField(default=0, help_text="1ヶ月以上投稿がなかったエリアへの投稿回数")

    def __str__(self):
        return f"{self.user.username} Profile"
