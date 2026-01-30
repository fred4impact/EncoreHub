from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class User(AbstractUser):
    """Custom User model with role-based functionality."""
    
    USER_TYPE_CHOICES = [
        ('artist', 'Artist'),
        ('venue', 'Venue'),
        ('manager', 'Manager'),
    ]
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        blank=True,
        null=True,
        help_text=_('Type of user account')
    )
    
    # Override email to be unique
    email = models.EmailField(_('email address'), unique=True)
    
    # Make username optional since we're using email
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )
    
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    @property
    def is_artist(self):
        return self.user_type == 'artist'
    
    @property
    def is_venue(self):
        return self.user_type == 'venue'
    
    @property
    def is_manager(self):
        return self.user_type == 'manager'


class ArtistProfile(models.Model):
    """Profile for artists with specific fields."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist_profile')
    
    # Basic info
    stage_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    genre = models.CharField(max_length=100, blank=True)
    
    # Contact & location
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Professional info
    experience_years = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Social media
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    youtube = models.CharField(max_length=100, blank=True)
    
    # Profile status
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('artist profile')
        verbose_name_plural = _('artist profiles')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - Artist Profile"


class VenueProfile(models.Model):
    """Profile for venues with specific fields."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='venue_profile')
    
    # Venue info
    venue_name = models.CharField(max_length=200)
    venue_type = models.CharField(max_length=100, blank=True)  # Club, Theater, Arena, etc.
    description = models.TextField(blank=True)
    
    # Contact & location
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Venue details
    capacity = models.PositiveIntegerField(null=True, blank=True)
    amenities = models.TextField(blank=True)  # JSON or comma-separated
    
    # Business info
    website = models.URLField(blank=True)
    business_hours = models.TextField(blank=True)
    
    # Profile status
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('venue profile')
        verbose_name_plural = _('venue profiles')
    
    def __str__(self):
        return f"{self.venue_name} - Venue Profile"


class ManagerProfile(models.Model):
    """Profile for managers with specific fields."""
    
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    
    # Manager info
    company_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=200, blank=True)  # Rock, Jazz, Pop, etc.
    
    # Contact & location
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Professional info
    experience_years = models.PositiveIntegerField(default=0)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)  # Percentage
    
    # Business info
    website = models.URLField(blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    
    # Verification System - NEW FIELDS
    business_license = models.FileField(upload_to='licenses/', blank=True, null=True)
    verification_status = models.CharField(
        max_length=20, 
        choices=VERIFICATION_STATUS_CHOICES, 
        default='pending'
    )
    verification_date = models.DateTimeField(blank=True, null=True)
    verification_notes = models.TextField(blank=True)
    business_address = models.TextField(blank=True)
    business_phone = models.CharField(max_length=20, blank=True)
    references = models.TextField(blank=True, help_text="Professional references")
    client_count = models.PositiveIntegerField(default=0, help_text="Number of artists currently managed")
    
    # Profile status
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('manager profile')
        verbose_name_plural = _('manager profiles')
    
    def __str__(self):
        return f"{self.company_name or self.user.get_full_name()} - Manager Profile"
    
    @property
    def verification_status_display(self):
        return dict(self.VERIFICATION_STATUS_CHOICES).get(self.verification_status, 'Unknown')
    
    @property
    def can_manage_artists(self):
        return self.verification_status == 'verified' and self.client_count > 0
    
    def mark_verified(self, notes=""):
        """Mark manager as verified with optional notes."""
        from django.utils import timezone
        self.verification_status = 'verified'
        self.verification_date = timezone.now()
        self.verification_notes = notes
        self.is_verified = True
        self.save()
    
    def mark_rejected(self, notes=""):
        """Mark manager as rejected with optional notes."""
        self.verification_status = 'rejected'
        self.verification_notes = notes
        self.is_verified = False
        self.save()
