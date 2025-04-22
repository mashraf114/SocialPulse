# 🔐 Authentication System – Email Confirmation Flow

This branch implements a secure, email-based user registration and activation flow using Django and Djoser. The system sends a real email to users for account activation after registration.

## ✅ Current Features

- Custom `CustomUser` model
- User registration via Djoser endpoint
- SMTP configuration using Gmail (with App Password)
- Activation link is emailed to the user
- Clickable activation confirms the user
- Fully compatible with frontend frameworks (like React)

### 📦 Technologies Used

- Django 5.2
- Djoser
- DRF (Django Rest Framework)
- Gmail SMTP
- SQLite

---

## ⚙️ How It Works

1. **User registers** at the `/auth/users/` endpoint.
2. **Activation link** is sent to their email inbox.
3. The user **clicks the link**, and their account is activated through a React frontend that calls the backend activation endpoint.
4. Backend endpoint used for activation:  
   `/auth/users/activation/` *(POST request with UID and token)*

---

## 🔐 Email Configuration (Gmail SMTP)

Set the following in your `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'email@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```
---
## 🚧 Planned Improvements
🔄 Remove Djoser to gain more control over logic and customization

📱 Add phone number verification (not supported directly by Djoser)

🔐 Use Firebase Authentication for:

Phone-based OTP

Better token management

🧠 Add Social Auth for:

✅ Google (Gmail)

✅ Facebook

✅ TikTok

✅ LinkedIn

✅ YouTube

## 🧪 Testing
All current features can be tested with:

POST /auth/users/ to register

POST /auth/users/activation/ with { "uid": "...", "token": "..." } to activate

Frontend (React) will handle the UI for these

## 📁 Branch
All this work is currently in the authenication branch.