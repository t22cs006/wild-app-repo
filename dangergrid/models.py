from django.db import models

class DangerGrid(models.Model):
    gx = models.IntegerField()
    gy = models.IntegerField()
    reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('gx', 'gy')

    def __str__(self):
        return f"Danger Grid ({self.gx}, {self.gy})"
