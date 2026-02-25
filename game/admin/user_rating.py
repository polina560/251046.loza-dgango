
from django.contrib import admin

from game.models.user_rating import UserRating


@admin.register(UserRating)
class UserRatingModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'clan', 'stage', 'glory', 'glory_time')