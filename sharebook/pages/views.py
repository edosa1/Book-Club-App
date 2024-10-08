from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount, Book
# Create your views here.


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    posts = Post.objects.all()
    return render(request, 'index.html', {'user_profile': user_profile, 'posts': posts})


@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def like_post(request):

    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_check = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_check == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_check.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')
    
@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    
    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts': user_posts,
        'user_post_length':user_post_length,
}
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST.get('follower')
        user = request.POST.get('user')

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/') 
        
@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)


    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image')!= None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']


            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
           if User.objects.filter(email=email).exists():
               messages.info(request, 'Email Token')
               return redirect('signup')
           elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
           else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

               
                #log user in and redirect to settings page
               
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)


                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
           
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):

    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
        
    else:
        return render(request, 'signin.html')
    
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
    





def books(request):
    query = request.GET.get('q')
    books = []
    if query:
        books = Book.objects.filter(bookTitle__icontains=query) | Book.objects.filter(bookAuthors__icontains=query)
    return render(request, 'books.html', {'books': books, 'query': query})


def book_details(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_details.html', {'book': book})

# just a test
def topbar(request):
    return render(request, 'topbar.html')

def chatroom(request):
    """
    View to display a form for entering a chat room name.
    """
    return render(request, 'chat/chatroom.html')

def room(request, room_name):
    """
    View to render the chat room page.
    """
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': request.user.username,
    })

def room_redirect(request):
    """
    View to handle form submission and redirect to the chat room.
    """
    if request.method == "POST":
        room_name = request.POST.get('room_name')
        if room_name:
            return redirect('room', room_name=room_name)
    return redirect('chatroom')