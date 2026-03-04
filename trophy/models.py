from django.db import models
from django.contrib.auth.models import User


# class UserProfile(models.Model):
#     """
#     ユーザープロファイルモデル
#     ユーザーの統計情報を管理
#     """
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name='profile',
#         help_text="ユーザー"
#     )
#     present_count = models.PositiveIntegerField(
#         default=0,
#         help_text="いた投稿の総数"
#     )
#     absent_count = models.PositiveIntegerField(
#         default=0,
#         help_text="いなかった投稿の総数"
#     )
#     rare_found = models.PositiveIntegerField(
#         default=0,
#         help_text="レア個体発見数"
#     )

#     class Meta:
#         verbose_name = "ユーザープロファイル"
#         verbose_name_plural = "ユーザープロファイル"

#     def __str__(self):
#         return f"{self.user.username} のプロファイル"


class Trophy(models.Model):
    """
    トロフィーモデル
    ユーザーが達成可能な目標を定義
    """
    RARITY_CHOICES = [
        ('bronze', 'ブロンズ'),
        ('silver', 'シルバー'),
        ('gold', 'ゴールド'),
        ('legend', 'レジェンド'),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="トロフィーの名前"
    )
    description = models.TextField(
        help_text="トロフィーの説明"
    )
    rarity = models.CharField(
        max_length=20,
        choices=RARITY_CHOICES,
        default='bronze',
        help_text="トロフィーのレア度"
    )
    condition_type = models.CharField(
        max_length=50,
        help_text="達成条件の種類（例: 'posts_count', 'species_count'）"
    )
    condition_value = models.PositiveIntegerField(
        default=1,
        help_text="達成条件の値"
    )
    icon = models.CharField(
        max_length=10,
        default="🏆",
        help_text="トロフィーのアイコン（絵文字）"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="アクティブなトロフィーかどうか"
    )

    class Meta:
        verbose_name = "トロフィー"
        verbose_name_plural = "トロフィー"
        ordering = ['rarity', 'name']

    def __str__(self):
        return f"{self.get_rarity_display()} {self.name}"

    @property
    def rarity_color(self):
        """レア度に応じた色を返す"""
        colors = {
            'bronze': '#CD7F32',
            'silver': '#C0C0C0',
            'gold': '#FFD700',
            'legend': '#FF6B6B'
        }
        return colors.get(self.rarity, '#666')


class UserTrophy(models.Model):
    """
    ユーザートロフィーモデル
    ユーザーが取得したトロフィーを管理
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='trophies',
        help_text="トロフィーを取得したユーザー"
    )
    trophy = models.ForeignKey(
        Trophy,
        on_delete=models.CASCADE,
        related_name='user_trophies',
        help_text="取得したトロフィー"
    )
    obtained_at = models.DateTimeField(
        auto_now_add=True,
        help_text="トロフィー取得日時"
    )

    class Meta:
        verbose_name = "ユーザートロフィー"
        verbose_name_plural = "ユーザートロフィー"
        unique_together = ('user', 'trophy')
        ordering = ['-obtained_at']

    def __str__(self):
        return f"{self.user.username} - {self.trophy.name}"

    @property
    def days_since_obtained(self):
        """取得してから何日経ったか"""
        from django.utils import timezone
        return (timezone.now().date() - self.obtained_at.date()).days
