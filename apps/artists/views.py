import re
from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import ArtistPortfolio, PortfolioMedia, Performance, Availability, ArtistReview
from .forms import ArtistPortfolioForm, PortfolioMediaForm, PerformanceForm, AvailabilityForm


def _parse_duration(value):
    """Convert duration string to timedelta. Accepts: '90', '2 hours', '1:30', '1:30:00'."""
    if not value or not str(value).strip():
        return timedelta(minutes=0)
    s = str(value).strip().lower()
    # Integer only -> minutes
    if s.isdigit():
        return timedelta(minutes=int(s))
    # "N hour(s)" or "N hr(s)"
    m = re.match(r'^(\d+)\s*(?:hours?|hrs?)\s*$', s)
    if m:
        return timedelta(hours=int(m.group(1)))
    # "N minute(s)" or "N min(s)"
    m = re.match(r'^(\d+)\s*(?:minutes?|mins?)\s*$', s)
    if m:
        return timedelta(minutes=int(m.group(1)))
    # H:MM or H:MM:SS
    parts = s.split(':')
    if len(parts) == 2:
        try:
            h, m = int(parts[0]), int(parts[1])
            return timedelta(hours=h, minutes=m)
        except ValueError:
            pass
    if len(parts) == 3:
        try:
            h, m, sec = int(parts[0]), int(parts[1]), int(parts[2])
            return timedelta(hours=h, minutes=m, seconds=sec)
        except ValueError:
            pass
    return timedelta(minutes=0)


