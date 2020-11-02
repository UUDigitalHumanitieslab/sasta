from allauth.account.models import EmailConfirmationHMAC
from django.http import HttpResponseRedirect, JsonResponse


def info_from_confirm_key(request, key):
    info = EmailConfirmationHMAC.from_key(key)
    return JsonResponse({'username': info.email_address.user.username,
                         'email': info.email_address.email})


def redirect_confirm(request, key):
    return HttpResponseRedirect('/confirm-email/{}/'.format(key))
