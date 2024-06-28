from django.utils.deprecation import MiddlewareMixin
import json

# decode the data of POST request
class Md1(MiddlewareMixin):
    # Request Middleware
    def process_request(self, request):
        if request.method != 'GET' and request.META.get('CONTENT_TYPE') == 'application/json':
            data = json.loads(request.body)  # encode the data into dictionary
            request.data = data

    # Response the middleware
    def process_response(self, request, response):
        return response