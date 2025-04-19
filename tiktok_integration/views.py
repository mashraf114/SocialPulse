from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
import os
import tempfile
from urllib.parse import urlencode
from .utils.tiktok_tokens import get_access_token


# Environment variables - NEVER HARDCODE CREDENTIALS!
CLIENT_KEY = os.getenv('aw8uojlhlr4lsboi')  # Changed from your hardcoded value
CLIENT_SECRET = os.getenv('agX5vLcBAluZNHN7XhisCcywAI3ehQEA')  # Changed from your hardcoded value
REDIRECT_URI = os.getenv('TIKTOK_REDIRECT_URI', 'http://localhost:8000/tiktok/callback/')

def auth_view(request):
    """Return TikTok auth URL for frontend"""
    auth_url = "https://www.tiktok.com/v2/auth/authorize/"
    params = {
        'client_key': CLIENT_KEY,
        'scope': 'video.upload',
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'state': 'your_state_parameter'
    }
    return JsonResponse({
        'auth_url': f"{auth_url}?{urlencode(params)}"
    })

@csrf_exempt
def callback_view(request):
    """Handle TikTok callback and exchange code for token"""
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    if error:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}?error={error}")
    
    if not code:
        return JsonResponse({'error': 'Missing authorization code'}, status=400)
    
    # Exchange code for access token
    token_url = "https://open.tiktokapis.com/v2/oauth/token/"
    data = {
        'client_key': CLIENT_KEY,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }
    
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        response_data = response.json()
        
        # Store tokens securely (consider using Django's database instead of session)
        request.session['tiktok_access_token'] = response_data.get('access_token')
        request.session['tiktok_refresh_token'] = response_data.get('refresh_token')
        
        return HttpResponseRedirect(
            f"{settings.FRONTEND_URL}/tiktok-success?success=true"
        )
        
    except requests.exceptions.RequestException as e:
        return HttpResponseRedirect(
            f"{settings.FRONTEND_URL}?error=token_exchange_failed"
        )
    
    # request.session['tiktok_access_token'] = response_data.get('access_token')
    # print("Token stored:", request.session['tiktok_access_token']) 

@csrf_exempt
def upload_video_view(request):
    """Handle video uploads to TikTok"""
        # Get valid access token (auto-refreshes if needed)
    access_token = get_access_token(request)
    if not access_token:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    # Rest of your upload logic...
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    if 'tiktok_access_token' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if 'video' not in request.FILES:
        return JsonResponse({'error': 'No video file provided'}, status=400)
    
    # Create temporary file securely
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            for chunk in request.FILES['video'].chunks():
                tmp_file.write(chunk)
            tmp_path = tmp_file.name
        
        # TikTok API endpoints
        init_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
        headers = {
            "Authorization": f"Bearer {request.session['tiktok_access_token']}",
            "Content-Type": "application/json"
        }
        
        # Step 1: Initialize upload
        init_response = requests.post(init_url, headers=headers)
        if init_response.status_code != 200:
            raise Exception('Failed to initialize upload')
        
        upload_url = init_response.json().get('data', {}).get('upload_url')
        if not upload_url:
            raise Exception('No upload URL received')
        
        # Step 2: Upload video
        with open(tmp_path, 'rb') as video_file:
            upload_response = requests.put(
                upload_url,
                headers={"Content-Type": "video/mp4"},
                data=video_file
            )
            if upload_response.status_code != 200:
                raise Exception('Video upload failed')
        
        # Step 3: Publish video
        publish_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/publish/"
        publish_data = {
            "post_info": {
                "title": request.POST.get('caption', ''),
                "privacy_level": "PUBLIC",  # or "PRIVATE"
                "disable_duet": False,
                "disable_stitch": False,
                "disable_comment": False
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": os.path.getsize(tmp_path),
                "chunk_size": os.path.getsize(tmp_path),
                "total_chunk_count": 1
            }
        }
        
        publish_response = requests.post(
            publish_url,
            headers=headers,
            json=publish_data
        )
        
        return JsonResponse(publish_response.json())
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        
    finally:
        # Clean up temp file
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)