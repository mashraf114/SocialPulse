from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Send the confirmation email to your Gmail inbox
        mail_subject = 'New User Registered'  # Subject of the email
        message = f'User {username} has registered with email {email}. Please verify the registration.'
        send_mail(mail_subject, message, 'your_email@gmail.com', ['your_email@gmail.com'])  # Send to your email

        return redirect('auth:email_verification_sent')  # Redirect to a success page after sending email

    return render(request, 'authapp/register.html')
