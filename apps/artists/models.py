from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


class ArtistPortfolio(models.Model):
    """Artist portfolio with media and performance information."""
    
    artist = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='portfolio',
        limit_choices_to={'user_type': 'artist'}
    )
    
    # Portfolio details
    headline = models.CharField(max_length=200, blank=True)
    bio = models.TextField(default="")
    genres = models.JSONField(default=list)  # List of genres
    instruments = models.JSONField(default=list)  # List of instruments
    
    # Performance details
    performance_types = models.JSONField(default=list)  # Solo, Band, Duo, etc.
    set_lengths = models.JSONField(default=list)  # 30min, 1hr, 2hr, etc.
    
    # Pricing
    base_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pricing_notes = models.TextField(blank=True)
    
    # Availability
    is_available = models.BooleanField(default=True)
    availability_notes = models.TextField(blank=True)
    
    # Social media
    social_links = models.JSONField(default=dict)  # {platform: url}
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('artist portfolio')
        verbose_name_plural = _('artist portfolios')
    
    def __str__(self):
        return f"Portfolio - {self.artist.get_full_name()}"


class PortfolioMedia(models.Model):
    """Media files for artist portfolio."""
    
    MEDIA_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
    ]
    
    portfolio = models.ForeignKey(
        ArtistPortfolio,
        on_delete=models.CASCADE,
        related_name='media'
    )
    
    # Media details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES)
    
    # File upload
    file = models.FileField(
        upload_to='portfolio_media/%Y/%m/%d/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'mp3', 'wav', 'pdf', 'doc', 'docx']
            )
        ]
    )
    
    # Display settings
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    
    # Metadata
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('portfolio media')
        verbose_name_plural = _('portfolio media')
        ordering = ['display_order', '-uploaded_at']
    
    def __str__(self):
        return f"{self.title} - {self.portfolio.artist.get_full_name()}"


class Performance(models.Model):
    """Past performances for artist portfolio."""
    
    portfolio = models.ForeignKey(
        ArtistPortfolio,
        on_delete=models.CASCADE,
        related_name='performances'
    )
    
    # Performance details
    title = models.CharField(max_length=200)
    venue_name = models.CharField(max_length=200)
    event_date = models.DateField()
    event_type = models.CharField(max_length=100)
    
    # Performance info
    duration = models.DurationField()
    audience_size = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    
    # Media from performance
    photos = models.JSONField(default=list)  # List of photo URLs
    videos = models.JSONField(default=list)  # List of video URLs
    
    # Reviews/feedback
    client_feedback = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        null=True,
        blank=True
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('performance')
        verbose_name_plural = _('performances')
        ordering = ['-event_date']
    
    def __str__(self):
        return f"{self.title} - {self.venue_name}"


class Availability(models.Model):
    """Artist availability calendar."""
    
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
        ('maybe', 'Maybe Available'),
        ('booked', 'Booked'),
    ]
    
    artist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='availability'
    )
    
    # Date and availability
    date = models.DateField()
    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='available'
    )
    
    # Time slots
    morning_available = models.BooleanField(default=True)
    afternoon_available = models.BooleanField(default=True)
    evening_available = models.BooleanField(default=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('availability')
        verbose_name_plural = _('availability')
        ordering = ['date']
        unique_together = ['artist', 'date']
    
    def __str__(self):
        return f"{self.artist.get_full_name()} - {self.date}"


class ArtistReview(models.Model):
    """Reviews from clients/venues."""
    
    artist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_reviews'
    )
    booking = models.ForeignKey(
        'bookings.Booking',
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True
    )
    
    # Review details
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    title = models.CharField(max_length=200)
    review_text = models.TextField()
    
    # Review categories
    professionalism = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    performance_quality = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    communication = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    value_for_money = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    
    # Review status
    is_public = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('artist review')
        verbose_name_plural = _('artist reviews')
        ordering = ['-created_at']
        unique_together = ['artist', 'reviewer', 'booking']
    
    def __str__(self):
        return f"Review by {self.reviewer.get_full_name()} for {self.artist.get_full_name()}"
    
    @property
    def average_rating(self):
        ratings = [
            self.professionalism,
            self.performance_quality,
            self.communication,
            self.value_for_money
        ]
        return sum(ratings) / len(ratings)
