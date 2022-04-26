from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


def edit_view(request):
    token = str(RefreshToken.for_user(request.user).access_token)

    # redirect to edit page for react
    gid = request.GET.get('gid')
    return redirect(f'{settings.REACT_URL}?gid={gid}&server={settings.SERVER_URL}&token={token}')
