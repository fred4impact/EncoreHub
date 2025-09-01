from django.shortcuts import render

# Create your views here.

def logistics_list(request):
    """List all logistics."""
    return render(request, 'logistics/list.html')

def logistics_detail(request, pk):
    """Show logistics details."""
    return render(request, 'logistics/detail.html')
