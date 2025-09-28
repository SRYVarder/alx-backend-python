import logging
import time

from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from collections import defaultdict
from datetime import datetime, timedelta

# Configure logger to write to requests.log
logger = logging.getLogger('requests')
logging.basicConfig(
    filename='requests.log',  # Relative to project root
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware to log user requests with timestamp, user, and path."""
    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Log request details and pass request to next middleware/view."""
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    """Middleware to restrict chat access outside 6 AM to 9 PM."""
    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Deny access if current time is outside 6 AM to 9 PM."""
        current_hour = datetime.now().hour
        if request.path.startswith('/api/messages/') and (current_hour < 6 or current_hour >= 21):
            return HttpResponseForbidden("Chat access restricted outside 6 AM to 9 PM.")
        response = self.get_response(request)
        return response
    
class OffensiveLanguageMiddleware(MiddlewareMixin):
    """Middleware to limit chat messages to 5 per minute per IP."""
    def __init__(self, get_response):
        """Initialize with get_response and message tracking."""
        self.get_response = get_response
        self.message_counts = defaultdict(list)  # {ip: [timestamps]}

    def __call__(self, request):
        """Limit POST requests to /api/messages/ to 5 per minute."""
        if request.method == 'POST' and request.path.startswith('/api/messages/'):
            client_ip = request.META.get('REMOTE_ADDR', 'unknown')
            current_time = time.time()
            minute_ago = current_time - 60  # 1-minute window

            # Clean old timestamps
            self.message_counts[client_ip] = [
                t for t in self.message_counts[client_ip] if t > minute_ago
            ]

            # Check message limit
            if len(self.message_counts[client_ip]) >= 5:
                return HttpResponseForbidden("Message limit exceeded: 5 messages per minute.")
            
            # Record new message timestamp
            self.message_counts[client_ip].append(current_time)
        
        response = self.get_response(request)
        return response
    
class RolePermissionMiddleware(MiddlewareMixin):
    """Middleware to restrict actions to admin or moderator roles."""
    def __init__(self, get_response):
        """Initialize with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Restrict POST, PUT, PATCH, DELETE to admins/moderators."""
        protected_methods = ['POST', 'PUT', 'PATCH', 'DELETE']
        if request.method in protected_methods and request.path.startswith('/api/messages/'):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")
            if request.user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Only admins or moderators can perform this action.")
        response = self.get_response(request)
        return response
