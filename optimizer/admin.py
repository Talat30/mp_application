# from django.contrib import admin
# from .models import UserProfile, NetflixShow, UserPreference

# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'daily_study_hours', 'daily_sleep_hours', 'daily_leisure_hours')
#     search_fields = ('user__username',)

# @admin.register(NetflixShow)
# class NetflixShowAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'episode_length', 'total_episodes', 'rating', 'total_watch_time')
#     list_filter = ('category', 'rating')
#     search_fields = ('title',)

# @admin.register(UserPreference)
# class UserPreferenceAdmin(admin.ModelAdmin):
#     list_display = ('user', 'category', 'weight')
#     list_filter = ('category',)
#     search_fields = ('user__username',)
from django.contrib import admin
from .models import UserProfile, NetflixShow, UserPreference, Recommendation

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'daily_study_hours', 'daily_sleep_hours', 'daily_leisure_hours')
    search_fields = ('user__username',)

@admin.register(NetflixShow)
class NetflixShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'episode_length', 'total_episodes', 'rating', 'total_watch_time')
    list_filter = ('category', 'rating')
    search_fields = ('title',)

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'weight')
    list_filter = ('category',)
    search_fields = ('user__username',)

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'show', 'recommended_date', 'watched')
    list_filter = ('watched', 'recommended_date')
    search_fields = ('user__username', 'show__title')