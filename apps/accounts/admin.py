from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ArtistProfile, VenueProfile, ManagerProfile

class ArtistProfileInline(admin.StackedInline):
    model = ArtistProfile
    can_delete = False
    verbose_name_plural = 'Artist Profile'
    fk_name = 'user'

class VenueProfileInline(admin.StackedInline):
    model = VenueProfile
    can_delete = False
    verbose_name_plural = 'Venue Profile'
    fk_name = 'user'

class ManagerProfileInline(admin.StackedInline):
    model = ManagerProfile
    can_delete = False
    verbose_name_plural = 'Manager Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ArtistProfileInline, VenueProfileInline, ManagerProfileInline)
    list_display = ('username', 'email', 'user_type', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('EncoreHub Profile', {'fields': ('user_type', 'phone', 'address', 'bio', 'profile_picture')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('EncoreHub Profile', {'fields': ('user_type', 'phone', 'address', 'bio', 'profile_picture')}),
    )

@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'stage_name', 'genre', 'city', 'experience_years', 'hourly_rate', 'is_verified', 'is_available')
    list_filter = ('genre', 'is_verified', 'is_available', 'city', 'state', 'country')
    search_fields = ('user__username', 'user__email', 'stage_name', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'stage_name', 'bio', 'genre')
        }),
        ('Contact & Location', {
            'fields': ('phone', 'city', 'state', 'country')
        }),
        ('Professional Information', {
            'fields': ('experience_years', 'hourly_rate')
        }),
        ('Social Media', {
            'fields': ('website', 'instagram', 'facebook', 'youtube')
        }),
        ('Profile Status', {
            'fields': ('is_verified', 'is_available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(VenueProfile)
class VenueProfileAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'user', 'venue_type', 'city', 'capacity', 'is_verified', 'is_active')
    list_filter = ('venue_type', 'is_verified', 'is_active', 'city', 'state', 'country')
    search_fields = ('venue_name', 'user__username', 'user__email', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Venue Information', {
            'fields': ('user', 'venue_name', 'venue_type', 'description')
        }),
        ('Contact & Location', {
            'fields': ('phone', 'address', 'city', 'state', 'country')
        }),
        ('Venue Details', {
            'fields': ('capacity', 'amenities')
        }),
        ('Business Information', {
            'fields': ('website', 'business_hours')
        }),
        ('Profile Status', {
            'fields': ('is_verified', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'specialization', 'city', 'verification_status', 'commission_rate', 'client_count', 'is_active')
    list_filter = ('verification_status', 'specialization', 'is_active', 'city', 'state', 'country')
    search_fields = ('company_name', 'user__username', 'user__email', 'bio')
    readonly_fields = ('created_at', 'updated_at', 'verification_date')
    actions = ['mark_verified', 'mark_rejected']
    
    fieldsets = (
        ('Manager Information', {
            'fields': ('user', 'company_name', 'bio', 'specialization')
        }),
        ('Contact & Location', {
            'fields': ('phone', 'city', 'state', 'country')
        }),
        ('Professional Information', {
            'fields': ('experience_years', 'commission_rate', 'client_count')
        }),
        ('Business Information', {
            'fields': ('website', 'linkedin', 'business_address', 'business_phone')
        }),
        ('Verification System', {
            'fields': ('business_license', 'verification_status', 'verification_date', 'verification_notes', 'references')
        }),
        ('Profile Status', {
            'fields': ('is_verified', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def mark_verified(self, request, queryset):
        """Mark selected managers as verified."""
        updated = queryset.update(verification_status='verified', is_verified=True)
        self.message_user(request, f'{updated} manager(s) marked as verified.')
    mark_verified.short_description = "Mark selected managers as verified"
    
    def mark_rejected(self, request, queryset):
        """Mark selected managers as rejected."""
        updated = queryset.update(verification_status='rejected', is_verified=False)
        self.message_user(request, f'{updated} manager(s) marked as rejected.')
    mark_rejected.short_description = "Mark selected managers as rejected"

# Register the custom user admin
admin.site.register(User, CustomUserAdmin)
