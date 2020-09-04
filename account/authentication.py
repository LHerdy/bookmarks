from django.contrib.auth.models import User

# Autentica pelo e-mail
class EmailAuthBackend(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(email=username):
                return user
            return None:
        except User.DoesNotExsit:
            return None
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
        return None



