from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse
from django.template.loader import render_to_string 
from .models import Blog, User, Email
from django.contrib.auth.models import User as U
import pymongo, json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.html import strip_tags
from .serializers import BlogSerializer

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "blog/home.html"

@login_required(redirect_field_name='next')
def blogs(request):
    '''
    View for fetching all blogs
    '''
    try:
        blogs = Blog.objects.all()
        print(blogs[0].get_read_time)
        serializer = BlogSerializer(blogs,many=True)
        return JsonResponse(serializer.data,safe=False)
    except Exception as e:
        raise Http404

@login_required
def get_blog(request, slug):
    '''
    View for fetching a single blog
    '''
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        raise Http404

    return JsonResponse({
        'blog': {
            'id' : blog.id,
            'title': blog.blog_title,
            'slug': blog.slug,
            'date': blog.blog_date_created,
            'author': blog.user.first_name,
            'image_url': blog.blog_image.url,
            'content' : blog.blog_content,
            'likes' : blog.blog_likes
        }
    })

@login_required
def users(request):
    '''
    View for fetching all users
    '''

    try:
        users = User.objects.all()
    except Exception as e:
        print(e)
        raise Http404

    user_list = []

    for user in users:
        user_list.append({
            'id': user.id,
            'name' : user.first_name + user.last_name,
            'email' : user.email,
        })
    
    return JsonResponse({
        'users': user_list,
    }, safe=False)

@login_required
def get_user(request, pk):
    '''
    View for fetching a single blog
    '''
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        raise Http404
    
    user_blog_list = []
    
    for blog in user.get_blogs.all():
        i=0
        comments = []

        for comment in blog.get_comments.all():
            comments.append({
                'date': comment.date,
                'comment': json.dumps(comment.body),
                'user' : comment.user.first_name
            })
        

        user_blog_list.append({
            f'{i}' : {
                'id' : blog.id,
                'title': blog.blog_title,
                'slug': blog.slug,
                'date': blog.blog_date_created,
                'author': blog.user.first_name,
                'image_url': blog.blog_image.url,
                'content' : blog.blog_content,
                'likes' : blog.blog_likes,
                'comments' : comments,
            }
        })
        i+=1

    return JsonResponse({
        'user': {
            'id': user.id,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
            'blogs' : user_blog_list,
        }
    })

# send a welcome mail to the specified address
# checking if user exist will be added later
# returns True if successful
def sendWelcomeMail(request):
    try:
        user_id = 3
        user = User.objects.get(id=user_id)
        user_email = user.email
        user_fname = user.first_name
        
        context = {'user': user_fname}
        htmlmsgbody = render_to_string('emails/registrationsuccess.html', context)
        plaintxtmsgbody = strip_tags(htmlmsgbody)

        emailtobesent = EmailMultiAlternatives(
            subject="Welcome to communityWeb",
            body=plaintxtmsgbody,
            from_email='',
            # reply_to='',
            to=[user_email]
        )

        emailtobesent.attach_alternative(htmlmsgbody, 'text/html')
        emailtobesent.send()
        return HttpResponse(htmlmsgbody)
    except User.DoesNotExist:
        return HttpResponse("User not found!")
    
    
