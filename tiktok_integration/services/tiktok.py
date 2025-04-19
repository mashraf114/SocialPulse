import requests
import os
import json
from django.conf import settings

def upload_video_to_tiktok(video_path, access_token, caption=""):
    """Upload video to TikTok using the API"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Step 1: Initialize upload
    init_url = "https://open-api.tiktok.com/share/video/upload/"
    init_response = requests.post(init_url, headers=headers)
    
    if init_response.status_code != 200:
        return {"error": "Failed to initialize upload", "details": init_response.json()}
    
    upload_url = init_response.json().get('data', {}).get('upload_url')
    if not upload_url:
        return {"error": "No upload URL received"}
    
    # Step 2: Upload video
    with open(video_path, 'rb') as video_file:
        upload_headers = {"Content-Type": "video/mp4"}
        upload_response = requests.put(upload_url, headers=upload_headers, data=video_file)
    
    if upload_response.status_code != 200:
        return {"error": "Video upload failed", "details": upload_response.text}
    
    # Step 3: Publish video
    publish_url = "https://open-api.tiktok.com/share/video/publish/"
    publish_data = {
        "post_info": {
            "title": caption,
            "privacy_level": "PUBLIC",
            "disable_duet": False,
            "disable_stitch": False,
            "disable_comment": False
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": os.path.getsize(video_path)
        }
    }
    
    publish_response = requests.post(
        publish_url,
        headers=headers,
        json=publish_data
    )
    
    return publish_response.json()