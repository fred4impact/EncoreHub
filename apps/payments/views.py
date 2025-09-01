from django.shortcuts import render

# Create your views here.

def payment_list(request):
    """List all payments."""
    return render(request, 'payments/list.html')

def payment_detail(request, pk):
    """Show payment details."""
    return render(request, 'payments/detail.html')
