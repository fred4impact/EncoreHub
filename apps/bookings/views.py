from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Event, BookingRequest, Booking, Contract
from .forms import EventForm, BookingRequestForm, DirectArtistBookingForm


def event_list(request):
    """List all events with filtering options."""
    events = Event.objects.filter(status='published')
    
    # Filter by event type
    event_type = request.GET.get('event_type')
    if event_type:
        events = events.filter(event_type=event_type)
    
    # Filter by location
    city = request.GET.get('city')
    if city:
        events = events.filter(city__icontains=city)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        events = events.filter(event_date__gte=date_from)
    if date_to:
        events = events.filter(event_date__lte=date_to)
    
    # Filter by budget
    budget_min = request.GET.get('budget_min')
    budget_max = request.GET.get('budget_max')
    if budget_min:
        events = events.filter(budget_max__gte=budget_min)
    if budget_max:
        events = events.filter(budget_min__lte=budget_max)
    
    context = {
        'events': events,
        'event_types': Event.EVENT_TYPE_CHOICES,
    }
    return render(request, 'bookings/event_list.html', context)


@login_required
def event_detail(request, pk):
    """Show event details and allow booking requests."""
    event = get_object_or_404(Event, pk=pk, status='published')
    
    # Check if user has already made a booking request
    existing_request = None
    if request.user.user_type == 'artist':
        existing_request = BookingRequest.objects.filter(
            event=event,
            artist=request.user
        ).first()
    
    context = {
        'event': event,
        'existing_request': existing_request,
    }
    return render(request, 'bookings/event_detail.html', context)


@login_required
def create_event(request):
    """Create a new event (for venues)."""
    if request.user.user_type != 'venue':
        messages.error(request, 'Only venues can create events.')
        return redirect('bookings:event_list')
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.venue = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('bookings:event_detail', pk=event.pk)
    else:
        form = EventForm()
    
    context = {
        'form': form,
        'title': 'Create New Event'
    }
    return render(request, 'bookings/event_form.html', context)


@login_required
def edit_event(request, pk):
    """Edit an existing event."""
    event = get_object_or_404(Event, pk=pk, venue=request.user)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('bookings:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'title': 'Edit Event'
    }
    return render(request, 'bookings/event_form.html', context)


@login_required
def create_booking_request(request, event_pk):
    """Create a booking request for an event."""
    if request.user.user_type != 'artist':
        messages.error(request, 'Only artists can create booking requests.')
        return redirect('bookings:event_detail', pk=event_pk)
    
    event = get_object_or_404(Event, pk=event_pk, status='published')
    
    # Check if request already exists
    existing_request = BookingRequest.objects.filter(
        event=event,
        artist=request.user
    ).first()
    
    if existing_request:
        messages.warning(request, 'You have already submitted a booking request for this event.')
        return redirect('bookings:event_detail', pk=event_pk)
    
    if request.method == 'POST':
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking_request = form.save(commit=False)
            booking_request.event = event
            booking_request.artist = request.user
            booking_request.expires_at = timezone.now() + timedelta(days=7)  # 7 days to respond
            booking_request.save()
            
            messages.success(request, 'Booking request submitted successfully!')
            return redirect('bookings:my_requests')
    else:
        form = BookingRequestForm()
    
    context = {
        'form': form,
        'event': event,
        'title': 'Submit Booking Request'
    }
    return render(request, 'bookings/booking_request_form.html', context)


@login_required
def my_requests(request):
    """Show user's booking requests."""
    if request.user.user_type == 'artist':
        requests = BookingRequest.objects.filter(artist=request.user)
    elif request.user.user_type == 'venue':
        requests = BookingRequest.objects.filter(event__venue=request.user)
    elif request.user.user_type == 'manager':
        requests = BookingRequest.objects.filter(manager=request.user)
    else:
        requests = BookingRequest.objects.none()
    
    context = {
        'requests': requests,
        'user_type': request.user.user_type
    }
    return render(request, 'bookings/my_requests.html', context)


@login_required
def request_detail(request, pk):
    """Show booking request details."""
    if request.user.user_type == 'artist':
        booking_request = get_object_or_404(BookingRequest, pk=pk, artist=request.user)
    elif request.user.user_type == 'venue':
        booking_request = get_object_or_404(BookingRequest, pk=pk, event__venue=request.user)
    elif request.user.user_type == 'manager':
        booking_request = get_object_or_404(BookingRequest, pk=pk, manager=request.user)
    else:
        messages.error(request, 'You do not have permission to view this request.')
        return redirect('bookings:my_requests')
    
    context = {
        'booking_request': booking_request,
        'user_type': request.user.user_type
    }
    return render(request, 'bookings/request_detail.html', context)


