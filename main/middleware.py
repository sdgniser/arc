from .models import Log
from .helper import *

class LogMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            i = getIP(request)
            l = Log(user=request.user, ip=i)
            l.save()
        return self.get_response(request)

    '''
    #Why isn't this working :(
    def process_request(self, request):
        print('this is working')
        if request.user is not None:
            i = getIP(request)
            l = Log(user=request.user, ip=i)
            l.save()
        return None
    '''
