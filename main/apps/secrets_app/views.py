from django.shortcuts import render, redirect
from models import Users, Secrets, Likes
from django.db.models import Count
from django.contrib import messages
import bcrypt
import re 

# Create your views here.

def index(request):
    return render(request, 'secrets_app/index.html')

def register(request):

    user = Users.usersManager.add(request.POST['first_name'], request.POST['last_name'], request.POST['email'],request.POST['password'], request.POST['confirm'])
    print user 

    if user[0] == False:
        for message in user[1]: 
            messages.add_message(request, messages.ERROR, message)
        return redirect('/')
    ## make sure this is indented this way so multiple error messages will display 
    else: 
        request.session['user_id'] = user[1].id
        print "Successful Registration"
        return redirect('/success/' + str(user[1].id))

def login(request):

    user = Users.usersManager.log(request.POST['email'],request.POST['password'])

    if user[0] == False:
        for message in user[1]:
            messages.add_message(request, messages.ERROR, message)
        return redirect('/')
        ## make sure this is indented this way so multiple error messages will display 
    
    else:
        request.session['user_id'] = user[1].id
        return redirect('/success/' + str(user[1].id))


def success(request, id):
    if 'user_id' not in request.session:
        return redirect("/")

    else: 
        secrets = Secrets.objects.all()
        liked_secrets = []

        for secret in secrets:
            if secret.likes.all().filter(user_id=request.session['user_id']).count()>0:
                user_likes = True
            else:
                user_likes = False 
            liked_secrets.append([secret,user_likes])

        context = {
            "secrets" : Secrets.objects.all().order_by("-created_at")[:5],
            "user" : Users.usersManager.get(id=id),
            "liked_secrets": liked_secrets
        }
        

        if str(request.session['user_id']) == id:
            return render(request, "secrets_app/success.html", context)
        else:
            return redirect("/")

def post(request):
    content = request.POST['content']
    user_id = request.session['user_id']
    Secrets.objects.create(content=content, creator_id = user_id)
    print "posted a secret"
    return redirect('/success/'+ str(user_id))

def delete(request, secret_id):
    secret = Secrets.objects.filter(id=secret_id)
    secret.delete()
    print secret
    return redirect('/success/' + str(request.session['user_id']))

def like(request, secret_id):

    likes = Likes.objects.filter(user_id = request.session['user_id']).filter(secret_id=secret_id)

    if len(likes) == 0:

        secret = Secrets.objects.get(id=secret_id)
        user = Users.usersManager.get(id=request.session['user_id'])
        Likes.objects.create(secret=secret,user=user)
        print "secret was liked"
        return redirect('/success/' + str(request.session['user_id'])) 
    else:
        return redirect('/success/' + str(request.session['user_id']))

def popular(request):

    context = {
            "secrets" : Secrets.objects.annotate(num_likes=Count('likes')).order_by('-num_likes'),
            "user" : Users.usersManager.get(id=request.session['user_id']),
            "type": 'popular'
        }
    return render(request, 'secrets_app/popular.html', context)


def back(request):
    return redirect('/success/' + str(request.session['user_id']))

def deletepop(request, secret_id):
    secret = Secrets.objects.filter(id=secret_id)
    secret.delete()
    print "popular secret deleted"
    return redirect('/popular')

def likepop(request, secret_id):
    secret = Secrets.objects.get(id=secret_id)
    user = Users.usersManager.get(id=request.session['user_id'])
    Likes.objects.create(secret=secret,user=user)
    print "popular secret was liked"
    return redirect('/popular')


def logout(request):
    request.session.clear()
    return redirect('/')

    

