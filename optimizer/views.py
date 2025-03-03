# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login, authenticate
# from django.contrib import messages
# from django.db.models import Sum, Avg
# import numpy as np
# from scipy.optimize import linprog

# from .models import UserProfile, NetflixShow, UserPreference
# from .forms import UserProfileForm, UserPreferenceForm, OptimizationForm

# def home(request):
#     """Home page view"""
#     shows = NetflixShow.objects.all().order_by('-rating')[:5]
    
#     # If no shows exist in the database, create some default shows
#     if not shows.exists():
#         # Create some popular Netflix shows
#         default_shows = [
#             {
#                 'title': 'Stranger Things',
#                 'category': 'scifi',
#                 'episode_length': 50,
#                 'total_episodes': 34,
#                 'rating': 8.7
#             },
#             {
#                 'title': 'The Crown',
#                 'category': 'drama',
#                 'episode_length': 55,
#                 'total_episodes': 50,
#                 'rating': 8.6
#             },
#             {
#                 'title': 'Money Heist',
#                 'category': 'thriller',
#                 'episode_length': 45,
#                 'total_episodes': 41,
#                 'rating': 8.2
#             },
#             {
#                 'title': 'Squid Game',
#                 'category': 'thriller',
#                 'episode_length': 55,
#                 'total_episodes': 9,
#                 'rating': 8.0
#             },
#             {
#                 'title': 'Wednesday',
#                 'category': 'comedy',
#                 'episode_length': 45,
#                 'total_episodes': 8,
#                 'rating': 8.1
#             }
#         ]
        
#         # Create the shows in the database
#         for show_data in default_shows:
#             NetflixShow.objects.create(**show_data)
        
#         # Fetch the newly created shows
#         shows = NetflixShow.objects.all().order_by('-rating')[:5]
    
#     return render(request, 'optimizer/home.html', {'shows': shows})

# def signup(request):
#     """User registration view"""
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Create user profile
#             UserProfile.objects.create(user=user)
#             # Log the user in
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             messages.success(request, f"Account created for {username}!")
#             return redirect('profile_setup')
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/signup.html', {'form': form})

# @login_required
# def profile_setup(request):
#     """Initial profile setup after registration"""
#     profile = request.user.profile
    
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Profile updated successfully!")
#             return redirect('preference_setup')
#     else:
#         form = UserProfileForm(instance=profile)
    
#     return render(request, 'optimizer/profile_setup.html', {'form': form})

# @login_required
# def preference_setup(request):
#     """Setup user preferences for show categories"""
#     categories = dict(NetflixShow.CATEGORY_CHOICES)
    
#     if request.method == 'POST':
#         for category, _ in NetflixShow.CATEGORY_CHOICES:
#             weight = request.POST.get(category, 5)
#             UserPreference.objects.update_or_create(
#                 user=request.user,
#                 category=category,
#                 defaults={'weight': weight}
#             )
#         messages.success(request, "Preferences saved successfully!")
#         return redirect('dashboard')
    
#     # Get existing preferences or create defaults
#     preferences = {}
#     for category, _ in NetflixShow.CATEGORY_CHOICES:
#         pref, created = UserPreference.objects.get_or_create(
#             user=request.user,
#             category=category,
#             defaults={'weight': 5}
#         )
#         preferences[category] = pref.weight
    
#     return render(request, 'optimizer/preference_setup.html', {
#         'categories': categories,
#         'preferences': preferences
#     })
# @login_required
# def dashboard(request):
#     profile = request.user.profile  # Assuming profile is linked to user
    
#     # Calculate percentages
#     study_percent = (profile.daily_study_hours / 24) * 100
#     sleep_percent = (profile.daily_sleep_hours / 24) * 100
#     netflix_percent = (profile.daily_leisure_hours / 24) * 100

#     context = {
#         'profile': profile,
#         'study_percent': study_percent,
#         'sleep_percent': sleep_percent,
#         'netflix_percent': netflix_percent,
#     }
#     return render(request, 'dashboard.html', context)

