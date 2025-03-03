from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views  # Ensure your views are correctly imported

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile-setup/', views.profile_setup, name='profile_setup'),
    path('preference-setup/', views.preference_setup, name='preference_setup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('optimize/', views.optimize_time, name='optimize'),
    path('profile/', views.profile, name='profile'),
    
    # ✅ Corrected logout path with import
    path('accounts/logout/', LogoutView.as_view(), name='logout'),

    path('mark-watched/<int:recommendation_id>/', views.mark_watched, name='mark_watched'),
]
