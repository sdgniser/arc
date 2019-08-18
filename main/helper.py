import random
import hashlib
from datetime import datetime

def genVID(email):
    salt = str(random.random()) + str(datetime.now())
    m = hashlib.sha3_256((salt + email).encode('utf-8')).hexdigest()
    return m[:10] + m[-10:]

def getIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
