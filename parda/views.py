from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# Create your views here.

def health(request):
    """Simple health check endpoint for readiness/liveness probes."""
    return HttpResponse('ok')

def health_json(request):
    return JsonResponse({'status': 'ok'})
