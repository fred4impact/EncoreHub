from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import ArtistProfile, VenueProfile, ManagerProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create role profile when user is created or when user_type is set (signup sets user_type after first save)."""
    if not instance.user_type:
        return
    if instance.user_type == 'artist':
        ArtistProfile.objects.get_or_create(user=instance)
    elif instance.user_type == 'venue':
        VenueProfile.objects.get_or_create(user=instance)
    elif instance.user_type == 'manager':
        ManagerProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Keep profile in sync when user is updated (avoid reverse relation errors)."""
    if hasattr(instance, 'artist_profile'):
        instance.artist_profile.save()
    elif hasattr(instance, 'venue_profile'):
        instance.venue_profile.save()
    elif hasattr(instance, 'manager_profile'):
        instance.manager_profile.save()
