import requests

def post_to_tiktok(access_token, video_path, caption):
    upload_url = 'https://open-api.tiktok.com/share/video/upload/'  # Example

    files = {'video': open(video_path, 'rb')}
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.post(upload_url, headers=headers, files=files, data={'caption': caption})
    return response.json()