# @login_required
# def optimize_time(request):
#     """View to optimize time using simplex method"""
#     if request.method == 'POST':
#         form = OptimizationForm(request.POST)
#         if form.is_valid():
#             # Get user constraints
#             available_hours = form.cleaned_data['available_hours']
#             min_study = form.cleaned_data['min_study_hours']
#             min_sleep = form.cleaned_data['min_sleep_hours']
            
#             # Get user profile
#             profile = request.user.profile
            
#             # Setup the simplex problem
#             # Objective: Maximize enjoyment (Netflix time weighted by preferences)
#             # Variables: [netflix_time, study_time, sleep_time]
#             # We want to maximize netflix_time, so we minimize -netflix_time
#             c = [-1, 0, 0]  # Coefficients of the objective function
            
#             # Constraints:
#             # 1. Total time <= available_hours
#             # 2. study_time >= min_study
#             # 3. sleep_time >= min_sleep
#             A_ub = [
#                 [1, 1, 1],  # Total time constraint
#                 [0, -1, 0],  # Study time constraint
#                 [0, 0, -1],  # Sleep time constraint
#             ]
            
#             b_ub = [
#                 available_hours,  # Total available hours
#                 -min_study,       # Minimum study hours
#                 -min_sleep,       # Minimum sleep hours
#             ]
            
#             # Bounds for variables (all non-negative)
#             bounds = [(0, None), (0, None), (0, None)]
            
#             # Solve the linear programming problem
#             result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='simplex')
            
#             if result.success:
#                 netflix_time, study_time, sleep_time = result.x
                
#                 # Update user profile
#                 profile.daily_study_hours = study_time
#                 profile.daily_sleep_hours = sleep_time
#                 profile.daily_leisure_hours = netflix_time
#                 profile.save()
                
#                 messages.success(request, "Time optimized successfully!")
#                 return redirect('dashboard')
#             else:
#                 messages.error(request, "Optimization failed. Please adjust your constraints.")
#     else:
#         # Pre-fill form with user's current values
#         profile = request.user.profile
#         initial_data = {
#             'available_hours': 24,
#             'min_study_hours': profile.daily_study_hours,
#             'min_sleep_hours': profile.daily_sleep_hours,
#         }
#         form = OptimizationForm(initial=initial_data)
    
#     return render(request, 'optimizer/optimize.html', {'form': form})

# @login_required
# def profile(request):
#     """User profile view"""
#     profile = request.user.profile
    
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Profile updated successfully!")
#             return redirect('profile')
#     else:
#         form = UserProfileForm(instance=profile)
    
#     return render(request, 'optimizer/profile.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Sum, Avg
import numpy as np
from scipy.optimize import linprog

from .models import UserProfile, NetflixShow, UserPreference, Recommendation
from .forms import UserProfileForm, UserPreferenceForm, OptimizationForm

def home(request):
    """Home page view"""
    shows = NetflixShow.objects.all().order_by('-rating')[:5]
    return render(request, 'optimizer/home.html', {'shows': shows})

