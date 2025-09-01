from django.shortcuts import render

# Create your views here.

def analytics_dashboard(request):
    """Analytics dashboard."""
    return render(request, 'analytics/dashboard.html')

def reports(request):
    """Analytics reports."""
    return render(request, 'analytics/reports.html')
