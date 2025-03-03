# from django import forms
# from .models import UserProfile, UserPreference

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['daily_study_hours', 'daily_sleep_hours', 'daily_leisure_hours']
#         labels = {
#             'daily_study_hours': 'Study Hours per Day',
#             'daily_sleep_hours': 'Sleep Hours per Day',
#             'daily_leisure_hours': 'Leisure Hours per Day (Netflix)',
#         }
#         widgets = {
#             'daily_study_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0', 'max': '24'}),
#             'daily_sleep_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0', 'max': '24'}),
#             'daily_leisure_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0', 'max': '24'}),
#         }

# class UserPreferenceForm(forms.ModelForm):
#     class Meta:
#         model = UserPreference
#         fields = ['category', 'weight']
#         widgets = {
#             'weight': forms.NumberInput(attrs={'class': 'form-range', 'type': 'range', 'min': '1', 'max': '10'}),
#         }

# class OptimizationForm(forms.Form):
#     available_hours = forms.FloatField(
#         label='Total Available Hours per Day',
#         min_value=1,
#         max_value=24,
#         initial=24,
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'})
#     )
#     min_study_hours = forms.FloatField(
#         label='Minimum Study Hours per Day',
#         min_value=0,
#         max_value=24,
#         initial=4,
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'})
#     )
#     min_sleep_hours = forms.FloatField(
#         label='Minimum Sleep Hours per Day',
#         min_value=0,
#         max_value=24,
#         initial=7,
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'})
#     )
    
#     def clean(self):
#         cleaned_data = super().clean()
#         available = cleaned_data.get('available_hours')
#         min_study = cleaned_data.get('min_study_hours')
#         min_sleep = cleaned_data.get('min_sleep_hours')
        
#         if available and min_study and min_sleep:
#             if min_study + min_sleep > available:
#                 raise forms.ValidationError(
#                     "The sum of minimum study and sleep hours cannot exceed total available hours."
#                 )
        
#         return cleaned_data
from django import forms
from .models import UserProfile, UserPreference

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['daily_study_hours', 'daily_sleep_hours', 'daily_leisure_hours']
        labels = {
            'daily_study_hours': 'Study Hours per Day',
            'daily_sleep_hours': 'Sleep Hours per Day',
            'daily_leisure_hours': 'Leisure Hours per Day (Netflix)',
        }
        widgets = {
            'daily_study_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0', 'max': '24'}),
            'daily_sleep_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0', 'max': '24'}),
            'daily_leisure_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0', 'max': '24'}),
        }

class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['category', 'weight']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-range', 'type': 'range', 'min': '1', 'max': '10'}),
        }

class OptimizationForm(forms.Form):
    available_hours = forms.FloatField(
        label='Total Available Hours per Day',
        min_value=1,
        max_value=24,
        initial=24,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'})
    )
    min_study_hours = forms.FloatField(
        label='Minimum Study Hours per Day',
        min_value=0,
        max_value=24,
        initial=4,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'})
    )
    min_sleep_hours = forms.FloatField(
        label='Minimum Sleep Hours per Day',
        min_value=0,
        max_value=24,
        initial=7,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        available = cleaned_data.get('available_hours')
        min_study = cleaned_data.get('min_study_hours')
        min_sleep = cleaned_data.get('min_sleep_hours')
        
        if available and min_study and min_sleep:
            if min_study + min_sleep > available:
                raise forms.ValidationError(
                    "The sum of minimum study and sleep hours cannot exceed total available hours."
                )
        
        return cleaned_data