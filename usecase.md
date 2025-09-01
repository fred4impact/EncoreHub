# EncoreHub Use Cases & User Flows

## Overview
This document outlines detailed use cases and user flows for the three main user personas in the EncoreHub platform. Each use case demonstrates the complete journey from registration to successful booking/performance.

---

## Persona 1: Julie - Jazz Vocalist (Artist)

### Profile
- **Name**: Julie Anderson
- **Role**: Jazz Vocalist
- **Experience**: 8 years performing in jazz clubs and private events
- **Location**: New York City
- **Specialties**: Jazz standards, bossa nova, contemporary jazz
- **Instruments**: Voice, piano (basic)

### Use Case 1: Initial Platform Registration & Portfolio Setup

#### **Flow:**
1. **Discovery & Registration**
   - Julie discovers EncoreHub through a friend's recommendation
   - Visits homepage and clicks "Get Started" button
   - Selects "Artist" role during registration
   - Fills out registration form with personal details
   - **System Action**: Creates User account with `user_type = 'artist'`
   - **System Action**: Redirects to profile completion page

2. **Profile Completion**
   - Julie completes her ArtistProfile with:
     - Instagram: @juliejazz
     - Facebook: Julie Anderson Jazz
     - YouTube: Julie Anderson Music
   - **System Action**: Saves profile data and redirects to portfolio creation

3. **Portfolio Creation**
   - Julie clicks "My Portfolio" in navigation
   - **System Action**: Redirects to `/artists/portfolio/`
   - Julie fills out ArtistPortfolio form:
     - Headline: "Award-winning Jazz Vocalist"
     - Bio: "Julie brings warmth and sophistication to every performance..."
     - Genres: ["Jazz", "Bossa Nova", "Contemporary"]
     - Instruments: ["Voice", "Piano"]
     - Base Rate: $500
     - Pricing Notes: "Rates vary based on event type and duration"
   - **System Action**: Creates ArtistPortfolio record
   - **System Action**: Displays portfolio management page

4. **Media Upload**
   - Julie clicks "Add Media" to upload portfolio content
   - **System Action**: Redirects to `/artists/portfolio/media/add/`
   - Julie uploads:
     - Performance video from Blue Note Jazz Club
     - Audio recording of "The Girl from Ipanema"
     - Professional headshot
   - **System Action**: Creates PortfolioMedia records
   - **System Action**: Displays media in portfolio gallery

5. **Performance History**
   - Julie clicks "Add Performance" to showcase experience
   - **System Action**: Redirects to `/artists/portfolio/performance/add/`
   - Julie adds past performances:
     - Blue Note Jazz Club (2023)
     - Private Corporate Event - Goldman Sachs (2023)
     - Wedding Reception - Central Park (2023)
   - **System Action**: Creates Performance records
   - **System Action**: Displays performances in portfolio

6. **Availability Management**
   - Julie clicks "Manage Availability" to set her schedule
   - **System Action**: Redirects to `/artists/portfolio/availability/`
   - Julie sets availability for upcoming months:
     - December 15: Morning, Afternoon available
     - December 16: Evening available
     - December 20: Full day available
   - **System Action**: Creates Availability records
   - **System Action**: Updates availability calendar

### Use Case 2: Receiving & Responding to Booking Requests

#### **Flow:**
1. **Booking Request Notification**
   - Vortex Jazz Club submits booking request for Julie
   - **System Action**: Creates BookingRequest record with:
     - Event: "New Year's Eve Jazz Night"
     - Date: December 31, 2024
     - Time: 8:00 PM
     - Duration: 3 hours
     - Proposed Fee: $800
     - Message: "Looking for sophisticated jazz vocalist..."
   - **System Action**: Sends email notification to Julie
   - **System Action**: Updates Julie's dashboard with new request

2. **Reviewing Request**
   - Julie logs in and sees notification in dashboard
   - Julie clicks on booking request
   - **System Action**: Redirects to `/bookings/requests/<id>/`
   - Julie reviews event details, venue information, and proposed fee
   - **System Action**: Displays BookingRequest details page

3. **Responding to Request**
   - Julie clicks "Accept" or "Decline"
   - **System Action**: Updates BookingRequest status to 'accepted' or 'declined'
   - **System Action**: Sends notification to Vortex Jazz Club
   - **System Action**: If accepted, creates Booking record
   - **System Action**: Updates both parties' dashboards

### Use Case 3: Performance & Payment

