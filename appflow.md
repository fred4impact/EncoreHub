# EncoreHub App Flow Documentation

## Overview
This document outlines the current user use case flows for testing the existing EncoreHub application functionalities.

## Current Application Status
- ✅ Docker containers running
- ✅ Database migrations applied
- ✅ Core booking workflow implemented
- ✅ Artist portfolio system implemented
- ✅ JAZZMIN admin interface configured
- ✅ User authentication system (django-allauth)
- ✅ User profile pages with modern UI
- ✅ Proper redirect URLs after registration
- ✅ My Bookings page with comprehensive booking management
- ✅ Booking detail pages with participant information
- ✅ Edit Profile functionality with role-specific forms
- ✅ Dashboard with working action buttons and links
- ✅ Public artist and event discovery pages
- ✅ Fixed form field validation errors
- ✅ Role-based navigation with prominent action buttons
- ✅ Fixed portfolio creation NOT NULL constraint errors
- ✅ Complete portfolio management template with modern UI
- ✅ Fixed Availability model field mapping issues
- ✅ Modern home page with full-width hero banner and background image
- ✅ Pato-inspired elegant design with sophisticated typography and gold accents
- ✅ White text colors on banner and CTA section with full-width container
- ✅ Gold EncoreHub logo color (#d4af37) in navigation
- ✅ Gold button text colors (#1a1a1a) with gold backgrounds (#d4af37) throughout the site
- ✅ Complete artist detail template with hero section, bio, media gallery, and performances
- ✅ Complete availability management template with form and current availability display
- ✅ Complete add performance template with comprehensive performance details form
- ✅ Complete add media template with file upload, drag-and-drop, and preview functionality
- ✅ Recreated artist detail template after deletion with full functionality
- ✅ Direct artist booking system with comprehensive booking form and database model updates
- ✅ Consistent gold button styling across all application components (navbar, dashboard, forms, home page)
- ✅ Comprehensive gold theme implementation across all pages (login, signup, logout, dashboard, icons, links, form focus states)
- ✅ Hero banner repositioned inside content block with full-width CSS override for proper visibility
- ✅ Hero banner title "Connect Artists with Opportunities" styled in gold theme color (#d4af37)
- ✅ Comprehensive use case documentation created with detailed user flows for Julie (Artist), James (Manager), and Vortex Jazz Club (Venue)
- ✅ Business model analysis and recommendations created with manager-centric flow and revenue structure

## User Types & Roles
1. **Artist** - Musicians looking for gigs
2. **Venue** - Event spaces and organizers
3. **Manager** - Artist managers and booking agents

## User Use Case Flows

### 1. Artist User Flow

#### 1.1 Artist Registration & Onboarding
1. **Access**: Visit `http://localhost:8000/`
2. **Sign Up**: Click "Sign Up" → "Join as Artist"
3. **Registration Form**: Fill in:
   - Email: `artist@example.com`
   - Password: `testpass123`
   - User Type: `Artist`
4. **Email Verification**: Check console logs for verification link
5. **Profile Setup**: Complete artist profile with:
   - Stage name
   - Bio
   - Genre
   - Location (city, state, country)
   - Hourly rate
   - Social media links
6. **Dashboard Access**: After registration, you'll be redirected to the dashboard
7. **Profile Page**: Visit your profile at `http://localhost:8000/accounts/profile/`

#### 1.2 Artist Portfolio Management
1. **Access Portfolio**: Navigate to "My Portfolio" (after login)
   - **Main Navigation**: Prominent "My Portfolio" button in top navigation
   - **User Menu**: "My Portfolio" link in user dropdown menu
   - **Dashboard**: "Manage Portfolio" button in dashboard
2. **Create Portfolio**: Fill in:
   - Headline
   - Bio
   - Genres (JSON array: `["Jazz", "Blues"]`)
   - Instruments (JSON array: `["Piano", "Saxophone"]`)
   - Performance types (JSON array: `["Solo", "Band"]`)
   - Set lengths (JSON array: `["30min", "60min", "90min"]`)
   - Base rate: `150.00`
   - Pricing notes
   - Availability status
3. **Add Media**: Upload photos, videos, audio samples
4. **Add Past Performances**: Include venue, date, duration, audience size
5. **Set Availability**: Mark available dates and time slots
6. **Social Media**: Add Instagram, Facebook, YouTube links

#### 1.3 Artist Discovery & Booking
1. **Browse Events**: Visit `http://localhost:8000/bookings/events/`
2. **View Event Details**: Click on any event
3. **Submit Booking Request**: Fill in:
   - Message to venue
   - Proposed fee
   - Special requirements
4. **Track Requests**: View "My Requests" section
5. **Respond to Venue**: Accept/decline booking offers
6. **Manage Bookings**: Visit `http://localhost:8000/bookings/bookings/` to view all confirmed bookings
7. **View Booking Details**: Click on any booking to see detailed information

### 2. Venue User Flow

#### 2.1 Venue Registration & Onboarding
1. **Access**: Visit `http://localhost:8000/`
2. **Sign Up**: Click "Sign Up" → "Join as Venue"
3. **Registration Form**: Fill in:
   - Email: `venue@example.com`
   - Password: `testpass123`
   - User Type: `Venue`
4. **Email Verification**: Check console logs for verification link
5. **Profile Setup**: Complete venue profile with:
   - Venue name
   - Venue type (Club, Theater, Arena, etc.)
   - Description
   - Address
   - Capacity
   - Amenities
   - Business hours
6. **Dashboard Access**: After registration, you'll be redirected to the dashboard
7. **Profile Page**: Visit your profile at `http://localhost:8000/accounts/profile/`

#### 2.2 Event Creation & Management
1. **Access Events**: Navigate to "Events" section
2. **Create Event**: Fill in:
   - Title: "Jazz Night at Blue Note"
   - Event type: "Concert"
   - Description
   - Venue details (auto-filled from profile)
   - Event date and time
   - Expected attendance
   - Budget range (min/max)
   - Technical requirements
   - Equipment provided/needed
3. **Publish Event**: Set status to "Published"
4. **Manage Event**: Edit event details as needed

#### 2.2 Venue Booking Management
1. **View Booking Requests**: Check incoming artist requests
2. **Review Artist Profiles**: Click on artist names to view portfolios
3. **Respond to Requests**: Accept/decline with comments
4. **Manage Bookings**: Track confirmed bookings at `http://localhost:8000/bookings/bookings/`
5. **View Booking Details**: Click on any booking to see detailed information
6. **Contract Management**: Review and sign contracts

### 3. Manager User Flow

#### 3.1 Manager Registration & Onboarding
1. **Access**: Visit `http://localhost:8000/`
2. **Sign Up**: Click "Sign Up" → "Join as Manager"
3. **Registration Form**: Fill in:
   - Email: `manager@example.com`
   - Password: `testpass123`
   - User Type: `Manager`
4. **Email Verification**: Check console logs for verification link
5. **Profile Setup**: Complete manager profile with:
   - Company name
   - Bio
   - Specialization
   - Experience years
   - Commission rate
   - Contact information
6. **Dashboard Access**: After registration, you'll be redirected to the dashboard
7. **Profile Page**: Visit your profile at `http://localhost:8000/accounts/profile/`

#### 3.2 Manager Artist Management
1. **Browse Artists**: Visit `http://localhost:8000/artists/`
2. **View Artist Portfolios**: Click on artist profiles
3. **Contact Artists**: Use messaging system (when implemented)
4. **Manage Bookings**: Assist with booking requests
5. **Track Performance**: Monitor artist bookings at `http://localhost:8000/bookings/bookings/`
6. **View Booking Details**: Click on any booking to see detailed information

## Admin Interface Flow

### Admin Access
1. **URL**: `http://localhost:8000/admin/`
2. **Login**: Use existing superuser credentials
3. **JAZZMIN Features**:
   - Modern, responsive interface
   - Custom EncoreHub branding
   - Icon-based navigation
   - Search functionality
   - User management
   - Booking system administration

### Admin Management Tasks
1. **User Management**:
   - View all users (Artists, Venues, Managers)
   - Edit user profiles
   - Manage user permissions
2. **Content Management**:
   - Review artist portfolios
   - Monitor events
   - Manage booking requests
   - Track contracts
3. **System Administration**:
   - Database management
   - System settings
   - Log monitoring

## User Profile Flow

### Profile Access
1. **URL**: `http://localhost:8000/accounts/profile/`
2. **Features**:
   - Modern dashboard-inspired design
   - Role-specific profile information
   - Quick stats and metrics
   - Recent activity timeline
   - Quick action buttons
   - Responsive layout

### Profile Features
1. **Profile Header**:
   - User avatar and basic info
   - User type and location
   - Join date
   - Edit and share buttons
2. **Profile Information**:
   - Role-specific details (Artist/Venue/Manager)
   - Contact information
   - Professional details
3. **Recent Activity**:
   - Timeline of user actions
   - Welcome messages
   - System notifications
4. **Quick Stats**:
   - Role-specific metrics
   - Performance indicators
   - Activity counters
5. **Quick Actions**:
   - Role-specific action buttons
   - Navigation shortcuts
   - Common tasks
6. **Edit Profile**:
   - Comprehensive form for updating profile information
   - Role-specific fields and validation
   - Real-time form validation and error handling

## Testing Scenarios

### Scenario 1: Complete Booking Flow
1. **Setup**: Create one user of each type (Artist, Venue, Manager)
2. **Venue Action**: Create an event
3. **Artist Action**: Submit booking request
4. **Venue Action**: Review and accept request
5. **Manager Action**: Assist with contract (optional)
6. **Verification**: Check booking status in admin

### Scenario 2: Artist Portfolio Showcase
1. **Setup**: Create artist user
2. **Artist Action**: Complete portfolio with media
3. **Venue Action**: Browse artists and view portfolio
4. **Verification**: Check portfolio display and media uploads

### Scenario 3: Event Discovery
1. **Setup**: Create venue user and multiple events
2. **Artist Action**: Browse events with filters at `http://localhost:8000/bookings/events/`
3. **Public Access**: Anyone can view events without login
4. **Verification**: Test search and filtering functionality

## Current Limitations & Known Issues

### Missing Features (To Be Implemented)
1. **Payment Integration**: Stripe Connect for payments
2. **Messaging System**: Real-time communication
3. **Notifications**: Email/SMS notifications
4. **File Upload**: Media file handling
5. **Advanced Search**: Elasticsearch integration
6. **Analytics**: Booking analytics and reporting

### Current Technical Notes
1. **Email Backend**: Console-based (check logs for verification emails)
2. **File Storage**: Local storage (not production-ready)
3. **Background Tasks**: No Celery (simplified setup)
4. **Real-time Features**: WebSocket setup ready but not implemented

## Testing Commands

### Docker Commands
```bash
# Start application
make up

# View logs
make logs

# Access shell
make shell

# Run migrations
make migrate

# Create superuser
make superuser

# Stop application
make down
```

### Database Commands
```bash
# Access database shell
docker-compose exec db psql -U encorehub -d encorehub

# Reset database
make reset
```

## Next Steps for Development

### Priority 1: Payment Integration
1. Implement Stripe Connect
2. Add payment processing
3. Handle deposits and final payments
4. Payment dispute resolution

### Priority 2: Enhanced User Experience
1. File upload functionality
2. Real-time messaging
3. Email notifications
4. Mobile-responsive design

### Priority 3: Advanced Features
1. Analytics dashboard
2. Advanced search
3. Recommendation system
4. Social features

## Support & Troubleshooting

### Common Issues
1. **Docker Issues**: Use `make clean` then `make build`
2. **Database Issues**: Use `make reset` to start fresh
3. **Email Issues**: Check console logs for verification links
4. **Permission Issues**: Ensure proper file permissions

### Getting Help
- Check Docker logs: `docker-compose logs web`
- Check Django logs: `docker-compose exec web python manage.py check`
- Database issues: `docker-compose exec db psql -U encorehub -d encorehub`

---

**Last Updated**: September 1, 2025
**Version**: 1.0.0
**Status**: Core functionality implemented, ready for testing
