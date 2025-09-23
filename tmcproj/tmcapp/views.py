from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages ,auth
from django.contrib.auth.models import User
from .models import AllowCourse, Video, UserProgress
from django.views.decorators.http import require_POST

from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']
        
        # Check if the input is an email
        if '@' in username_or_email:
            # Try to get the user by email
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                user = None
        else:
            # Try to get the user by username
            user = auth.authenticate(username=username_or_email, password=password)
        
        if user is not None:
            # If the user is found, authenticate and log in
            user = auth.authenticate(username=user.username, password=password)
            auth.login(request, user)
            return redirect('index')
        else:
            # If no user is found, display an error message
            messages.info(request, 'Invalid credentials')
            return redirect('login')
        
    return render(request, 'login.html')



def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        u_name = request.POST.get('username')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm-password')

        if pass1 == pass2:
            if User.objects.filter(username=u_name).exists():
                messages.error(request, "Username taken.")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return redirect('register')
            else:
                user = User.objects.create_user(username=u_name, password=pass1, email=email)
                user.save()
                messages.success(request, 'Account created successfully. Please log in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

    return render(request, 'register.html')



def signout(request):
    auth.logout(request)
    return redirect('/')


def contact(request):
    return render(request, 'contact.html')



# def useradmin(request):
#     users = User.objects.all()
    
#     user_data = []
#     for user in users:
#         # Check if user has an AllowCourse object
#         allow_course = AllowCourse.objects.filter(user=user).first()
#         if allow_course:
#             user_data.append({'user': user, 'gmail': user.email, 'course_allowed': allow_course.course_allowed})
#         else:
#             user_data.append({'user': user, 'gmail': user.email, 'course_allowed': False})

#     return render(request, 'useradmin.html', {'user_data': user_data})


# def delete_user(request, user_id):
#     user = User.objects.get(id=user_id)
#     user.delete()
#     return redirect('useradmin')
    

# @login_required
# def toggle_course(request, user_id):
#     user = get_object_or_404(User, pk=user_id)
#     allow_course, created = AllowCourse.objects.get_or_create(user=user)
#     allow_course.course_allowed = not allow_course.course_allowed
#     allow_course.save()
#     return redirect('useradmin')


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProgress, Video


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProgress, Video

@receiver(post_save, sender=User)
def create_user_progress(sender, instance, created, **kwargs):
    if created:
        # Get the first two videos
        first_video = Video.objects.all().order_by('id').first()
        second_video = Video.objects.all().order_by('id')[1]
        
        # Create UserProgress instances for the first two videos
        UserProgress.objects.create(user=instance, video=first_video, is_unlocked=True, watched_previous=True)
        UserProgress.objects.create(user=instance, video=second_video, watched_previous=True)
        
        # Get all videos starting from the third video
        videos = Video.objects.all().order_by('id')[2:]
        
        # Create UserProgress instances for each video with is_unlocked=False, watched_previous=False
        for video in videos:
            UserProgress.objects.create(user=instance, video=video, is_unlocked=False, watched_previous=False)





@login_required
def start_learning(request):
    videos = Video.objects.all()

    user = request.user  
    user_progress = UserProgress.objects.filter(user=user)
    print(user_progress)

    return render(request, 'allvideos.html', {'videos': videos, 'user_progress':user_progress})


@login_required
def unlock_video(request, video_id):
    video = Video.objects.get(pk=video_id)
    user = request.user
    
    userprogress, created = UserProgress.objects.get_or_create(user=user, video=video)
    
    if not userprogress.is_unlocked:
        userprogress.is_unlocked = True
        userprogress.save()
    
    # Check if there's a next video
    next_video_id = video_id + 1
    try:
        next_video = Video.objects.get(pk=next_video_id)
        next_userprogress, created = UserProgress.objects.get_or_create(user=user, video=next_video)
        
        # Mark the next video as watched_previous
        if not next_userprogress.watched_previous:
            next_userprogress.watched_previous = True
            next_userprogress.save()
    except Video.DoesNotExist:
        pass  # No next video
    
    return redirect('start_learning')

def documents(request):
    return render(request, "documents.html")