from django.contrib import admin
from django.utils.html import format_html
from .models import Event, BookingRequest, Booking, Contract


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'venue', 'event_type', 'event_date', 'status', 'budget_range', 'is_featured']
    list_filter = ['event_type', 'status', 'is_featured', 'event_date', 'city', 'state']
    search_fields = ['title', 'venue__first_name', 'venue__last_name', 'venue_name', 'city']
    list_editable = ['status', 'is_featured']
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'event_type', 'description', 'status', 'is_featured')
        }),
        ('Venue Information', {
            'fields': ('venue', 'venue_name', 'address', 'city', 'state', 'country')
        }),
        ('Event Timing', {
            'fields': ('event_date', 'start_time', 'end_time', 'setup_time')
        }),
        ('Capacity & Budget', {
            'fields': ('expected_attendance', 'capacity', 'budget_min', 'budget_max', 'payment_terms')
        }),
        ('Technical Requirements', {
            'fields': ('technical_requirements', 'equipment_provided', 'equipment_needed')
        }),
    )
    
    def budget_range(self, obj):
        return obj.budget_range
    budget_range.short_description = 'Budget Range'


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ['artist', 'event', 'proposed_fee', 'status', 'created_at', 'expires_at', 'is_expired_display']
    list_filter = ['status', 'created_at', 'expires_at']
    search_fields = ['artist__first_name', 'artist__last_name', 'event__title', 'message']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Request Details', {
            'fields': ('event', 'artist', 'manager', 'message', 'proposed_fee', 'special_requirements')
        }),
        ('Status & Timing', {
            'fields': ('status', 'expires_at', 'responded_at')
        }),
    )
    
    def is_expired_display(self, obj):
        if obj.is_expired:
            return format_html('<span style="color: red;">Expired</span>')
        return format_html('<span style="color: green;">Active</span>')
    is_expired_display.short_description = 'Expired'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['artist', 'event', 'venue', 'agreed_fee', 'status', 'confirmed_at', 'payment_status']
    list_filter = ['status', 'confirmed_at', 'deposit_paid', 'final_payment_paid']
    search_fields = ['artist__first_name', 'artist__last_name', 'event__title', 'venue__first_name', 'venue__last_name']
    date_hierarchy = 'confirmed_at'
    
    fieldsets = (
        ('Booking Details', {
            'fields': ('booking_request', 'event', 'artist', 'venue', 'manager', 'status')
        }),
        ('Contract Details', {
            'fields': ('agreed_fee', 'deposit_amount', 'deposit_paid', 'final_payment_paid')
        }),
        ('Performance Details', {
            'fields': ('performance_duration', 'set_list', 'special_requirements')
        }),
        ('Timing', {
            'fields': ('confirmed_at', 'completed_at')
        }),
    )
    
    def payment_status(self, obj):
        if obj.final_payment_paid:
            return format_html('<span style="color: green;">Paid in Full</span>')
        elif obj.deposit_paid:
            return format_html('<span style="color: orange;">Deposit Paid</span>')
        return format_html('<span style="color: red;">No Payment</span>')
    payment_status.short_description = 'Payment Status'


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['booking', 'contract_type', 'status', 'signature_status', 'expires_at', 'is_expired_display']
    list_filter = ['contract_type', 'status', 'expires_at']
    search_fields = ['booking__artist__first_name', 'booking__artist__last_name', 'booking__event__title']
    date_hierarchy = 'expires_at'
    
    fieldsets = (
        ('Contract Details', {
            'fields': ('booking', 'contract_type', 'status', 'expires_at')
        }),
        ('Contract Content', {
            'fields': ('terms_and_conditions', 'special_clauses')
        }),
        ('Signatures', {
            'fields': (
                'artist_signed', 'artist_signature_date',
                'venue_signed', 'venue_signature_date',
                'manager_signed', 'manager_signature_date'
            )
        }),
    )
    
    def signature_status(self, obj):
        if obj.is_fully_signed:
            return format_html('<span style="color: green;">Fully Signed</span>')
        elif obj.artist_signed or obj.venue_signed:
            return format_html('<span style="color: orange;">Partially Signed</span>')
        return format_html('<span style="color: red;">Not Signed</span>')
    signature_status.short_description = 'Signature Status'
    
    def is_expired_display(self, obj):
        if obj.is_expired:
            return format_html('<span style="color: red;">Expired</span>')
        return format_html('<span style="color: green;">Active</span>')
    is_expired_display.short_description = 'Expired'
