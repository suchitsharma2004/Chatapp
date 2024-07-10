# from django.shortcuts import render

# # Create your views here.
# # views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages 
from .models import Message, Draft, User
import requests
from django.middleware.csrf import get_token
from django.http import JsonResponse

def get_csrf_token(request):
    if request.method == 'GET':
        csrf_token = get_token(request)
        return JsonResponse({'csrftoken': csrf_token})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inbox')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def inbox(request):
    user = request.user
    received_messages = Message.objects.filter(recipient=user)
    return render(request, 'inbox.html', {'messages': received_messages})

# @login_required
# def compose(request):
#     if request.method == 'POST':
#         recipient_username = request.POST.get('recipient')
#         subject = request.POST.get('subject')
#         body = request.POST.get('body')
#         action = request.POST.get('action')
        
#         if action == 'Send':
#             try:
#                 recipient = User.objects.get(username=recipient_username)
#                 Message.objects.create(
#                     sender=request.user,
#                     recipient=recipient,
#                     subject=subject,
#                     body=body
#                 )
#             except User.DoesNotExist:
#                 messages.error(request, f"User '{recipient_username}' does not exist.")
        
#         elif action == 'Save as Draft':
#             Draft.objects.create(
#                 user=request.user,
#                 subject=subject,
#                 body=body
#             )
        
#         return redirect('inbox')  # Redirect to inbox after sending or saving draft

#     return render(request, 'compose.html')
# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message, Draft
# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message, Draft
from django.contrib.auth.models import User
from django.http import JsonResponse

@login_required
def compose(request):
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        action = request.POST.get('action')
        
        if action == 'Send':
            # Check if recipient exists
            try:
                recipient = User.objects.get(username=recipient_username)
                Message.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    subject=subject,
                    body=body
                )
                return redirect('inbox')  # Redirect to inbox after sending message
            except User.DoesNotExist:
                messages.error(request, f"User '{recipient_username}' does not exist.")
        
        elif action == 'Save as Draft':
            Draft.objects.create(
                user=request.user,
                subject=subject,
                body=body
            )
            return redirect('inbox')  # Redirect to inbox after saving draft
    
    return render(request, 'compose.html')


@login_required
def drafts(request):
    user = request.user
    user_drafts = Draft.objects.filter(user=user)
    return render(request, 'drafts.html', {'drafts': user_drafts})

@login_required
def sent(request):
    user = request.user
    sent_messages = Message.objects.filter(sender=user)
    return render(request, 'sent.html', {'messages': sent_messages})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# views.py

from django.shortcuts import get_object_or_404

def get_user(request, username):
    try:
        user = get_object_or_404(User, username=username)
        return JsonResponse({'exists': True, 'user_id': user.id})
    except User.DoesNotExist:
        return JsonResponse({'exists': False}, status=404)
