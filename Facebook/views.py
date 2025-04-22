import requests
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from .models import FacebookToken
from django.views.decorators.csrf import csrf_exempt

def facebook_login(request):
    scopes = "email,pages_show_list,pages_manage_posts,pages_read_engagement"
    auth_url = f"https://www.facebook.com/v12.0/dialog/oauth?client_id={settings.FB_APP_ID}&redirect_uri={settings.FB_REDIRECT_URI}&scope={scopes}"
    return redirect(auth_url)

from django.shortcuts import render

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

    facebook_token = FacebookToken.objects.create(
        user_id=profile_data['id'],
        access_token=access_token
    )
    request.session['facebook_access_token'] = access_token
    request.session['facebook_profile'] = profile_data

    return redirect('/facebook/success/')

def facebook_success(request):
    return render(request, 'facebook/success.html')


from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import requests

@csrf_exempt
@require_POST
def facebook_disconnect(request):
    access_token = request.session.get('facebook_access_token')
    request.session.pop('facebook_access_token', None)
    request.session.pop('facebook_profile', None)
    if access_token:
        from .models import FacebookToken
        FacebookToken.objects.filter(access_token=access_token).delete()
    return JsonResponse({'success': True})

@csrf_exempt
@require_POST
def facebook_post(request):
    access_token = request.session.get('facebook_access_token')
    if not access_token:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    text = request.POST.get('text', '')
    image = request.FILES.get('image')
    page_id = request.POST.get('page_id')
    if not page_id:
        return JsonResponse({'error': 'No page selected'}, status=400)
    
    pages_url = f'https://graph.facebook.com/v18.0/me/accounts?fields=id,access_token&access_token={access_token}'
    resp = requests.get(pages_url)
    if resp.status_code != 200:
        return JsonResponse({'error': 'Failed to get pages', 'details': resp.text}, status=400)
    pages = resp.json().get('data', [])
    page_token = None
    for pg in pages:
        if pg['id'] == page_id:
            page_token = pg['access_token']
            break
    if not page_token:
        return JsonResponse({'error': 'Could not get page access token'}, status=400)
    
    if image is None:
        url = f'https://graph.facebook.com/{page_id}/feed'
        params = {
            'message': text,
            'access_token': page_token
        }
        resp = requests.post(url, data=params)
        if resp.status_code == 200:
            return JsonResponse({'success': True, 'response': resp.json()})
        else:
            return JsonResponse({'success': False, 'error': resp.text}, status=400)
    
    else:
        url = f'https://graph.facebook.com/{page_id}/photos'
        files = {'source': image}
        data = {
            'caption': text,
            'access_token': page_token
        }
        resp = requests.post(url, files=files, data=data)
        if resp.status_code == 200:
            return JsonResponse({'success': True, 'response': resp.json()})
        else:
            return JsonResponse({'success': False, 'error': resp.text}, status=400)

@csrf_exempt
@require_GET
def facebook_pages(request):
    access_token = request.session.get('facebook_access_token')
    if not access_token:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    access_token = request.session.get('facebook_access_token')
    if not access_token:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    text = request.POST.get('text', '')
    image = request.FILES.get('image')
    page_id = request.POST.get('page_id')
    if not page_id:
        return JsonResponse({'error': 'No page selected'}, status=400)
    
    pages_url = f'https://graph.facebook.com/v18.0/me/accounts?fields=id,access_token&access_token={access_token}'
    resp = requests.get(pages_url)
    if resp.status_code != 200:
        return JsonResponse({'error': 'Failed to get pages', 'details': resp.text}, status=400)
    pages = resp.json().get('data', [])
    page_token = None
    for pg in pages:
        if pg['id'] == page_id:
            page_token = pg['access_token']
            break
    if not page_token:
        return JsonResponse({'error': 'Could not get page access token'}, status=400)
    
    if image is None:
        url = f'https://graph.facebook.com/{page_id}/feed'
        params = {
            'message': text,
            'access_token': page_token
        }
        resp = requests.post(url, data=params)
        if resp.status_code == 200:
            return JsonResponse({'success': True, 'response': resp.json()})
        else:
            return JsonResponse({'success': False, 'error': resp.text}, status=400)
    
    else:
        url = f'https://graph.facebook.com/{page_id}/photos'
        files = {'source': image}
        data = {
            'caption': text,
            'access_token': page_token
        }
        resp = requests.post(url, files=files, data=data)
        if resp.status_code == 200:
            return JsonResponse({'success': True, 'response': resp.json()})
        else:
            return JsonResponse({'success': False, 'error': resp.text}, status=400)

@csrf_exempt
@require_GET
def facebook_pages(request):
    access_token = request.session.get('facebook_access_token')
    if not access_token:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    pages_url = f'https://graph.facebook.com/v18.0/me/accounts?fields=id,name,picture,access_token&access_token={access_token}'
    resp = requests.get(pages_url)
    if resp.status_code == 200:
        data = resp.json()
        return JsonResponse({'success': True, 'pages': data.get('data', [])})
    else:
        return JsonResponse({'success': False, 'error': resp.text}, status=400)

def facebook_profile(request):
    print('=== facebook_profile DEBUG ===')
    print('SESSION:', dict(request.session.items()))
    access_token = request.session.get('facebook_access_token')
    print('access_token (from session):', access_token)
    if not access_token:
        access_token = request.GET.get('access_token')
        print('access_token (from GET):', access_token)
    if not access_token:
        print('NO ACCESS TOKEN FOUND')
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    try:
        from .models import FacebookToken
        token_obj = FacebookToken.objects.get(access_token=access_token)
    except FacebookToken.DoesNotExist:
        print('INVALID TOKEN')
        return JsonResponse({'error': 'Invalid token'}, status=401)
    profile_url = "https://graph.facebook.com/me?fields=id,name,email,picture"
    profile_params = {'access_token': access_token}
    profile_response = requests.get(profile_url, params=profile_params)
    profile_data = profile_response.json()
    print('profile_data:', profile_data)
    request.session['facebook_profile'] = profile_data
    print('=== END DEBUG ===')
    return JsonResponse({'name': profile_data.get('name'), 'id': profile_data.get('id'), 'picture': profile_data.get('picture', {}).get('data', {}).get('url', '')})
