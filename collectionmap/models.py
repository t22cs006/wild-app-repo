# collectionmap/models.py

from django.db import models
from django.contrib.auth.models import User

class PuzzleImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='puzzles/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserGridCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gx = models.IntegerField()
    gy = models.IntegerField()

    # present（いた）投稿の数
    present_count = models.IntegerField(default=0)

    # absent（いなかった）投稿の数
    absent_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "gx", "gy")

    def __str__(self):
        return f"{self.user.username} ({self.gx}, {self.gy})"
