from .helper import *
from django.utils import timezone

class LogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            ip_addr= getIP(request)
            log = str(timezone.now()) + '\t' + ip_addr + '\t' + request.user.email + '\n'
            f = open('/home/kss/log', 'a')
            f.write(log)
            f.close()
        return self.get_response(request)
