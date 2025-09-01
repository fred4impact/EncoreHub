from django.contrib import admin
from django.utils.html import format_html
from .models import ArtistPortfolio, PortfolioMedia, Performance, Availability, ArtistReview


@admin.register(ArtistPortfolio)
class ArtistPortfolioAdmin(admin.ModelAdmin):
    list_display = ['artist', 'headline', 'base_rate', 'is_available', 'created_at']
    list_filter = ['is_available', 'created_at']
    search_fields = ['artist__first_name', 'artist__last_name', 'headline', 'bio']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Artist Information', {
            'fields': ('artist', 'headline', 'bio')
        }),
        ('Performance Details', {
            'fields': ('genres', 'instruments', 'performance_types', 'set_lengths')
        }),
        ('Pricing & Availability', {
            'fields': ('base_rate', 'pricing_notes', 'is_available', 'availability_notes')
        }),
        ('Social Media', {
            'fields': ('social_links',)
        }),
    )


@admin.register(PortfolioMedia)
class PortfolioMediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'portfolio', 'media_type', 'is_featured', 'display_order', 'uploaded_at']
    list_filter = ['media_type', 'is_featured', 'uploaded_at']
    search_fields = ['title', 'description', 'portfolio__artist__first_name', 'portfolio__artist__last_name']
    list_editable = ['is_featured', 'display_order']
    date_hierarchy = 'uploaded_at'
    
    fieldsets = (
        ('Media Details', {
            'fields': ('portfolio', 'title', 'description', 'media_type')
        }),
        ('File Upload', {
            'fields': ('file',)
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'display_order')
        }),
    )


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['title', 'portfolio', 'venue_name', 'event_date', 'duration', 'rating', 'created_at']
    list_filter = ['event_date', 'rating', 'created_at']
    search_fields = ['title', 'venue_name', 'portfolio__artist__first_name', 'portfolio__artist__last_name']
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Performance Details', {
            'fields': ('portfolio', 'title', 'venue_name', 'event_date', 'event_type')
        }),
        ('Performance Info', {
            'fields': ('duration', 'audience_size', 'description')
        }),
        ('Media & Feedback', {
            'fields': ('photos', 'videos', 'client_feedback', 'rating')
        }),
    )


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['artist', 'date', 'availability_status', 'time_slots', 'created_at']
    list_filter = ['availability_status', 'date', 'created_at']
    search_fields = ['artist__first_name', 'artist__last_name', 'notes']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Availability Details', {
            'fields': ('artist', 'date', 'availability_status')
        }),
        ('Time Slots', {
            'fields': ('morning_available', 'afternoon_available', 'evening_available')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )
    
    def time_slots(self, obj):
        slots = []
        if obj.morning_available:
            slots.append('Morning')
        if obj.afternoon_available:
            slots.append('Afternoon')
        if obj.evening_available:
            slots.append('Evening')
        return ', '.join(slots) if slots else 'None'
    time_slots.short_description = 'Available Time Slots'


@admin.register(ArtistReview)
class ArtistReviewAdmin(admin.ModelAdmin):
    list_display = ['artist', 'reviewer', 'rating', 'title', 'is_public', 'is_verified', 'created_at']
    list_filter = ['rating', 'is_public', 'is_verified', 'created_at']
    search_fields = ['artist__first_name', 'artist__last_name', 'reviewer__first_name', 'reviewer__last_name', 'title']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Review Details', {
            'fields': ('artist', 'reviewer', 'booking', 'title', 'review_text')
        }),
        ('Ratings', {
            'fields': ('rating', 'professionalism', 'performance_quality', 'communication', 'value_for_money')
        }),
        ('Status', {
            'fields': ('is_public', 'is_verified')
        }),
    )
    
    def average_rating_display(self, obj):
        return f"{obj.average_rating:.1f}/5.0"
    average_rating_display.short_description = 'Average Rating'
