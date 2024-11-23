import datetime

class RequestLoggingMiddleware:
    """
    Middleware to log details of incoming requests and add custom data to the request object.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request details
        # print(f"satyam singh inside middleware code is running [{datetime.datetime.now()}] {request.method} {request.path}")
        
        # Add custom data to the request object
        request.custom_data = "This is custom data added by the middleware"
        
        # Proceed to the next middleware or view
        response = self.get_response(request)
        
       
        return response
