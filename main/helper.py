import random
import hashlib
from datetime import datetime

def genVID(email):
    n = hashlib.sha256((str(random.random()) + str(datetime.now())).encode('utf-8')).hexdigest()
    salt = n[:4]+ n[-4:]
    return hashlib.sha256((salt + email).encode('utf-8')).hexdigest()

def getIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
