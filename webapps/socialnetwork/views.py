from django.shortcuts import render,redirect,get_object_or_404,render_to_response
from django.http import HttpResponse, Http404        
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.decorators import login_required 
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core import serializers
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from operator import attrgetter

from .models import Posts,UserProfile,Comment
from .forms import LoginForm,RegistrationForm,PostForm,EditProForm,EditUserForm

def user_login(request):   
    context = {}

    if request.method == 'POST':            
        form = LoginForm(request.POST)            
        if form.is_valid():                
            cd = form.cleaned_data
            username=cd['username']
            password=cd['password']
            user = authenticate(username=username,password = password)                
            if user is not None and user.is_active:                                         
                login(request, user)                        
                return redirect('/homepage')
            else: 
                context['errors'] = "Invalid username or password!"             
                return render(request, 'login.html',{'form' : form})
        else:
            context['errors'] = "Invalid username or password!"
            context['form'] = form
            return render(request, 'login.html', context)  
    else:            
        form = LoginForm()        
    return render(request, 'login.html', {'form': form})


@transaction.atomic
def user_register(request):
    context = {}
 
    if request.method == 'GET':
    	form = RegistrationForm()
        return render(request, 'register.html', {'form' : form})

    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        # context['errors'] = form.errors
    	return render(request, 'register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'])
    
    profile = UserProfile.objects.create(user=new_user,userage = form.cleaned_data['userage'], ip_addr = request.META['REMOTE_ADDR'])
    new_user.is_active = False
    new_user.save()

    token = default_token_generator.make_token(new_user)

    email_body = """
Welcome to this Social App.  Please click the link below to
verify your email address and complete the registration of your account:
  http://%s%s
""" % (request.get_host(), 
       reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="lem1@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'emailcomfirmation.html', context)

    # profile = UserProfile.objects.create(user=new_user, ip_addr = request.META['REMOTE_ADDR'])
    # context['message'] = 'profile #{0} saved.'.format(profile.id)
    # new_user = authenticate(username=form.cleaned_data['username'],
    #                         password=form.cleaned_data['password1'])
    # login(request, new_user)
    # return redirect('/homepage/')

def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'confirmed.html', {})

@login_required
@ensure_csrf_cookie
def go_home(request):
    all_posts = Posts.objects.all().order_by('-post_time')
    return render(request,'homepage.html', {'Posts' : all_posts})

@login_required
def view_profile(request,pk):
    context = {}
    # auser = User.objects.get(username = pk)
    auser = get_object_or_404(User, username=pk)

    all_posts = Posts.objects.filter(user = auser).order_by('-post_time')
    context['Posts'] = all_posts
    context['username'] = pk
    return render(request, 'profile.html', context)

def view_yourprofile(request):
    context = {}
    user = request.user
    all_posts =Posts.objects.filter(user = request.user).order_by('-post_time')
    yourprofile = UserProfile.objects.get(user = request.user)
    friends = user.userprofile.friends.all()
    userage = user.userprofile.userage;
    context['yourprofile'] = yourprofile
    context['all_posts'] = all_posts
    context['friends'] = friends
    context['userage'] = userage

    return render(request, 'viewyourprofile.html', context)

def getphoto(request,id):
    profile = get_object_or_404(UserProfile, id = id)
    if not profile.picture:
        raise Http404
    return HttpResponse(profile.picture, content_type=profile.content_type)

def index(request):
    return render(request,'index.html')

def logout(request):
    auth.logout(request)
    return render(request, 'logout.html')

@login_required
def post_message(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.post_time = timezone.now()
            post.save()
            return redirect('/homepage')
    else:
        form = PostForm()
    return render(request, 'postpage.html', {'form': form})

		
@login_required
def follow_user(request,id):
    context = {} 

    friend =get_object_or_404(User,id = id)
    user = request.user

    user.userprofile.friends.add(friend)
    friends = user.userprofile.friends.all()

    context['friends'] = friends
    posts = []
    for friend in friends:
        post = Posts.objects.filter(user = friend)  #.order_by('-post_time')
        for postt in post:
            posts.append(postt)
    posts = sorted(posts, key=attrgetter('post_time'), reverse=True)
    print(posts)
    context['posts'] = posts
    context['following_status'] = True
    context['followed_userid'] = id
    return render (request, 'friendlist.html', context)


@login_required
def unfollow(request,id):
    context = {}

    friend =get_object_or_404(User,id = id)
    user = request.user
    user.userprofile.friends.remove(friend)

    friends = user.userprofile.friends.all()
    context['friends'] = friends
    posts = []
    for friend in friends:
    	post = Posts.objects.filter(user = friend).order_by('-post_time')
    	for postt in post:
            posts.append(postt)
    context['posts'] = posts
    context['following_status'] = False
    return render (request, 'friendlist.html', context)


@login_required
@transaction.atomic
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user = request.user)
    if request.method == 'POST':
        user_form = EditUserForm(instance=request.user,
                                 data=request.POST)
        profile_form = EditProForm(data=request.POST,
                                   files=request.FILES,
                                   instance = profile)
        if user_form.is_valid() and profile_form.is_valid():
            profile.picture = profile_form.cleaned_data['picture']
            profile.content_type = profile_form.cleaned_data['picture'].content_type
            
            user_form.save()
            profile_form.save()
            return redirect('/viewyourprofile')
        else:
            return render(request, 'editprofile.html', {'user_form' : user_form,'profile_form': profile_form} )
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProForm(instance = request.user.userprofile)
        return render(request,'editprofile.html', {'user_form' : user_form,'profile_form': profile_form})



def add_comment(request):
    errors = []

    if not 'comment' in request.POST or not request.POST['comment']:
        message = 'You must enter a comment to add.'
        json_error = '{ "error": "'+message+'" }'
        return HttpResponse(json_error, content_type='application/json')

    new_comment = Comment(comment_content=request.POST['comment'],comment_user = request.user,
                          comment_post = Posts.objects.get(id = request.POST['postid']))
    new_comment.save()
    comments = Comment.objects.filter(comment_post = Posts.objects.get(id = request.POST['postid']))
    response_text = serializers.serialize('json', comments)
    return HttpResponse(response_text, content_type='application/json')


def get_list_json(request):
    print(request)
    response_text = serializers.serialize('json', Comment.objects.all())
    return HttpResponse(response_text, content_type='application/json')


def get_list_xml(request):
    response_text = serializers.serialize('xml', Comment.objects.all())
    return HttpResponse(response_text, content_type='application/xml')


def get_list_xml_template(request):
    context = { 'Comments': Comment.objects.all() }
    return render(request, 'comments.xml', context, content_type='application/xml')
























