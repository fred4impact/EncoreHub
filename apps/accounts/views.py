from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User, ArtistProfile, VenueProfile, ManagerProfile
from .forms import ArtistProfileForm, VenueProfileForm, ManagerProfileForm

@login_required
def dashboard(request):
    """User dashboard view."""
    user = request.user
    context = {
        'user': user,
    }
    
    # Add profile data based on user type
    if user.user_type == 'artist':
        try:
            context['profile'] = user.artist_profile
        except ArtistProfile.DoesNotExist:
            context['profile'] = None
    elif user.user_type == 'venue':
        try:
            context['profile'] = user.venue_profile
        except VenueProfile.DoesNotExist:
            context['profile'] = None
    elif user.user_type == 'manager':
        try:
            context['profile'] = user.manager_profile
        except ManagerProfile.DoesNotExist:
            context['profile'] = None
    
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile(request):
    """User profile view."""
    user = request.user
    context = {
        'user': user,
    }
    
    # Add profile data based on user type
    if user.user_type == 'artist':
        try:
            context['profile'] = user.artist_profile
        except ArtistProfile.DoesNotExist:
            context['profile'] = None
    elif user.user_type == 'venue':
        try:
            context['profile'] = user.venue_profile
        except VenueProfile.DoesNotExist:
            context['profile'] = None
    elif user.user_type == 'manager':
        try:
            context['profile'] = user.manager_profile
        except ManagerProfile.DoesNotExist:
            context['profile'] = None
    
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    """Edit user profile view."""
    user = request.user
    
    if request.method == 'POST':
        if user.user_type == 'artist':
            try:
                profile = user.artist_profile
                form = ArtistProfileForm(request.POST, instance=profile)
            except ArtistProfile.DoesNotExist:
                profile = None
                form = ArtistProfileForm(request.POST)
        elif user.user_type == 'venue':
            try:
                profile = user.venue_profile
                form = VenueProfileForm(request.POST, instance=profile)
            except VenueProfile.DoesNotExist:
                profile = None
                form = VenueProfileForm(request.POST)
        elif user.user_type == 'manager':
            try:
                profile = user.manager_profile
                form = ManagerProfileForm(request.POST, instance=profile)
            except ManagerProfile.DoesNotExist:
                profile = None
                form = ManagerProfileForm(request.POST)
        else:
            messages.error(request, 'Invalid user type.')
            return redirect('accounts:profile')
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # GET request - show form
        if user.user_type == 'artist':
            try:
                profile = user.artist_profile
                form = ArtistProfileForm(instance=profile)
            except ArtistProfile.DoesNotExist:
                form = ArtistProfileForm()
        elif user.user_type == 'venue':
            try:
                profile = user.venue_profile
                form = VenueProfileForm(instance=profile)
            except VenueProfile.DoesNotExist:
                form = VenueProfileForm()
        elif user.user_type == 'manager':
            try:
                profile = user.manager_profile
                form = ManagerProfileForm(instance=profile)
            except ManagerProfile.DoesNotExist:
                form = ManagerProfileForm()
        else:
            messages.error(request, 'Invalid user type.')
            return redirect('accounts:profile')
    
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'accounts/edit_profile.html', context)
