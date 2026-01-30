from django import forms
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from .models import User, ArtistProfile, VenueProfile, ManagerProfile

class CustomUserCreationForm(SignupForm):
    """Custom signup form that includes user type selection for Allauth."""
    
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if hasattr(field.widget, 'attrs'):
                field.widget.attrs.update({'class': 'form-control'})
    
    def save(self, request):
        """Save the user with the selected user type and create role profile (artist/venue/manager)."""
        user = super().save(request)
        user_type = self.cleaned_data.get('user_type')
        if user_type:
            user.user_type = user_type
            user.save(update_fields=['user_type'])
            # Create role profile so dashboard/complete-profile work immediately
            if user_type == 'artist':
                ArtistProfile.objects.get_or_create(user=user)
            elif user_type == 'venue':
                VenueProfile.objects.get_or_create(user=user)
            elif user_type == 'manager':
                ManagerProfile.objects.get_or_create(user=user)
        return user

class ArtistProfileForm(forms.ModelForm):
    class Meta:
        model = ArtistProfile
        fields = ['stage_name', 'bio', 'genre', 'phone', 'city', 'state', 'country', 'experience_years', 'hourly_rate', 'website', 'instagram', 'facebook', 'youtube', 'is_available', 'is_verified']
        widgets = {
            'stage_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control'}),
            'youtube': forms.TextInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class VenueProfileForm(forms.ModelForm):
    class Meta:
        model = VenueProfile
        fields = ['venue_name', 'venue_type', 'description', 'phone', 'address', 'city', 'state', 'country', 'capacity', 'amenities', 'website', 'business_hours', 'is_verified', 'is_active']
        widgets = {
            'venue_name': forms.TextInput(attrs={'class': 'form-control'}),
            'venue_type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'amenities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'business_hours': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ManagerProfileForm(forms.ModelForm):
    class Meta:
        model = ManagerProfile
        fields = ['company_name', 'bio', 'specialization', 'phone', 'city', 'state', 'country', 'experience_years', 'commission_rate', 'website', 'linkedin', 'is_verified', 'is_active']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'commission_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin': forms.TextInput(attrs={'class': 'form-control'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ManagerVerificationForm(forms.ModelForm):
    """Form for managers to submit verification documents."""
    
    class Meta:
        model = ManagerProfile
        fields = ['business_license', 'business_address', 'business_phone', 'references']
        widgets = {
            'business_license': forms.FileInput(attrs={'class': 'form-control'}),
            'business_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'business_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'references': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Please provide 2-3 professional references with contact information...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['business_license'].required = True
        self.fields['business_address'].required = True
        self.fields['business_phone'].required = True
        self.fields['references'].required = True
        
        # Add help text
        self.fields['business_license'].help_text = 'Upload your business license or registration document (PDF, JPG, PNG)'
        self.fields['business_address'].help_text = 'Your business address for verification purposes'
        self.fields['business_phone'].help_text = 'Business phone number for verification'
        self.fields['references'].help_text = 'Provide 2-3 professional references who can vouch for your management experience'

class ProfilePictureForm(forms.ModelForm):
    """Form for updating profile picture only (used in Edit Profile)."""
    class Meta:
        model = User
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }


class UserProfileForm(forms.ModelForm):
    """Form for updating basic user profile information."""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'address', 'bio', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        } 