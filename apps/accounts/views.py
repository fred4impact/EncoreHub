from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import ArtistProfileForm, VenueProfileForm, ManagerProfileForm, ManagerVerificationForm, UserProfileForm, ProfilePictureForm
from .models import User, ArtistProfile, VenueProfile, ManagerProfile

def manager_discovery(request):
    """Public manager discovery page for venues."""
    # Get verified managers only
    managers = ManagerProfile.objects.filter(
        verification_status='verified',
        is_active=True
    ).select_related('user')
    
    # Search and filtering
    search_query = request.GET.get('search', '')
    specialization = request.GET.get('specialization', '')
    location = request.GET.get('location', '')
    
    if search_query:
        managers = managers.filter(
            Q(company_name__icontains=search_query) |
            Q(bio__icontains=search_query) |
            Q(specialization__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )
    
    if specialization:
        managers = managers.filter(specialization__icontains=specialization)
    
    if location:
        managers = managers.filter(
            Q(city__icontains=location) |
            Q(state__icontains=location) |
            Q(country__icontains=location)
        )
    
    # Pagination
    paginator = Paginator(managers, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique specializations and locations for filters
    specializations = ManagerProfile.objects.filter(
        verification_status='verified'
    ).values_list('specialization', flat=True).distinct()
    
    locations = ManagerProfile.objects.filter(
        verification_status='verified'
    ).values_list('city', 'state', 'country').distinct()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'specialization': specialization,
        'location': location,
        'specializations': specializations,
        'locations': locations,
        'total_managers': managers.count(),
    }
    
    return render(request, 'accounts/manager_discovery.html', context)

def manager_detail(request, manager_id):
    """Public manager detail page showing their artist roster."""
    manager = get_object_or_404(ManagerProfile, 
                               id=manager_id, 
                               verification_status='verified',
                               is_active=True)
    
    # Get artists managed by this manager (placeholder for now)
    # This will be implemented when we add the artist-manager relationship
    managed_artists = []
    
    context = {
        'manager': manager,
        'managed_artists': managed_artists,
    }
    
    return render(request, 'accounts/manager_detail.html', context)

@login_required
def complete_artist_profile(request):
    """Complete artist profile after registration."""
    if request.user.user_type != 'artist':
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    try:
        profile = request.user.artist_profile
    except ArtistProfile.DoesNotExist:
        profile = ArtistProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ArtistProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artist profile completed successfully!')
            return redirect('accounts:dashboard')
    else:
        form = ArtistProfileForm(instance=profile)
    
    return render(request, 'accounts/complete_artist_profile.html', {'form': form})

@login_required
def complete_venue_profile(request):
    """Complete venue profile after registration."""
    if request.user.user_type != 'venue':
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    try:
        profile = request.user.venue_profile
    except VenueProfile.DoesNotExist:
        profile = VenueProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = VenueProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Venue profile completed successfully!')
            return redirect('accounts:dashboard')
    else:
        form = VenueProfileForm(instance=profile)
    
    return render(request, 'accounts/complete_venue_profile.html', {'form': form})

@login_required
def complete_manager_profile(request):
    """Complete manager profile after registration."""
    if request.user.user_type != 'manager':
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    try:
        profile = request.user.manager_profile
    except ManagerProfile.DoesNotExist:
        profile = ManagerProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ManagerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Manager profile completed successfully! Please submit verification documents.')
            return redirect('accounts:manager_verification')
    else:
        form = ManagerProfileForm(instance=profile)
    
    return render(request, 'accounts/complete_manager_profile.html', {'form': form})

@login_required
def manager_verification(request):
    """Submit manager verification documents."""
    if request.user.user_type != 'manager':
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    try:
        profile = request.user.manager_profile
    except ManagerProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('accounts:complete_manager_profile')
    
    if profile.verification_status == 'verified':
        messages.info(request, 'Your account is already verified!')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = ManagerVerificationForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile.verification_status = 'pending'
            form.save()
            messages.success(request, 'Verification documents submitted successfully! Our team will review them within 2-3 business days.')
            return redirect('accounts:dashboard')
    else:
        form = ManagerVerificationForm(instance=profile)
    
    return render(request, 'accounts/manager_verification.html', {'form': form, 'profile': profile})

@login_required
def edit_profile(request):
    """Edit role-specific profile (artist, venue, or manager)."""
    user_type = request.user.user_type
    if user_type == 'artist':
        try:
            profile_obj = request.user.artist_profile
        except ArtistProfile.DoesNotExist:
            profile_obj = ArtistProfile.objects.create(user=request.user)
        form_class = ArtistProfileForm
    elif user_type == 'venue':
        try:
            profile_obj = request.user.venue_profile
        except VenueProfile.DoesNotExist:
            profile_obj = VenueProfile.objects.create(user=request.user)
        form_class = VenueProfileForm
    elif user_type == 'manager':
        try:
            profile_obj = request.user.manager_profile
        except ManagerProfile.DoesNotExist:
            profile_obj = ManagerProfile.objects.create(user=request.user)
        form_class = ManagerProfileForm
    else:
        messages.error(request, 'Invalid account type.')
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = form_class(request.POST, instance=profile_obj)
        user_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:dashboard')
    else:
        form = form_class(instance=profile_obj)
        user_form = ProfilePictureForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form, 'user_form': user_form, 'user': request.user})

@login_required
def profile(request):
    """View and edit user profile."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
    }
    
    # Add role-specific profile data
    if request.user.user_type == 'artist':
        try:
            context['artist_profile'] = request.user.artist_profile
        except ArtistProfile.DoesNotExist:
            pass
    elif request.user.user_type == 'venue':
        try:
            context['venue_profile'] = request.user.venue_profile
        except VenueProfile.DoesNotExist:
            pass
    elif request.user.user_type == 'manager':
        try:
            context['manager_profile'] = request.user.manager_profile
        except ManagerProfile.DoesNotExist:
            pass
    
    return render(request, 'accounts/profile.html', context)

@login_required
def dashboard(request):
    """Role-based dashboard."""
    context = {
        'user': request.user,
    }
    
    # Add role-specific data
    if request.user.user_type == 'artist':
        try:
            context['artist_profile'] = request.user.artist_profile
        except ArtistProfile.DoesNotExist:
            pass
    elif request.user.user_type == 'venue':
        try:
            context['venue_profile'] = request.user.venue_profile
        except VenueProfile.DoesNotExist:
            pass
    elif request.user.user_type == 'manager':
        try:
            context['manager_profile'] = request.user.manager_profile
        except ManagerProfile.DoesNotExist:
            pass
    
    return render(request, 'accounts/dashboard.html', context)
