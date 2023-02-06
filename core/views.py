from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import profile,post, LikePost
# Create your views here.

# @login_required(login_url='signin')
def index(request):
    user_obejct = User.objects.get(username=request.user.username)
    user_profile = profile.objects.get(user= user_obejct)
    
    posts = post.objects.all()
    return render(request,'index.html',{'user_profile' : user_profile, 'posts': posts})
# @login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post = post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')
    return HttpResponse('<h1>upload view</h1>')
# @login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    Post = post.objects.get(id=post_id)
    
    like_filter = LikePost.objects.filter(post_id = post_id, username=username).first()
    
    if like_filter == None:
        new_like = LikePost.objects.create(post_id = post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')
        
def settings(request):
    user_profile = profile.objects.get(user=request.user)
    
    if request.method== 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('settings')    
            
    
    return render(request,'setting.html',{'user_profile': user_profile})
# @login_required(login_url='signin')

def signup(request):
    
    if request.method == 'POST':
        username = request.POST['usename']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password== password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user= User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
                user_login = auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                
                #create new profile obj for new usr
                user_model = User.objects.get(username=username)
                new_profile = profile.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request,'Password mismatch')
            return redirect('signup')
            
        
    else:
        
        return render(request,'signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credential Invalid')
            return redirect('signin')
        
       
    return render(request,'signin.html')
# @login_required(login_url='signin')

def logout(request):
    
    auth.logout(request)
    return redirect('signin')