def artist_list(request):
    """List all artists with filtering and search."""
    artists = ArtistPortfolio.objects.filter(is_available=True)
    supports_json_contains = connection.vendor != 'sqlite'

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        search_q = (
            Q(artist__first_name__icontains=search_query) |
            Q(artist__last_name__icontains=search_query) |
            Q(headline__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
        if supports_json_contains:
            search_q |= Q(genres__contains=[search_query])
        artists = artists.filter(search_q)

    # Filter by genre (JSONField contains not supported on SQLite)
    genre = request.GET.get('genre')
    if genre:
        if supports_json_contains:
            artists = artists.filter(genres__contains=[genre])
        else:
            pks = list(artists.values_list('pk', flat=True))
            filtered_pks = [
                p.pk for p in ArtistPortfolio.objects.filter(pk__in=pks)
                if p.genres and genre in p.genres
            ]
            artists = artists.filter(pk__in=filtered_pks)
    
    # Filter by location
    city = request.GET.get('city')
    if city:
        artists = artists.filter(artist__artist_profile__city__icontains=city)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        artists = artists.filter(base_rate__gte=min_price)
    if max_price:
        artists = artists.filter(base_rate__lte=max_price)
    
    # Pagination
    paginator = Paginator(artists, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique genres for filter
    all_genres = set()
    for artist in ArtistPortfolio.objects.all():
        all_genres.update(artist.genres)
    
    context = {
        'page_obj': page_obj,
        'genres': sorted(all_genres),
        'search_query': search_query,
    }
    return render(request, 'artists/artist_list.html', context)


def artist_detail(request, pk):
    """Show artist portfolio details (public page from discovery)."""
    portfolio = get_object_or_404(
        ArtistPortfolio.objects.select_related('artist', 'artist__artist_profile'),
        pk=pk
    )
    
    # Get featured media
    featured_media = portfolio.media.filter(is_featured=True).order_by('display_order')
    
    # Get recent performances
    recent_performances = portfolio.performances.all()[:5]
    
    # Get reviews
    reviews = portfolio.artist.reviews.filter(is_public=True).order_by('-created_at')[:5]
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    # Availability for display: show all set by artist (no date filter so timezone doesn't hide entries)
    availability = portfolio.artist.availability.all().order_by('date')[:60]
    
    context = {
        'portfolio': portfolio,
        'featured_media': featured_media,
        'recent_performances': recent_performances,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'availability': availability,
    }
    return render(request, 'artists/artist_detail.html', context)


@login_required
def my_portfolio(request):
    """Show current user's portfolio."""
    if request.user.user_type != 'artist':
        messages.error(request, 'Only artists can have portfolios.')
        return redirect('home')
    
    portfolio, created = ArtistPortfolio.objects.get_or_create(artist=request.user)
    
    if request.method == 'POST':
        form = ArtistPortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Portfolio updated successfully!')
            return redirect('artists:my_portfolio')
    else:
        form = ArtistPortfolioForm(instance=portfolio)
    
    # Get portfolio media
    media = portfolio.media.all().order_by('display_order')
    
    # Get performances
    performances = portfolio.performances.all().order_by('-event_date')
    
    # Get availability
    availability = portfolio.artist.availability.all().order_by('date')
    
    context = {
        'portfolio': portfolio,
        'form': form,
        'media': media,
        'performances': performances,
        'availability': availability,
    }
    return render(request, 'artists/my_portfolio.html', context)


@login_required
def add_media(request):
    """Add media to portfolio."""
    if request.user.user_type != 'artist':
        messages.error(request, 'Only artists can add media.')
        return redirect('artists:my_portfolio')
    
    portfolio = get_object_or_404(ArtistPortfolio, artist=request.user)
    
    if request.method == 'POST':
        form = PortfolioMediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.portfolio = portfolio
            media.save()
            messages.success(request, 'Media added successfully!')
            return redirect('artists:my_portfolio')
    else:
        form = PortfolioMediaForm()
    
    context = {
        'form': form,
        'portfolio': portfolio,
    }
    return render(request, 'artists/add_media.html', context)


@login_required
def edit_media(request, pk):
    """Edit portfolio media."""
    media = get_object_or_404(PortfolioMedia, pk=pk, portfolio__artist=request.user)
    
    if request.method == 'POST':
        form = PortfolioMediaForm(request.POST, request.FILES, instance=media)
        if form.is_valid():
            form.save()
            messages.success(request, 'Media updated successfully!')
            return redirect('artists:my_portfolio')
    else:
        form = PortfolioMediaForm(instance=media)
    
    context = {
        'form': form,
        'media': media,
    }
    return render(request, 'artists/edit_media.html', context)


@login_required
def delete_media(request, pk):
    """Delete portfolio media."""
    media = get_object_or_404(PortfolioMedia, pk=pk, portfolio__artist=request.user)
    
    if request.method == 'POST':
        media.delete()
        messages.success(request, 'Media deleted successfully!')
        return redirect('artists:my_portfolio')
    
    context = {
        'media': media,
    }
    return render(request, 'artists/delete_media.html', context)


@login_required
def add_performance(request):
    """Add past performance to portfolio."""
    if request.user.user_type != 'artist':
        messages.error(request, 'Only artists can add performances.')
        return redirect('artists:my_portfolio')
    
    portfolio = get_object_or_404(ArtistPortfolio, artist=request.user)
    
    if request.method == 'POST':
        # Handle performance creation
        title = request.POST.get('title')
        venue_name = request.POST.get('venue_name')
        event_date = request.POST.get('event_date')
        event_type = request.POST.get('event_type')
        duration = request.POST.get('duration')
        audience_size = request.POST.get('audience_size')
        description = request.POST.get('description')
        client_feedback = request.POST.get('client_feedback')
        rating = request.POST.get('rating')
        
        if title and venue_name and event_date:
            duration_timedelta = _parse_duration(duration)
            performance = Performance.objects.create(
                portfolio=portfolio,
                title=title,
                venue_name=venue_name,
                event_date=event_date,
                event_type=event_type,
                duration=duration_timedelta,
                audience_size=int(audience_size) if audience_size else None,
                description=description,
                client_feedback=client_feedback,
                rating=int(rating) if rating else None,
            )
            messages.success(request, 'Performance added successfully!')
            return redirect('artists:my_portfolio')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    context = {
        'portfolio': portfolio,
    }
    return render(request, 'artists/add_performance.html', context)


@login_required
def manage_availability(request):
    """Manage artist availability calendar."""
    if request.user.user_type != 'artist':
        messages.error(request, 'Only artists can manage availability.')
        return redirect('artists:my_portfolio')
    
    if request.method == 'POST':
        # Handle availability updates
        date = request.POST.get('date')
        status = request.POST.get('status')
        morning = request.POST.get('morning') == 'on'
        afternoon = request.POST.get('afternoon') == 'on'
        evening = request.POST.get('evening') == 'on'
        notes = request.POST.get('notes')
        
        if date and status:
            availability, created = Availability.objects.get_or_create(
                artist=request.user,
                date=date,
                defaults={
                    'availability_status': status,
                    'morning_available': morning,
                    'afternoon_available': afternoon,
                    'evening_available': evening,
                    'notes': notes,
                }
            )
            
            if not created:
                availability.availability_status = status
                availability.morning_available = morning
                availability.afternoon_available = afternoon
                availability.evening_available = evening
                availability.notes = notes
                availability.save()
            
            messages.success(request, 'Availability updated successfully!')
            return redirect('artists:manage_availability')
    
    # Get current availability
    availability_entries = request.user.availability.all().order_by('date')
    
    context = {
        'availability_entries': availability_entries,
    }
    return render(request, 'artists/manage_availability.html', context)


# API Views
@login_required
def artist_search_api(request):
    """API endpoint for artist search."""
    query = request.GET.get('q', '')
    artists = ArtistPortfolio.objects.filter(
        Q(artist__first_name__icontains=query) |
        Q(artist__last_name__icontains=query) |
        Q(headline__icontains=query),
        is_available=True
    )[:10]
    
    data = [{
        'id': artist.id,
        'name': f"{artist.artist.first_name} {artist.artist.last_name}",
        'headline': artist.headline,
        'genres': artist.genres,
        'base_rate': str(artist.get_display_rate()),
        'city': artist.artist.artist_profile.city if hasattr(artist.artist, 'artist_profile') else '',
    } for artist in artists]
    
    return JsonResponse({'results': data})


@login_required
def artist_availability_api(request, artist_pk):
    """API endpoint for artist availability."""
    artist = get_object_or_404(ArtistPortfolio, pk=artist_pk)
    availability = artist.artist.availability.all()
    
    availability_data = [{
        'id': entry.id, # Added ID for editing/deleting
        'date': entry.date.strftime('%Y-%m-%d'),
        'status': entry.availability_status,
        'morning': entry.morning_available,
        'afternoon': entry.afternoon_available,
        'evening': entry.evening_available,
    } for entry in availability]
    
    return JsonResponse({'availability': availability_data})


@login_required
def edit_performance(request, pk):
    """Edit a past performance."""
    performance = get_object_or_404(Performance, pk=pk, portfolio__artist=request.user)
    
    if request.method == 'POST':
        form = PerformanceForm(request.POST, instance=performance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Performance updated successfully!')
            return redirect('artists:my_portfolio')
    else:
        form = PerformanceForm(instance=performance)
    
    context = {
        'form': form,
        'performance': performance,
    }
    return render(request, 'artists/edit_performance.html', context)


@login_required
def delete_performance(request, pk):
    """Delete a past performance."""
    performance = get_object_or_404(Performance, pk=pk, portfolio__artist=request.user)
    
    if request.method == 'POST':
        performance.delete()
        messages.success(request, 'Performance deleted successfully!')
        return redirect('artists:my_portfolio')
    
    context = {
        'performance': performance,
    }
    return render(request, 'artists/delete_performance.html', context)


@login_required
def edit_availability(request, pk):
    """Edit an availability slot."""
    availability = get_object_or_404(Availability, pk=pk, artist=request.user)
    
    if request.method == 'POST':
        form = AvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            form.save()
            messages.success(request, 'Availability updated successfully!')
            return redirect('artists:my_portfolio')
    else:
        form = AvailabilityForm(instance=availability)
    
    context = {
        'form': form,
        'availability': availability,
    }
    return render(request, 'artists/edit_availability.html', context)


@login_required
def delete_availability(request, pk):
    """Delete an availability slot."""
    availability = get_object_or_404(Availability, pk=pk, artist=request.user)
    
    if request.method == 'POST':
        availability.delete()
        messages.success(request, 'Availability deleted successfully!')
        return redirect('artists:my_portfolio')
    
    context = {
        'availability': availability,
    }
    return render(request, 'artists/delete_availability.html', context)
