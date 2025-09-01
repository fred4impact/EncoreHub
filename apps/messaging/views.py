from django.shortcuts import render

# Create your views here.

def message_list(request):
    """List all messages."""
    return render(request, 'messaging/list.html')

def message_detail(request, pk):
    """Show message details."""
    return render(request, 'messaging/detail.html')
