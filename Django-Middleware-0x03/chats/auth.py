from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication if we need to extend later
    (e.g., logging, blacklisting, etc.)
    """
    pass
