from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ArtistProfile, VenueProfile, ManagerProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'user_type'),
        }),
    )

@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'stage_name', 'genre', 'city', 'is_verified', 'is_available')
    list_filter = ('genre', 'city', 'is_verified', 'is_available')
    search_fields = ('user__email', 'stage_name', 'bio')
    raw_id_fields = ('user',)

@admin.register(VenueProfile)
class VenueProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'venue_name', 'venue_type', 'city', 'is_verified', 'is_active')
    list_filter = ('venue_type', 'city', 'is_verified', 'is_active')
    search_fields = ('user__email', 'venue_name', 'description')
    raw_id_fields = ('user',)

@admin.register(ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'city', 'is_verified', 'is_active')
    list_filter = ('city', 'is_verified', 'is_active')
    search_fields = ('user__email', 'company_name', 'bio')
    raw_id_fields = ('user',)