@login_required
def respond_to_request(request, pk):
    """Respond to a booking request (accept/decline). Venue responds to event-based requests; artist responds to direct requests."""
    booking_request = get_object_or_404(BookingRequest, pk=pk)
    # Who can respond: venue for event-based, artist for direct
    can_respond = False
    if booking_request.event:
        can_respond = booking_request.event.venue_id == request.user.id
    else:
        can_respond = booking_request.artist_id == request.user.id
    if not can_respond:
        messages.error(request, 'You do not have permission to respond to this request.')
        return redirect('bookings:request_detail', pk=pk)
    
    if booking_request.status != 'pending':
        messages.error(request, 'This request has already been responded to.')
        return redirect('bookings:request_detail', pk=pk)
    if booking_request.is_expired:
        messages.error(request, 'This request has expired.')
        return redirect('bookings:request_detail', pk=pk)
    
    if request.method == 'POST':
        response = request.POST.get('response')
        if response in ['accepted', 'declined']:
            booking_request.status = response
            booking_request.responded_at = timezone.now()
            booking_request.save()
            
            if response == 'accepted' and booking_request.event:
                # Create a booking (only for event-based requests; Booking requires event)
                booking = Booking.objects.create(
                    booking_request=booking_request,
                    event=booking_request.event,
                    artist=booking_request.artist,
                    venue=booking_request.event.venue,
                    manager=booking_request.manager,
                    agreed_fee=booking_request.proposed_fee or Decimal('0'),
                    performance_duration=timedelta(hours=2),
                )
                Contract.objects.create(
                    booking=booking,
                    terms_and_conditions="Standard performance contract terms...",
                    expires_at=timezone.now() + timedelta(days=30)
                )
                messages.success(request, 'Booking request accepted! A booking has been created.')
            elif response == 'accepted' and not booking_request.event:
                messages.success(request, 'Booking request accepted! You can coordinate details with the requester.')
            else:
                messages.success(request, 'Booking request declined.')
            
            return redirect('bookings:my_requests')
    
    context = {'booking_request': booking_request}
    return render(request, 'bookings/respond_to_request.html', context)


@login_required
def my_bookings(request):
    """Show user's bookings."""
    if request.user.user_type == 'artist':
        bookings = Booking.objects.filter(artist=request.user)
    elif request.user.user_type == 'venue':
        bookings = Booking.objects.filter(venue=request.user)
    elif request.user.user_type == 'manager':
        bookings = Booking.objects.filter(manager=request.user)
    else:
        bookings = Booking.objects.none()
    
    context = {
        'bookings': bookings,
        'user_type': request.user.user_type
    }
    return render(request, 'bookings/my_bookings.html', context)


@login_required
def booking_detail(request, pk):
    """Show booking details."""
    if request.user.user_type == 'artist':
        booking = get_object_or_404(Booking, pk=pk, artist=request.user)
    elif request.user.user_type == 'venue':
        booking = get_object_or_404(Booking, pk=pk, venue=request.user)
    elif request.user.user_type == 'manager':
        booking = get_object_or_404(Booking, pk=pk, manager=request.user)
    else:
        messages.error(request, 'You do not have permission to view this booking.')
        return redirect('bookings:my_bookings')
    
    context = {
        'booking': booking,
        'user_type': request.user.user_type
    }
    return render(request, 'bookings/booking_detail.html', context)


# API Views for AJAX requests
@login_required
def event_search_api(request):
    """API endpoint for event search."""
    query = request.GET.get('q', '')
    events = Event.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query) |
        Q(city__icontains=query),
        status='published'
    )[:10]
    
    data = [{
        'id': event.id,
        'title': event.title,
        'event_type': event.get_event_type_display(),
        'date': event.event_date.strftime('%Y-%m-%d'),
        'city': event.city,
        'budget_range': event.budget_range
    } for event in events]
    
    return JsonResponse({'results': data})


@login_required
def create_artist_booking_request(request, portfolio_pk):
    """Create a booking request for an artist (direct booking). Only venues and managers can book; artists cannot book themselves."""
    from apps.artists.models import ArtistPortfolio
    portfolio = get_object_or_404(ArtistPortfolio, pk=portfolio_pk)

    # Artists cannot book themselves
    if request.user == portfolio.artist:
        messages.error(request, 'You cannot book yourself.')
        return redirect('artists:detail', pk=portfolio_pk)

    # Only venues and managers can book artists
    if request.user.user_type not in ('venue', 'manager'):
        messages.error(request, 'Only venues and managers can book artists. Please log in with a venue or manager account.')
        return redirect('artists:detail', pk=portfolio_pk)

    # Check if request already exists
    existing_request = BookingRequest.objects.filter(
        artist=portfolio.artist,
        requester=request.user
    ).first()
    
    if existing_request:
        messages.warning(request, 'You have already submitted a booking request for this artist.')
        return redirect('artists:detail', pk=portfolio_pk)
    
    if request.method == 'POST':
        form = DirectArtistBookingForm(request.POST)
        if form.is_valid():
            booking_request = form.save(commit=False)
            booking_request.artist = portfolio.artist
            booking_request.requester = request.user
            booking_request.requester_type = request.user.user_type
            booking_request.expires_at = timezone.now() + timedelta(days=7)  # 7 days to respond
            booking_request.save()
            
            messages.success(request, 'Booking request submitted successfully!')
            return redirect('bookings:my_requests')
    else:
        form = DirectArtistBookingForm()
    
    context = {
        'form': form,
        'portfolio': portfolio,
        'title': 'Book Artist'
    }
    return render(request, 'bookings/artist_booking_request_form.html', context)
