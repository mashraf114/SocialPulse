# socialpulse/utils/tiktok_tokens.py
import requests
from django.conf import settings
from django.core.cache import cache  # Using cache for token storage
import time
def get_access_token(request):
    """
    Retrieve valid access token - refreshes if expired
    Returns: access_token or None if refresh fails
    """
    # Try to get from session first
    access_token = request.session.get('tiktok_access_token')
    
    # If not in session, try cache (alternative storage)
    if not access_token:
        access_token = cache.get('tiktok_access_token')
    
    # Verify token is still valid (pseudo-check)
    if access_token and not is_token_expired(request):
        return access_token
    
    # If invalid, attempt refresh
    return refresh_tiktok_token(request)

def refresh_tiktok_token(request):
    """
    Refresh expired TikTok token
    Returns: new_access_token or None
    """
    refresh_token = request.session.get('tiktok_refresh_token') or cache.get('tiktok_refresh_token')
    
    if not refresh_token:
        return None
    
    response = requests.post(
        'https://open.tiktokapis.com/v2/oauth/token/',
        data={
            'client_key': settings.TIKTOK_CLIENT_KEY,
            'client_secret': settings.TIKTOK_CLIENT_SECRET,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        # Store tokens in both session and cache
        request.session['tiktok_access_token'] = data['access_token']
        request.session['tiktok_refresh_token'] = data.get('refresh_token', refresh_token)  # Keep old if no new one
        cache.set('tiktok_access_token', data['access_token'], timeout=data['expires_in'] - 60)
        return data['access_token']
    
    return None

def is_token_expired(request):
    """Check if token is expired (pseudo-implementation)"""
    # Option 1: If you stored expiration time
    expires_at = request.session.get('tiktok_expires_at')
    if expires_at and time.time() > expires_at:
        return True
    
    # Option 2: Simple heuristic (tokens typically expire in 24h)
    last_refresh = request.session.get('tiktok_last_refresh')
    if last_refresh and time.time() - last_refresh > 82800:  # 23 hours
        return True
    
    return False