from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class Event(models.Model):
    """Event model representing a performance opportunity."""
    
    EVENT_TYPE_CHOICES = [
        ('concert', 'Concert'),
        ('wedding', 'Wedding'),
        ('corporate', 'Corporate Event'),
        ('festival', 'Festival'),
        ('private_party', 'Private Party'),
        ('club_gig', 'Club Gig'),
        ('theater', 'Theater Performance'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    # Event details
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    description = models.TextField()
    
    # Venue/Client info
    venue = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hosted_events',
        limit_choices_to={'user_type': 'venue'}
    )
    venue_name = models.CharField(max_length=200, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    # Event timing
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    setup_time = models.TimeField(null=True, blank=True)
    
    # Capacity and requirements
    expected_attendance = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField(null=True, blank=True)
    
    # Budget and payment
    budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)
    payment_terms = models.TextField(blank=True)
    
    # Technical requirements
    technical_requirements = models.TextField(blank=True)
    equipment_provided = models.TextField(blank=True)
    equipment_needed = models.TextField(blank=True)
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ['-event_date']
    
    def __str__(self):
        return f"{self.title} - {self.event_date}"
    
    @property
    def budget_range(self):
        return f"${self.budget_min} - ${self.budget_max}"
    
    @property
    def is_upcoming(self):
        from django.utils import timezone
        return self.event_date >= timezone.now().date()


class BookingRequest(models.Model):
    """Booking request from venue to artist."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Request details - can be either event-based or direct artist booking
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        related_name='booking_requests',
        null=True,
        blank=True
    )
    artist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_requests',
        limit_choices_to={'user_type': 'artist'}
    )
    
    # For direct artist bookings (when event is null)
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_requests',
        null=True,
        blank=True
    )
    requester_type = models.CharField(
        max_length=20,
        choices=[('venue', 'Venue'), ('manager', 'Manager')],
        null=True,
        blank=True
    )
    
    # Event details for direct bookings
    event_name = models.CharField(max_length=200, blank=True)
    event_date = models.DateField(null=True, blank=True)
    event_time = models.TimeField(null=True, blank=True)
    event_type = models.CharField(max_length=50, blank=True)
    venue_location = models.CharField(max_length=200, blank=True)
    duration = models.CharField(max_length=50, blank=True)
    budget = models.CharField(max_length=50, blank=True)
    audience_size = models.PositiveIntegerField(null=True, blank=True)
    
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_requests',
        limit_choices_to={'user_type': 'manager'}
    )
    
    # Request details
    message = models.TextField(blank=True)
    proposed_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    special_requirements = models.TextField(blank=True)
    description = models.TextField(blank=True)
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    expires_at = models.DateTimeField()
    responded_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('booking request')
        verbose_name_plural = _('booking requests')
        ordering = ['-created_at']
        unique_together = ['event', 'artist']
    
    def __str__(self):
        if self.event:
            return f"{self.artist.get_full_name()} - {self.event.title}"
        else:
            return f"{self.artist.get_full_name()} - {self.event_name}"
    
    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at
    
    @property
    def is_direct_booking(self):
        return self.event is None


class Booking(models.Model):
    """Confirmed booking between artist and venue."""
    
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('disputed', 'Disputed'),
    ]
    
    # Booking details
    booking_request = models.OneToOneField(
        BookingRequest,
        on_delete=models.CASCADE,
        related_name='booking'
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    artist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='artist_bookings'
    )
    venue = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='venue_bookings'
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_bookings'
    )
    
    # Contract details
    agreed_fee = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    deposit_paid = models.BooleanField(default=False)
    final_payment_paid = models.BooleanField(default=False)
    
    # Performance details
    performance_duration = models.DurationField()
    set_list = models.TextField(blank=True)
    special_requirements = models.TextField(blank=True)
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    confirmed_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('booking')
        verbose_name_plural = _('bookings')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.artist.get_full_name()} - {self.event.title}"
    
    @property
    def total_paid(self):
        total = Decimal('0.00')
        if self.deposit_paid:
            total += self.deposit_amount
        if self.final_payment_paid:
            total += (self.agreed_fee - self.deposit_amount)
        return total
    
    @property
    def remaining_balance(self):
        return self.agreed_fee - self.total_paid


class Contract(models.Model):
    """Digital contract for bookings."""
    
    CONTRACT_TYPE_CHOICES = [
        ('standard', 'Standard Contract'),
        ('custom', 'Custom Contract'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending_signature', 'Pending Signature'),
        ('signed', 'Signed'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Contract details
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='contract')
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPE_CHOICES, default='standard')
    
    # Contract content
    terms_and_conditions = models.TextField()
    special_clauses = models.TextField(blank=True)
    
    # Signature tracking
    artist_signed = models.BooleanField(default=False)
    venue_signed = models.BooleanField(default=False)
    manager_signed = models.BooleanField(default=False)
    
    artist_signature_date = models.DateTimeField(null=True, blank=True)
    venue_signature_date = models.DateTimeField(null=True, blank=True)
    manager_signature_date = models.DateTimeField(null=True, blank=True)
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    expires_at = models.DateTimeField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('contract')
        verbose_name_plural = _('contracts')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Contract for {self.booking}"
    
    @property
    def is_fully_signed(self):
        required_signatures = ['artist_signed', 'venue_signed']
        if self.booking.manager:
            required_signatures.append('manager_signed')
        
        return all(getattr(self, sig) for sig in required_signatures)
    
    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at
