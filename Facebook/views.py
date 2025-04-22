import requests
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from .models import FacebookToken

def facebook_login(request):
    auth_url = f"https://www.facebook.com/v12.0/dialog/oauth?client_id={settings.FB_APP_ID}&redirect_uri={settings.FB_REDIRECT_URI}&scope=email,pages_show_list"
    return redirect(auth_url)

def facebook_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'No code provided'}, status=400)

    token_url = "https://graph.facebook.com/v12.0/oauth/access_token"
    token_params = {
        'client_id': settings.FB_APP_ID,
        'redirect_uri': settings.FB_REDIRECT_URI,
        'client_secret': settings.FB_APP_SECRET,
        'code': code
    }

    token_response = requests.get(token_url, params=token_params)
    access_token = token_response.json().get('access_token')

    if not access_token:
        return JsonResponse({'error': 'Failed to obtain access token'}, status=400)

    profile_url = "https://graph.facebook.com/me?fields=id,name,email,picture"
    profile_params = {
        'access_token': access_token
    }

    profile_response = requests.get(profile_url, params=profile_params)
    profile_data = profile_response.json()

    # حفظ الـ token في قاعدة البيانات
    facebook_token = FacebookToken.objects.create(
        user_id=profile_data['id'],
        access_token=access_token
    )

    return JsonResponse({
        'profile': profile_data,
        'access_token': access_token
    })
