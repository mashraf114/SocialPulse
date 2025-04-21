# utils/upload_video.py
from ..models import YouTubeCredential
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http


def upload_video(
    file_path,
    title,
    description,
    category_id,
    tags,
    privacy_status="private",
    user=None,
):
    """
    Upload a video to YouTube using saved credentials.

    Args:
        file_path: Path to video file
        title: Video title
        description: Video description
        category_id: YouTube category ID
        tags: List of tags
        privacy_status: Video privacy setting
        user: Django user whose credentials to use
    """

    if not user:
        raise ValueError("User required to access YouTube credentials")

    # Get credentials from database
    try:
        credential = YouTubeCredential.objects.get(user=user)
        credentials = credential.get_credentials()
    except YouTubeCredential.DoesNotExist:
        raise ValueError(
            "No YouTube credentials found for this user. Please authenticate first."
        )

    # Build YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    # Prepare request
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id,
        },
        "status": {"privacyStatus": privacy_status},
    }

    media_file = googleapiclient.http.MediaFileUpload(file_path, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status", body=request_body, media_body=media_file
    )

    # Execute upload
    print(f"Uploading {file_path} to YouTube...")
    response = None
    try:
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")

        print(f"Upload Complete! Video ID: {response['id']}")
        return response

    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return None
