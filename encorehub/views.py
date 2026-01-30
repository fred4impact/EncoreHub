"""Project-level views (e.g. home page)."""
from django.shortcuts import render
from apps.artists.models import ArtistPortfolio


def home(request):
    """Home page with featured/recent artists."""
    featured_artists = ArtistPortfolio.objects.filter(
        is_available=True
    ).select_related('artist', 'artist__artist_profile').order_by('-created_at')[:4]
    return render(request, 'home.html', {'featured_artists': featured_artists})
