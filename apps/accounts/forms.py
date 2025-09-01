from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from .models import ArtistProfile, VenueProfile, ManagerProfile

User = get_user_model()


class CustomSignupForm(SignupForm):
    """Custom signup form that includes user type selection."""
    
    USER_TYPE_CHOICES = [
        ('artist', 'Artist'),
        ('venue', 'Venue'),
        ('manager', 'Manager'),
    ]
    
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        required=True,
        widget=forms.RadioSelect,
        help_text='Select your account type'
    )
    
    def save(self, request):
        """Save the user with the selected user type."""
        user = super().save(request)
        user.user_type = self.cleaned_data['user_type']
        user.save()
        return user


class ArtistProfileForm(forms.ModelForm):
    class Meta:
        model = ArtistProfile
        fields = [
            'stage_name', 'bio', 'genre', 'experience_years',
            'hourly_rate', 'city', 'state', 'country', 'phone', 'website',
            'instagram', 'facebook', 'youtube', 'is_available', 'is_verified'
        ]
        widgets = {
            'stage_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your stage name'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself and your music...'
            }),
            'genre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Jazz, Rock, Classical'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100
            }),
            'hourly_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourwebsite.com'
            }),
            'instagram': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@username'
            }),
            'facebook': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'username or page name'
            }),
            'youtube': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Channel name or URL'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_verified': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

class VenueProfileForm(forms.ModelForm):
    class Meta:
        model = VenueProfile
        fields = [
            'venue_name', 'venue_type', 'description', 'capacity',
            'address', 'city', 'state', 'country', 'phone', 'website',
            'business_hours', 'amenities', 'is_active', 'is_verified'
        ]
        widgets = {
            'venue_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter venue name'
            }),
            'venue_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your venue...'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourvenue.com'
            }),
            'business_hours': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Monday: 9 AM - 5 PM\nTuesday: 9 AM - 5 PM\n...'
            }),
            'amenities': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Sound system, lighting, parking, etc.'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_verified': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

class ManagerProfileForm(forms.ModelForm):
    class Meta:
        model = ManagerProfile
        fields = [
            'company_name', 'bio', 'specialization', 'experience_years',
            'commission_rate', 'city', 'state', 'country', 'phone', 'website',
            'is_active', 'is_verified'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about your management experience...'
            }),
            'specialization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Rock bands, Jazz artists, Classical musicians'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100
            }),
            'commission_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'step': 0.1
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourcompany.com'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_verified': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        } 