#### **Flow:**
1. **Pre-Event Communication**
   - Julie and venue communicate through platform messaging
   - **System Action**: Stores messages in messaging system
   - **System Action**: Notifies both parties of new messages

2. **Performance Day**
   - Julie performs at Vortex Jazz Club
   - **System Action**: Updates booking status to 'completed'
   - **System Action**: Triggers payment processing

3. **Payment & Review**
   - Venue processes payment through platform
   - **System Action**: Creates payment record
   - **System Action**: Updates Julie's earnings dashboard
   - Venue leaves review for Julie
   - **System Action**: Creates ArtistReview record
   - **System Action**: Updates Julie's portfolio with new review

---

## Persona 2: James - Artist Manager

### Profile
- **Name**: James Rodriguez
- **Role**: Artist Manager
- **Experience**: 15 years managing musicians and bands
- **Location**: Los Angeles
- **Specialties**: Jazz, Rock, Pop artists
- **Client Base**: 12 active artists

### Use Case 1: Platform Registration & Artist Discovery

#### **Flow:**
1. **Registration**
   - James discovers EncoreHub while searching for new talent
   - Registers as "Manager" role
   - **System Action**: Creates User account with `user_type = 'manager'`
   - **System Action**: Redirects to manager dashboard

2. **Artist Discovery**
   - James clicks "Browse Artists" in navigation
   - **System Action**: Redirects to `/artists/`
   - James uses search filters:
     - Genre: Jazz
     - Location: New York
     - Price Range: $400-$600
   - **System Action**: Filters ArtistPortfolio records
   - **System Action**: Displays matching artists

3. **Artist Evaluation**
   - James clicks on Julie's profile
   - **System Action**: Redirects to `/artists/<id>/`
   - James reviews:
     - Portfolio media (videos, audio)
     - Performance history
     - Reviews and ratings
     - Availability calendar
   - **System Action**: Displays artist detail page

### Use Case 2: Direct Artist Booking

#### **Flow:**
1. **Initiating Booking**
   - James clicks "Book This Artist" on Julie's profile
   - **System Action**: Redirects to `/bookings/artists/<portfolio_pk>/book/`
   - James fills out DirectArtistBookingForm:
     - Event Name: "Corporate Holiday Party"
     - Event Date: December 20, 2024
     - Event Time: 7:00 PM
     - Event Type: Corporate
     - Venue Location: "Downtown LA Convention Center"
     - Duration: 2 hours
     - Budget: $1000-$1500
     - Audience Size: 200
     - Description: "Sophisticated jazz performance for corporate event..."
   - **System Action**: Creates BookingRequest record
   - **System Action**: Sends notification to Julie

2. **Booking Management**
   - James monitors booking status in dashboard
   - **System Action**: Updates dashboard with booking status
   - James communicates with Julie through platform
   - **System Action**: Stores messages in messaging system

3. **Event Coordination**
   - James coordinates logistics between Julie and venue
   - **System Action**: Facilitates communication through messaging
   - **System Action**: Updates booking details as needed

### Use Case 3: Managing Multiple Artists

#### **Flow:**
1. **Artist Portfolio Management**
   - James manages multiple artists on the platform
   - **System Action**: Displays all managed artists in dashboard
   - James reviews performance opportunities for each artist
   - **System Action**: Shows booking requests for each artist

2. **Bulk Booking**
   - James books multiple artists for a festival
   - **System Action**: Creates multiple BookingRequest records
   - **System Action**: Tracks all bookings in manager dashboard

---

## Persona 3: Vortex Jazz Club (Venue)

### Profile
- **Name**: Vortex Jazz Club
- **Role**: Venue
- **Type**: Jazz Club & Restaurant
- **Location**: New York City
- **Capacity**: 150 people
- **Events**: Live jazz performances, private events, corporate functions

### Use Case 1: Venue Registration & Event Creation

#### **Flow:**
1. **Registration**
   - Vortex Jazz Club manager discovers EncoreHub
   - Registers as "Venue" role
   - **System Action**: Creates User account with `user_type = 'venue'`
   - **System Action**: Redirects to venue dashboard

2. **Event Creation**
   - Venue clicks "Create Event" in navigation
   - **System Action**: Redirects to `/bookings/events/create/`
   - Venue fills out EventForm:
     - Title: "New Year's Eve Jazz Night"
     - Date: December 31, 2024
     - Time: 8:00 PM
     - Duration: 4 hours
     - Venue: "Vortex Jazz Club"
     - Address: "123 Jazz Street, NYC"
     - Capacity: 150
     - Budget: $800-$1200
     - Description: "Sophisticated jazz evening with dinner service..."
   - **System Action**: Creates Event record
   - **System Action**: Displays event in public event listings

