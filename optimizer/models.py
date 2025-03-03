# from django.db import models
# from django.contrib.auth.models import User

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     daily_study_hours = models.FloatField(default=4.0)
#     daily_sleep_hours = models.FloatField(default=8.0)
#     daily_leisure_hours = models.FloatField(default=2.0)
    
#     def __str__(self):
#         return f"{self.user.username}'s Profile"

# class NetflixShow(models.Model):
#     CATEGORY_CHOICES = [
#         ('action', 'Action'),
#         ('comedy', 'Comedy'),
#         ('drama', 'Drama'),
#         ('documentary', 'Documentary'),
#         ('scifi', 'Sci-Fi'),
#         ('thriller', 'Thriller'),
#         ('romance', 'Romance'),
#         ('horror', 'Horror'),
#     ]
    
#     title = models.CharField(max_length=200)
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
#     episode_length = models.IntegerField(help_text="Average episode length in minutes")
#     total_episodes = models.IntegerField()
#     rating = models.FloatField(help_text="Rating from 1 to 10")
    
#     def __str__(self):
#         return self.title
    
#     @property
#     def total_watch_time(self):
#         """Return total watch time in hours"""
#         return (self.episode_length * self.total_episodes) / 60

# class UserPreference(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
#     category = models.CharField(max_length=20, choices=NetflixShow.CATEGORY_CHOICES)
#     weight = models.IntegerField(help_text="Preference weight from 1 to 10")
    
#     class Meta:
#         unique_together = ('user', 'category')
    
#     def __str__(self):
#         return f"{self.user.username}'s preference for {self.category}"
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    daily_study_hours = models.FloatField(default=4.0)
    daily_sleep_hours = models.FloatField(default=8.0)
    daily_leisure_hours = models.FloatField(default=2.0)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class NetflixShow(models.Model):
    CATEGORY_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('documentary', 'Documentary'),
        ('scifi', 'Sci-Fi'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('horror', 'Horror'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    episode_length = models.IntegerField(help_text="Average episode length in minutes")
    total_episodes = models.IntegerField()
    rating = models.FloatField(help_text="Rating from 1 to 10")
    
    def __str__(self):
        return self.title
    
    @property
    def total_watch_time(self):
        """Return total watch time in hours"""
        return (self.episode_length * self.total_episodes) / 60

class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    category = models.CharField(max_length=20, choices=NetflixShow.CATEGORY_CHOICES)
    weight = models.IntegerField(help_text="Preference weight from 1 to 10")
    
    class Meta:
        unique_together = ('user', 'category')
    
    def __str__(self):
        return f"{self.user.username}'s preference for {self.category}"

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    show = models.ForeignKey(NetflixShow, on_delete=models.CASCADE)
    recommended_date = models.DateTimeField(auto_now_add=True)
    watched = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.show.title}"