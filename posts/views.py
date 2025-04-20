from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
import requests
from django.conf import settings

@api_view(['GET', 'POST'])
def posts_list_create(request):
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def facebook_post(request):
    user_token = request.data.get('user_access_token')
    if not user_token:
        return Response({'error': 'Access token is required'}, status=400)

    pages_url = f"https://graph.facebook.com/me/accounts?access_token={user_token}"
    pages_res = requests.get(pages_url).json()
    if 'data' not in pages_res or not pages_res['data']:
        return Response({'error': 'No pages found'}, status=400)

    page = pages_res['data'][0]
    page_access_token = page['access_token']
    page_id = page['id']

    message = request.data.get('message', 'Test post from Django')
    post_url = f"https://graph.facebook.com/{page_id}/feed"
    post_data = {
        'message': message,
        'access_token': page_access_token,
    }
    fb_post = requests.post(post_url, data=post_data).json()
    return Response(fb_post)
