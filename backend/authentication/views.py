from django.http import JsonResponse
from allauth.account.models import EmailConfirmationHMAC


def info_from_confirm_key(request, key):
    info = EmailConfirmationHMAC.from_key(key)
    return JsonResponse({'username': info.email_address.user.username,
                         'email': info.email_address.email})
