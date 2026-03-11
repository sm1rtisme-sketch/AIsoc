from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            return self.get_response(request)
        
        if request.path.startswith('/api/'):
            if not request.user.is_authenticated:
                if request.path not in ['/api/login', '/api/health']:
                    return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        return self.get_response(request)