def signup(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            # Log the user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"Account created for {username}!")
            return redirect('profile_setup')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile_setup(request):
    """Initial profile setup after registration"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('preference_setup')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'optimizer/profile_setup.html', {'form': form})

@login_required
def preference_setup(request):
    """Setup user preferences for show categories"""
    categories = dict(NetflixShow.CATEGORY_CHOICES)
    
    if request.method == 'POST':
        for category, _ in NetflixShow.CATEGORY_CHOICES:
            weight = request.POST.get(category, 5)
            UserPreference.objects.update_or_create(
                user=request.user,
                category=category,
                defaults={'weight': weight}
            )
        messages.success(request, "Preferences saved successfully!")
        return redirect('dashboard')
    
    # Get existing preferences or create defaults
    preferences = {}
    for category, _ in NetflixShow.CATEGORY_CHOICES:
        pref, created = UserPreference.objects.get_or_create(
            user=request.user,
            category=category,
            defaults={'weight': 5}
        )
        preferences[category] = pref.weight
    
    return render(request, 'optimizer/preference_setup.html', {
        'categories': categories,
        'preferences': preferences
    })

@login_required
def dashboard(request):
    """User dashboard with recommendations"""
    profile = request.user.profile
    recommendations = Recommendation.objects.filter(user=request.user, watched=False)
    
    context = {
        'profile': profile,
        'recommendations': recommendations,
    }
    return render(request, 'optimizer/dashboard.html', context)

@login_required
def optimize_time(request):
    """View to optimize time using simplex method"""
    if request.method == 'POST':
        form = OptimizationForm(request.POST)
        if form.is_valid():
            # Get user constraints
            available_hours = form.cleaned_data['available_hours']
            min_study = form.cleaned_data['min_study_hours']
            min_sleep = form.cleaned_data['min_sleep_hours']
            
            # Get user profile
            profile = request.user.profile
            
            # Setup the simplex problem
            # Objective: Maximize enjoyment (Netflix time weighted by preferences)
            # Variables: [netflix_time, study_time, sleep_time]
            # We want to maximize netflix_time, so we minimize -netflix_time
            c = [-1, 0, 0]  # Coefficients of the objective function
            
            # Constraints:
            # 1. Total time <= available_hours
            # 2. study_time >= min_study
            # 3. sleep_time >= min_sleep
            A_ub = [
                [1, 1, 1],  # Total time constraint
                [0, -1, 0],  # Study time constraint
                [0, 0, -1],  # Sleep time constraint
            ]
            
            b_ub = [
                available_hours,  # Total available hours
                -min_study,       # Minimum study hours
                -min_sleep,       # Minimum sleep hours
            ]
            
            # Bounds for variables (all non-negative)
            bounds = [(0, None), (0, None), (0, None)]
            
            # Solve the linear programming problem
            result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='simplex')
            
            if result.success:
                netflix_time, study_time, sleep_time = result.x
                
                # Update user profile
                profile.daily_study_hours = study_time
                profile.daily_sleep_hours = sleep_time
                profile.daily_leisure_hours = netflix_time
                profile.save()
                
                # Generate recommendations based on available Netflix time
                generate_recommendations(request.user, netflix_time)
                
                messages.success(request, "Time optimized successfully!")
                return redirect('dashboard')
            else:
                messages.error(request, "Optimization failed. Please adjust your constraints.")
    else:
        # Pre-fill form with user's current values
        profile = request.user.profile
        initial_data = {
            'available_hours': 24,
            'min_study_hours': profile.daily_study_hours,
            'min_sleep_hours': profile.daily_sleep_hours,
        }
        form = OptimizationForm(initial=initial_data)
    
    return render(request, 'optimizer/optimize.html', {'form': form})

def generate_recommendations(user, available_hours):
    """Generate show recommendations based on available time and preferences"""
    # Clear existing unwatched recommendations
    Recommendation.objects.filter(user=user, watched=False).delete()
    
    # Get user preferences
    preferences = UserPreference.objects.filter(user=user)
    pref_dict = {p.category: p.weight for p in preferences}
    
    # Get shows sorted by weighted rating (rating * user preference for category)
    shows = NetflixShow.objects.all()
    weighted_shows = []
    
    for show in shows:
        pref_weight = pref_dict.get(show.category, 5)  # Default to 5 if no preference
        weighted_rating = show.rating * (pref_weight / 5)  # Normalize preference
        weighted_shows.append((show, weighted_rating, show.total_watch_time))
    
    # Sort by weighted rating
    weighted_shows.sort(key=lambda x: x[1], reverse=True)
    
    # Select shows that fit within available time
    remaining_time = available_hours
    for show, _, watch_time in weighted_shows:
        if watch_time <= remaining_time:
            # Create recommendation
            Recommendation.objects.create(user=user, show=show)
            remaining_time -= watch_time
            
            # Stop if we've recommended enough shows
            if remaining_time < 0.5:  # Less than 30 minutes left
                break

@login_required
def mark_watched(request, recommendation_id):
    """Mark a recommendation as watched"""
    recommendation = get_object_or_404(Recommendation, id=recommendation_id, user=request.user)
    recommendation.watched = True
    recommendation.save()
    messages.success(request, f"Marked '{recommendation.show.title}' as watched!")
    return redirect('dashboard')

@login_required
def profile(request):
    """User profile view"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'optimizer/profile.html', {'form': form})