# views.py (add these new views)
from django.urls import reverse
import google_auth_oauthlib.flow
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import VideoSerializer
from django.conf import settings
from django.core.files.storage import default_storage
from .utils.uplaod_video import upload_video
from .models import YouTubeCredential
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
User = get_user_model()


# views.py
class YouTubeUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            video_file = serializer.validated_data["video"]
            file_name = video_file.name
            save_path = os.path.join("videos", file_name)
            path = default_storage.save(save_path, video_file)
            full_path = os.path.join(settings.MEDIA_ROOT, path)
            try:
                # TODO: Change later to request.user
                response = upload_video(
                    full_path,
                    serializer.validated_data["title"],
                    serializer.validated_data["description"],
                    "22",
                    ["WOW"],
                    serializer.validated_data["privacy"],
                    request.user,
                )

                return Response(response)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


CLIENT_SECRETS_FILE = settings.GOOGLE_SECRETS_DIR / "client_secrets.json"


class YouTubeAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Disable OAuthlib's HTTPS verification when running locally
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=["https://www.googleapis.com/auth/youtube.upload"],
            redirect_uri=request.build_absolute_uri(reverse("youtube_callback")),
        )

        authorization_url, state = flow.authorization_url(
            access_type="offline", include_granted_scopes="true"
        )

        request.session["youtube_auth_state"] = state

        return Response({"authorization_url": authorization_url, "state": state})


class YouTubeCallbackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        state = request.session.get("youtube_auth_state")
        state = "iwkL59BwNOVZyCLrOx2nYWDoah1Maw"
        if not state:
            return Response(
                {"error": "No state found in session"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=["https://www.googleapis.com/auth/youtube.upload"],
            state=state,
            redirect_uri=request.build_absolute_uri(reverse("youtube_callback")),
        )

        flow.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = flow.credentials

        print( request.user)

        # TODO: Change later to request.user
        YouTubeCredential.save_credentials(request.user, credentials)

        return Response(status=status.HTTP_204_NO_CONTENT)
