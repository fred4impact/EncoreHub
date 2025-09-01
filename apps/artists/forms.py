from django import forms
from .models import ArtistPortfolio, PortfolioMedia, Performance, Availability


class ArtistPortfolioForm(forms.ModelForm):
    """Form for creating and editing artist portfolios."""
    
    class Meta:
        model = ArtistPortfolio
        fields = [
            'headline', 'bio', 'genres', 'instruments', 'performance_types',
            'set_lengths', 'base_rate', 'pricing_notes', 'is_available',
            'availability_notes', 'social_links'
        ]
        widgets = {
            'headline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., "Award-winning Jazz Vocalist"'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell your story, experience, and what makes you unique...'
            }),
            'genres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Jazz, Blues, R&B (comma separated)'
            }),
            'instruments': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Vocals, Piano, Guitar (comma separated)'
            }),
            'performance_types': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Solo, Duo, Band (comma separated)'
            }),
            'set_lengths': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 30min, 1hr, 2hr (comma separated)'
            }),
            'base_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Your base rate per performance'
            }),
            'pricing_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any notes about pricing, packages, or special rates...'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'availability_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any notes about your availability...'
            }),
            'social_links': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '{"instagram": "https://instagram.com/...", "youtube": "https://youtube.com/..."}'
            }),
        }
    
    def clean_genres(self):
        """Convert comma-separated string to list."""
        genres = self.cleaned_data.get('genres')
        if isinstance(genres, str):
            return [genre.strip() for genre in genres.split(',') if genre.strip()]
        return genres
    
    def clean_instruments(self):
        """Convert comma-separated string to list."""
        instruments = self.cleaned_data.get('instruments')
        if isinstance(instruments, str):
            return [instrument.strip() for instrument in instruments.split(',') if instrument.strip()]
        return instruments
    
    def clean_performance_types(self):
        """Convert comma-separated string to list."""
        performance_types = self.cleaned_data.get('performance_types')
        if isinstance(performance_types, str):
            return [pt.strip() for pt in performance_types.split(',') if pt.strip()]
        return performance_types
    
    def clean_set_lengths(self):
        """Convert comma-separated string to list."""
        set_lengths = self.cleaned_data.get('set_lengths')
        if isinstance(set_lengths, str):
            return [sl.strip() for sl in set_lengths.split(',') if sl.strip()]
        return set_lengths
    
    def clean_base_rate(self):
        """Ensure base rate is positive."""
        rate = self.cleaned_data.get('base_rate')
        if rate and rate <= 0:
            raise forms.ValidationError("Base rate must be greater than zero.")
        return rate


class PortfolioMediaForm(forms.ModelForm):
    """Form for adding portfolio media."""
    
    class Meta:
        model = PortfolioMedia
        fields = ['title', 'description', 'media_type', 'file', 'is_featured', 'display_order']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., "Live Performance at Blue Note"'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description of this media...'
            }),
            'media_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Display order (lower numbers first)'
            }),
        }
    
    def clean_file(self):
        """Validate file upload."""
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 10MB)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be less than 10MB.")
            
            # Check file extension
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'mp3', 'wav', 'pdf', 'doc', 'docx']
            file_extension = file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError(f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}")
        
        return file


class ArtistSearchForm(forms.Form):
    """Form for searching artists."""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search artists by name, genre, or location...'
        })
    )
    
    genre = forms.ChoiceField(
        choices=[('', 'All Genres')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        })
    )
    
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Price',
            'step': '0.01'
        })
    )
    
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Price',
            'step': '0.01'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate genre choices
        from .models import ArtistPortfolio
        all_genres = set()
        for portfolio in ArtistPortfolio.objects.all():
            all_genres.update(portfolio.genres)
        
        genre_choices = [('', 'All Genres')] + [(genre, genre) for genre in sorted(all_genres)]
        self.fields['genre'].choices = genre_choices
    
    def clean(self):
        """Validate price range."""
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        
        if min_price and max_price and min_price > max_price:
            raise forms.ValidationError("Minimum price cannot be greater than maximum price.")
        
        return cleaned_data


class PerformanceForm(forms.Form):
    """Form for adding past performances."""
    
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Performance title'
        })
    )
    
    venue_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Venue name'
        })
    )
    
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    event_type = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Concert, Wedding, Corporate Event'
        })
    )
    
    duration = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 2 hours'
        })
    )
    
    audience_size = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of attendees'
        })
    )
    
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Description of the performance...'
        })
    )
    
    client_feedback = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Feedback from the client...'
        })
    )
    
    rating = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


class AvailabilityForm(forms.ModelForm):
    """Form for managing artist availability."""
    
    class Meta:
        model = Availability
        fields = ['date', 'availability_status', 'morning_available', 'afternoon_available', 'evening_available', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'availability_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'morning_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'afternoon_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'evening_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any notes about this date...'
            }),
        }
