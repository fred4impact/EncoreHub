# Test script for EncoreHub Booking System
# Run this in Django shell: python manage.py shell

from django.contrib.auth import get_user_model
from apps.bookings.models import Event, BookingRequest, Booking, Contract
from apps.artists.models import ArtistPortfolio, PortfolioMedia, Performance, Availability
from decimal import Decimal
from datetime import date, time, timedelta
from django.utils import timezone

User = get_user_model()

def create_test_data():
    """Create test data for the booking system."""
    print("Creating test data for EncoreHub...")
    
    # Create test users
    print("Creating test users...")
    
    # Create a venue
    venue = User.objects.create_user(
        email='venue@example.com',
        password='testpass123',
        first_name='Blue Note',
        last_name='Jazz Club',
        user_type='venue'
    )
    
    # Create an artist
    artist = User.objects.create_user(
        email='artist@example.com',
        password='testpass123',
        first_name='Sarah',
        last_name='Johnson',
        user_type='artist'
    )
    
    # Create a manager
    manager = User.objects.create_user(
        email='manager@example.com',
        password='testpass123',
        first_name='Mike',
        last_name='Manager',
        user_type='manager'
    )
    
    print(f"Created users: {venue.email}, {artist.email}, {manager.email}")
    
    # Create artist profile
    print("Creating artist portfolio...")
    portfolio = ArtistPortfolio.objects.create(
        artist=artist,
        headline="Award-winning Jazz Vocalist",
        bio="Sarah Johnson is a talented jazz vocalist with over 10 years of experience performing at prestigious venues across the country.",
        genres=['Jazz', 'Blues', 'R&B'],
        instruments=['Vocals', 'Piano'],
        performance_types=['Solo', 'Duo', 'Band'],
        set_lengths=['30min', '1hr', '2hr'],
        base_rate=Decimal('500.00'),
        is_available=True
    )
    
    # Create an event
    print("Creating test event...")
    event = Event.objects.create(
        title="Jazz Night at Blue Note",
        event_type='concert',
        description="Join us for an evening of smooth jazz featuring local and touring artists.",
        venue=venue,
        venue_name="Blue Note Jazz Club",
        address="123 Jazz Street",
        city="New York",
        state="NY",
        country="USA",
        event_date=date(2024, 12, 15),
        start_time=time(20, 0),
        end_time=time(23, 0),
        expected_attendance=150,
        capacity=200,
        budget_min=Decimal('400.00'),
        budget_max=Decimal('800.00'),
        status='published'
    )
    
    # Create a booking request
    print("Creating booking request...")
    booking_request = BookingRequest.objects.create(
        event=event,
        artist=artist,
        manager=manager,
        message="I would love to perform at your jazz night! I have extensive experience in jazz vocals and would be perfect for this event.",
        proposed_fee=Decimal('600.00'),
        special_requirements="I'll need a piano and microphone setup.",
        expires_at=timezone.now() + timedelta(days=7)
    )
    
    print("Test data created successfully!")
    print(f"Event: {event.title}")
    print(f"Artist: {artist.get_full_name()}")
    print(f"Venue: {venue.get_full_name()}")
    print(f"Booking Request: {booking_request}")
    
    return {
        'venue': venue,
        'artist': artist,
        'manager': manager,
        'event': event,
        'portfolio': portfolio,
        'booking_request': booking_request
    }

def test_booking_workflow():
    """Test the complete booking workflow."""
    print("\nTesting booking workflow...")
    
    # Create test data
    data = create_test_data()
    
    # Test event properties
    print(f"Event budget range: {data['event'].budget_range}")
    print(f"Event is upcoming: {data['event'].is_upcoming}")
    
    # Test booking request properties
    print(f"Booking request is expired: {data['booking_request'].is_expired}")
    
    # Test portfolio properties
    print(f"Artist genres: {data['portfolio'].genres}")
    print(f"Artist is available: {data['portfolio'].is_available}")
    
    print("Booking workflow test completed!")

if __name__ == "__main__":
    test_booking_workflow()
