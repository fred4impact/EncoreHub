# EncoreHub - Artist Booking Platform

A comprehensive Django-based platform for connecting artists with booking opportunities worldwide.

## 🎯 Project Overview

EncoreHub is a full-featured artist booking platform that streamlines the entire process from artist discovery to gig execution. The platform serves as a digital marketplace connecting artists, managers, and clients while providing powerful tools for booking management, payments, and logistics coordination.

## 🚀 Features

### Core Functionality
- **Artist Management**: Profile creation, portfolio management, availability tracking
- **Booking System**: Request workflow, contract management, event coordination
- **Payment Processing**: Stripe integration, commission handling, invoice generation
- **Real-time Communication**: WebSocket-based messaging, notifications
- **Logistics Management**: Travel arrangements, technical requirements, rider management
- **Analytics & Reporting**: Performance metrics, earnings reports, client insights

### Technical Features
- **Progressive Web App (PWA)**: Mobile-responsive with offline capabilities
- **Real-time Updates**: WebSocket connections for live chat and notifications
- **API-First Design**: RESTful API with Django REST Framework
- **Modern Frontend**: Bootstrap 5 + HTMX for dynamic interactions
- **Security**: JWT authentication, CSRF protection, secure file uploads

## 🛠️ Technology Stack

### Backend
- **Django 5.2+**: Web framework
- **Django REST Framework**: API development
- **Django Allauth**: Authentication system
- **PostgreSQL**: Primary database
- **Redis**: Caching and message broker
- **Celery**: Background task processing

### Frontend
- **Bootstrap 5**: UI framework
- **HTMX**: Dynamic interactions
- **JavaScript**: Custom functionality
- **CSS3**: Custom styling

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Local development
- **AWS S3**: File storage (production)
- **Stripe**: Payment processing
- **Twilio**: SMS notifications

## 📁 Project Structure

```
EncoreHub/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Docker services configuration
├── Dockerfile               # Docker image definition
├── Makefile                 # Development commands
├── .env                     # Environment variables (create this)
├── .gitignore              # Git ignore rules
├── encorehub/              # Main Django project
│   ├── __init__.py
│   ├── settings/           # Settings configuration
│   │   ├── __init__.py
│   │   ├── base.py        # Base settings
│   │   ├── development.py # Development settings
│   │   └── production.py  # Production settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   ├── asgi.py            # ASGI configuration
│   └── celery.py          # Celery configuration
├── apps/                   # Django applications
│   ├── __init__.py
│   ├── accounts/          # User management
│   ├── artists/           # Artist profiles & portfolios
│   ├── bookings/          # Booking workflow
│   ├── payments/          # Payment processing
│   ├── messaging/         # Real-time communication
│   ├── logistics/         # Travel & accommodation
│   └── analytics/         # Reports & insights
├── static/                # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── templates/             # HTML templates
├── media/                 # User-uploaded files
└── logs/                  # Application logs
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd EncoreHub
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Using Docker (Recommended)**
   ```bash
   # Build and start services
   make start
   
   # Or manually:
   docker-compose build
   docker-compose up -d
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Using Local Python**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run migrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   
   # Start development server
   python manage.py runserver
   ```

5. **Access the application**
   - Web application: http://localhost:8000
   - Admin interface: http://localhost:8000/admin
   - API documentation: http://localhost:8000/api/

## 🛠️ Development Commands

### Using Makefile
```bash
make help              # Show all available commands
make build             # Build Docker images
make up                # Start all services
make down              # Stop all services
make logs              # Show service logs
make shell             # Open Django shell
make migrate           # Run database migrations
make makemigrations    # Create new migrations
make test              # Run tests
make superuser         # Create Django superuser
make clean             # Clean up containers and volumes
```

### Using Docker Compose
```bash
docker-compose up -d           # Start services in background
docker-compose down            # Stop services
docker-compose logs -f         # Follow logs
docker-compose exec web bash   # Access web container
```

### Using Django Management
```bash
python manage.py runserver     # Start development server
python manage.py migrate       # Apply migrations
python manage.py makemigrations # Create migrations
python manage.py collectstatic # Collect static files
python manage.py test          # Run tests
python manage.py shell         # Open Django shell
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=encorehub
DB_USER=encorehub
DB_PASSWORD=encorehub
DB_HOST=localhost
DB_PORT=5432

# Redis Settings
REDIS_URL=redis://localhost:6379/0

# Email Settings
EMAIL_HOST=localhost
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Stripe Settings
STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

# Twilio Settings
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
```

## 📚 API Documentation

The API is built with Django REST Framework and provides endpoints for:

- **Authentication**: JWT-based authentication
- **Artists**: CRUD operations for artist profiles
- **Bookings**: Booking management and workflow
- **Payments**: Payment processing and tracking
- **Messaging**: Real-time communication
- **Analytics**: Reports and insights

### API Endpoints
- Base URL: `http://localhost:8000/api/`
- Authentication: `POST /api/token/`
- Artists: `GET /api/artists/`
- Bookings: `GET /api/bookings/`
- Payments: `GET /api/payments/`

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.accounts

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False` in production settings
2. Configure production database (PostgreSQL)
3. Set up Redis for caching and Celery
4. Configure AWS S3 for file storage
5. Set up SSL certificates
6. Configure email settings
7. Set up monitoring and logging

### Docker Production
```bash
# Build production image
docker build -t encorehub:production .

# Run with production settings
docker run -e DJANGO_SETTINGS_MODULE=encorehub.settings.production encorehub:production
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation

## 🔮 Roadmap

### Phase 1: Core Features ✅
- [x] User authentication and authorization
- [x] Artist profile management
- [x] Basic booking workflow
- [x] Payment integration
- [x] Real-time messaging

### Phase 2: Advanced Features 🚧
- [ ] Advanced analytics and reporting
- [ ] Mobile app development
- [ ] AI-powered recommendations
- [ ] Advanced search and filtering
- [ ] Multi-language support

### Phase 3: Enterprise Features 📋
- [ ] White-label solutions
- [ ] Advanced API integrations
- [ ] Enterprise reporting
- [ ] Custom workflows
- [ ] Advanced security features

---

**EncoreHub** - Connecting artists with opportunities worldwide! 🎵
