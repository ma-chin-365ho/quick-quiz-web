import string
import secrets

class AppUtilException(Exception):  
    pass

def gen_password(size):
   chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
   return ''.join(secrets.choice(chars) for x in range(size))