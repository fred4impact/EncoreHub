from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Event, BookingRequest


class EventForm(forms.ModelForm):
    """Form for creating and editing events."""
    
    class Meta:
        model = Event
        fields = [
            'title', 'event_type', 'description', 'venue_name', 'address',
            'city', 'state', 'country', 'event_date', 'start_time', 'end_time',
            'setup_time', 'expected_attendance', 'capacity', 'budget_min',
            'budget_max', 'payment_terms', 'technical_requirements',
            'equipment_provided', 'equipment_needed'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'venue_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'setup_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'expected_attendance': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'budget_min': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'budget_max': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_terms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'technical_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'equipment_provided': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'equipment_needed': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_event_date(self):
        """Ensure event date is in the future."""
        event_date = self.cleaned_data.get('event_date')
        if event_date and event_date < timezone.now().date():
            raise forms.ValidationError("Event date must be in the future.")
        return event_date
    
    def clean(self):
        """Validate budget range and time range."""
        cleaned_data = super().clean()
        budget_min = cleaned_data.get('budget_min')
        budget_max = cleaned_data.get('budget_max')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if budget_min and budget_max and budget_min > budget_max:
            raise forms.ValidationError("Minimum budget cannot be greater than maximum budget.")
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")
        
        return cleaned_data


class BookingRequestForm(forms.ModelForm):
    """Form for creating booking requests."""
    
    class Meta:
        model = BookingRequest
        fields = ['message', 'proposed_fee', 'special_requirements']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell the venue about your interest in this event and why you would be a great fit...'
            }),
            'proposed_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Enter your proposed fee for this performance'
            }),
            'special_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requirements or requests...'
            }),
        }
    
    def clean_proposed_fee(self):
        """Ensure proposed fee is positive."""
        fee = self.cleaned_data.get('proposed_fee')
        if fee and fee <= 0:
            raise forms.ValidationError("Proposed fee must be greater than zero.")
        return fee


class EventFilterForm(forms.Form):
    """Form for filtering events."""
    
    event_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Event.EVENT_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    budget_min = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Budget',
            'step': '0.01'
        })
    )
    
    budget_max = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Budget',
            'step': '0.01'
        })
    )
    
    def clean(self):
        """Validate date range and budget range."""
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        budget_min = cleaned_data.get('budget_min')
        budget_max = cleaned_data.get('budget_max')
        
        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError("Start date cannot be after end date.")
        
        if budget_min and budget_max and budget_min > budget_max:
            raise forms.ValidationError("Minimum budget cannot be greater than maximum budget.")
        
        return cleaned_data


class DirectArtistBookingForm(forms.ModelForm):
    """Form for creating direct artist booking requests."""
    
    class Meta:
        model = BookingRequest
        fields = [
            'event_name', 'event_date', 'event_time', 'event_type', 
            'venue_location', 'duration', 'budget', 'audience_size',
            'description', 'special_requirements'
        ]
        widgets = {
            'event_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Summer Wedding Reception'
            }),
            'event_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'event_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-select'
            }, choices=[
                ('', 'Select event type...'),
                ('wedding', 'Wedding'),
                ('corporate', 'Corporate Event'),
                ('birthday', 'Birthday Party'),
                ('anniversary', 'Anniversary'),
                ('concert', 'Concert'),
                ('festival', 'Festival'),
                ('private', 'Private Event'),
                ('other', 'Other'),
            ]),
            'venue_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Grand Hotel Ballroom'
            }),
            'duration': forms.Select(attrs={
                'class': 'form-select'
            }, choices=[
                ('', 'Select duration...'),
                ('30min', '30 minutes'),
                ('1hour', '1 hour'),
                ('1.5hours', '1.5 hours'),
                ('2hours', '2 hours'),
                ('3hours', '3 hours'),
                ('4hours', '4 hours'),
                ('full_day', 'Full day'),
            ]),
            'budget': forms.Select(attrs={
                'class': 'form-select'
            }, choices=[
                ('', 'Select budget range...'),
                ('under_500', 'Under $500'),
                ('500_1000', '$500 - $1,000'),
                ('1000_2000', '$1,000 - $2,000'),
                ('2000_5000', '$2,000 - $5,000'),
                ('5000_10000', '$5,000 - $10,000'),
                ('over_10000', 'Over $10,000'),
            ]),
            'audience_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 150',
                'min': '1'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your event, requirements, and any special requests...'
            }),
            'special_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any specific requirements, equipment needs, or special requests...'
            }),
        }
    
    def clean_event_date(self):
        """Ensure event date is in the future."""
        event_date = self.cleaned_data.get('event_date')
        if event_date and event_date < timezone.now().date():
            raise forms.ValidationError("Event date must be in the future.")
        return event_date
    
    def clean_audience_size(self):
        """Ensure audience size is positive."""
        audience_size = self.cleaned_data.get('audience_size')
        if audience_size and audience_size <= 0:
            raise forms.ValidationError("Audience size must be greater than zero.")
        return audience_size
