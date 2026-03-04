from django.contrib import admin
from .models import UserGridCollection
from .models import PuzzleImage

admin.site.register(PuzzleImage)
admin.site.register(UserGridCollection)
