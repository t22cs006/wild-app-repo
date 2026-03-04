from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Post(models.Model):
    PRESENCE_CHOICES = [
        ("present", "いた"),
        ("absent", "いなかった"),
    ]

    TIME_MODE_CHOICES = [
        ("auto", "自動（現在時刻）"),
        ("manual", "手動入力"),
    ]

    SPECIES_CHOICES = [
        ("タヌキ", "タヌキ"),
        ("キツネ", "キツネ"),
        ("シカ", "シカ"),
        ("イノシシ", "イノシシ"),
        ("サル", "サル"),
        ("クマ", "クマ"),
        ("ハクビシン", "ハクビシン"),
        ("アライグマ", "アライグマ"),
        ("不明", "わからない"),
        # ★ レア個体はユーザー選択不可なので choices に入れない
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 位置情報
    lat = models.FloatField()
    lon = models.FloatField()

    # グリッド座標
    gx = models.IntegerField()
    gy = models.IntegerField()

    # いた / いなかった
    presence = models.CharField(
        max_length=10,
        choices=PRESENCE_CHOICES,
        default="present"
    )

    # 画像（任意）
    image = models.ImageField(upload_to="posts/", null=True, blank=True)

    # 時刻
    timestamp = models.DateTimeField(default=timezone.now)
    time_mode = models.CharField(
        max_length=10,
        choices=TIME_MODE_CHOICES,
        default="auto"
    )

    # 位置情報の取得元
    source = models.CharField(max_length=20, default="manual")

    # 投稿の有効性
    is_valid = models.BooleanField(default=True)

    # 種類（ユーザー選択 or 不明）
    species = models.CharField(
        max_length=50,
        choices=SPECIES_CHOICES,
        blank=True,
        null=True,
        default="不明"
    )

    # 作成日時
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # ★ 画像必須チェックは削除
        # presence = present でも画像は任意

        # time_mode = auto → timestamp を現在時刻に
        if self.time_mode == "auto":
            self.timestamp = timezone.now()

        # time_mode = manual → timestamp 必須
        if self.time_mode == "manual" and not self.timestamp:
            raise ValidationError("手動入力の日時が指定されていません。")

    def __str__(self):
        return f"{self.user.username} - {self.presence} ({self.lat}, {self.lon})"
