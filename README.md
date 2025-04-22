# SocialPulse Backend (Django)

## Overview
This is the backend for SocialPulse, built with Django. It manages authentication, Facebook integration, and APIs for posting content to Facebook Pages. The backend is designed to work seamlessly with a React frontend, supporting cross-origin requests and secure session handling.

## Features
- Facebook OAuth login (with page management permissions)
- Fetch user-managed Facebook pages
- Post text and images to selected Facebook pages
- Session-based authentication
- CSRF protection (where needed)
- CORS enabled for frontend integration

## Main Endpoints
| Endpoint                | Method | Description                                  |
|------------------------|--------|----------------------------------------------|
| `/facebook/login/`     | GET    | Start Facebook OAuth login                   |
| `/facebook/callback/`  | GET    | Facebook OAuth callback                      |
| `/facebook/profile/`   | GET    | Get Facebook user profile                    |
| `/facebook/pages/`     | GET    | Get list of managed Facebook pages           |
| `/facebook/post/`      | POST   | Post text/image to selected Facebook page    |
| `/facebook/disconnect/`| POST   | Disconnect/unlink Facebook account           |

## Facebook Integration
- Uses Facebook Graph API (v18.0)
- Permissions required: `email`, `pages_show_list`, `pages_manage_posts`, `pages_read_engagement`
- Stores Facebook access tokens in session
- Fetches and uses page-specific access tokens for posting

## Environment Variables
Set these in your `.env` file or environment:
- `FB_APP_ID`: Facebook App ID
- `FB_APP_SECRET`: Facebook App Secret
- `FB_REDIRECT_URI`: OAuth redirect URI (should match Facebook app settings)

## CORS & Security
- `CORS_ALLOW_CREDENTIALS = True`
- `CORS_ALLOWED_ORIGINS` includes all frontend origins (e.g. `http://localhost:5190`)
- Session cookies are used for authentication

## Dependencies
- Django
- django-cors-headers
- requests

## Running the Backend
```bash
# Activate your virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
./runserver.sh
```

## Notes
- Make sure your Facebook app is in development mode or approved for required permissions.
- The backend must be running on the same machine/network as the frontend for local development.
- For production, update allowed origins and secure cookie settings accordingly.
