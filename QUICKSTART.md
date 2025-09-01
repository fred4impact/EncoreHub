# EncoreHub Quick Start Guide

This guide will help you get EncoreHub running locally in minutes.

## 🚀 Quick Setup (5 minutes)

### Option 1: Using Docker (Recommended)

1. **Start the application**
   ```bash
   make start
   ```

2. **Access the application**
   - Web app: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - Username: `admin`
   - Password: `admin123` (you'll be prompted to change this)

### Option 2: Using Local Python

1. **Install dependencies**
   ```bash
   python3 -m pip install -r requirements.txt
   ```

2. **Run migrations**
   ```bash
   python3 manage.py migrate
   ```

3. **Create superuser**
   ```bash
   python3 manage.py createsuperuser
   ```

4. **Start server**
   ```bash
   python3 manage.py runserver
   ```

5. **Access the application**
   - Web app: http://localhost:8000
   - Admin: http://localhost:8000/admin

## 🎯 What You Can Test

### 1. Home Page
- Visit http://localhost:8000
- See the landing page with artist booking information
- Test responsive design on different screen sizes

### 2. Admin Interface
- Visit http://localhost:8000/admin
- Login with your superuser credentials
- Explore Django's built-in admin interface

### 3. User Authentication
- Test user registration and login
- Email verification (configured for console output)

### 4. API Endpoints
- Base API: http://localhost:8000/api/
- Authentication: http://localhost:8000/api/token/
- Artists: http://localhost:8000/api/artists/
- Bookings: http://localhost:8000/api/bookings/

## 🛠️ Development Commands

```bash
# View all available commands
make help

# Start/stop services
make up
make down

# View logs
make logs

# Run migrations
make migrate

# Create superuser
make superuser

# Run tests
make test

# Clean up
make clean
```

## 🔧 Configuration

### Environment Variables
The application uses these default settings for development:
- Database: SQLite (local file)
- Debug: Enabled
- Email: Console output
- Static files: Local storage

### Custom Configuration
Create a `.env` file to override defaults:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process on port 8000
   lsof -ti:8000 | xargs kill -9
   ```

2. **Database issues**
   ```bash
   # Reset database
   make reset-db
   ```

3. **Docker issues**
   ```bash
   # Clean and rebuild
   make clean
   make build
   make start
   ```

4. **Permission issues**
   ```bash
   # Fix file permissions
   chmod +x manage.py
   ```

### Getting Help

- Check the logs: `make logs`
- Run Django shell: `make shell`
- Check Django status: `python manage.py check`

## 📱 Testing on Mobile

1. **Enable mobile testing**
   - Use browser dev tools to simulate mobile devices
   - Test responsive design on different screen sizes

2. **PWA features**
   - Install the app on mobile devices
   - Test offline functionality
   - Check push notifications

## 🔄 Next Steps

After getting the basic application running:

1. **Explore the codebase**
   - Check the `apps/` directory for different modules
   - Review `templates/` for frontend structure
   - Examine `static/` for CSS and JavaScript

2. **Add features**
   - Create new Django apps
   - Add models and views
   - Implement API endpoints

3. **Customize styling**
   - Modify `static/css/style.css`
   - Update Bootstrap components
   - Add custom JavaScript

4. **Deploy**
   - Set up production environment
   - Configure database and caching
   - Deploy to cloud platform

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/)
- [HTMX](https://htmx.org/docs/)

---

**Happy coding!** 🎵 