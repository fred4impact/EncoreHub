"""Custom Allauth adapter so user_type and role profile are set correctly at signup."""
from allauth.account.adapter import DefaultAccountAdapter
from .models import ArtistProfile, VenueProfile, ManagerProfile


class EncoreHubAccountAdapter(DefaultAccountAdapter):
    """Set user_type from signup form and create role profile so manager/artist/venue signup works."""

    def save_user(self, request, user, form, commit=True):
        """Save user with user_type from form, then create role profile."""
        # Set user_type from our custom signup form before first save
        if 'user_type' in form.cleaned_data:
            user.user_type = form.cleaned_data['user_type']
        user = super().save_user(request, user, form, commit=commit)
        if not commit:
            return user
        # Explicitly create role profile so signup always completes (avoids signal timing issues)
        if user.user_type == 'artist':
            ArtistProfile.objects.get_or_create(user=user)
        elif user.user_type == 'venue':
            VenueProfile.objects.get_or_create(user=user)
        elif user.user_type == 'manager':
            ManagerProfile.objects.get_or_create(user=user)
        return user