### Use Case 2: Artist Discovery & Booking

#### **Flow:**
1. **Artist Search**
   - Venue clicks "Browse Artists" to find performers
   - **System Action**: Redirects to `/artists/`
   - Venue searches for:
     - Genre: Jazz
     - Price Range: $500-$1000
     - Availability: December 31
   - **System Action**: Filters artists based on criteria
   - **System Action**: Displays matching artists

2. **Artist Selection**
   - Venue clicks on Julie's profile
   - **System Action**: Redirects to `/artists/<id>/`
   - Venue reviews Julie's:
     - Portfolio media
     - Performance history
     - Reviews and ratings
     - Base rate and pricing
   - **System Action**: Displays artist detail page

3. **Direct Booking**
   - Venue clicks "Book This Artist"
   - **System Action**: Redirects to `/bookings/artists/<portfolio_pk>/book/`
   - Venue fills booking form with event details
   - **System Action**: Creates BookingRequest record
   - **System Action**: Sends notification to Julie

### Use Case 3: Event Management & Communication

#### **Flow:**
1. **Booking Management**
   - Venue monitors booking requests in dashboard
   - **System Action**: Shows all booking requests for venue
   - Venue communicates with artists through platform
   - **System Action**: Facilitates messaging between parties

2. **Event Execution**
   - Event day arrives
   - **System Action**: Updates booking status
   - Venue processes payment through platform
   - **System Action**: Creates payment record
   - **System Action**: Updates financial dashboard

3. **Post-Event**
   - Venue leaves review for Julie
   - **System Action**: Creates ArtistReview record
   - **System Action**: Updates Julie's portfolio
   - Venue books Julie for future events
   - **System Action**: Creates new BookingRequest records

---

## System Flow Summary

### **Registration Flow:**
1. User visits homepage → Clicks "Get Started"
2. Selects role (Artist/Manager/Venue) → Fills registration form
3. **System Action**: Creates User account with appropriate `user_type`
4. **System Action**: Redirects to role-specific onboarding

### **Artist Journey:**
1. Registration → Profile completion → Portfolio creation
2. Media upload → Performance history → Availability setting
3. Receives booking requests → Reviews → Accepts/Declines
4. Performs → Receives payment → Gets reviewed

### **Manager Journey:**
1. Registration → Artist discovery → Artist evaluation
2. Direct booking → Communication → Event coordination
3. Multiple artist management → Bulk booking → Performance monitoring

### **Venue Journey:**
1. Registration → Event creation → Artist discovery
2. Artist selection → Direct booking → Communication
3. Event execution → Payment processing → Review submission

### **Key System Actions:**
- **User Creation**: Creates User records with role-based profiles
- **Portfolio Management**: Handles artist portfolio CRUD operations
- **Booking System**: Manages booking requests, acceptances, and payments
- **Communication**: Facilitates messaging between all parties
- **Reviews**: Handles review submission and display
- **Notifications**: Sends email and dashboard notifications
- **Payment Processing**: Manages financial transactions
- **Search & Filter**: Provides discovery functionality for artists and events

---

## Technical Implementation Notes

### **Database Relationships:**
- User → ArtistProfile/VenueProfile/ManagerProfile (One-to-One)
- User → ArtistPortfolio (One-to-One for artists)
- ArtistPortfolio → PortfolioMedia (One-to-Many)
- ArtistPortfolio → Performance (One-to-Many)
- User → Availability (One-to-Many for artists)
- Event → BookingRequest (One-to-Many)
- User → BookingRequest (Many-to-Many through requester/artist fields)
- BookingRequest → Booking (One-to-One)
- User → ArtistReview (Many-to-Many through reviewer/artist fields)

### **URL Patterns:**
- `/accounts/` - Authentication and profiles
- `/artists/` - Artist discovery and portfolio management
- `/bookings/` - Event and booking management
- `/dashboard/` - Role-specific dashboards

### **Role-Based Access:**
- Artists: Portfolio management, availability, booking responses
- Managers: Artist discovery, direct booking, multi-artist management
- Venues: Event creation, artist discovery, booking management

This comprehensive use case document demonstrates the complete user journey for each persona and the system actions that support their interactions with the EncoreHub platform.
