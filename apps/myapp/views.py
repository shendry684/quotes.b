from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
   
    return render(request, 'index.html')

def register(request):
    # print('inside register method in views')
    result = User.objects.reg_validator(request.POST)
    # print('back inside register in views')
    # print(result)
    if len(result) > 0:
        for key, value in result.items():
            # messages.error(request, value)
            messages.add_message(request, messages.ERROR, value)
        return redirect('/')
    else:  # passed validations
        # create the user (add to database)
        hash = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(
            name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], birthday=request.POST['birthday'], password=hash.decode())
        # print(user.id)
        # save their id in session
        request.session['userid'] = user.id
        # redirect to add page/dashboard
        return redirect('/dashboard')


def dashboard(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['userid'])
        quotes = user.favorites.all()
        unfavorites = []
        allquotes = Quote.objects.all()
        for i in allquotes:
            if i not in quotes:
                unfavorites.append(i)
        context = {
            'user': user,
            'quotes': quotes,
            'unfavorites': unfavorites

        }

        return render(request, 'dashboard.html', context)


def delete(request, id):
    m = Quote.objects.get(id=id)
    m.delete()
    return redirect('/dashboard')

def favorite(request, id):
    user = User.objects.get(id=request.session['userid'])
    quote = Quote.objects.get(id=id)
    user.favorites.add(quote)
    return redirect('/dashboard')


def unfavorite(request, id):
    user = User.objects.get(id=request.session['userid'])
    quote = Quote.objects.get(id=id)
    user.favorites.remove(quote)
    return redirect('/dashboard')


def showquote(request, id):
    quote = Quote.objects.get(id=id)
    context = {
        "quote": quote,
        "favorites": Quote.objects.get(id=id).favorites.all(),
       
        
    }
    return render(request, "show.html", context)


def addquote(request):
   
    return render(request, 'dashboard.html')

def processquote(request):
    result = Quote.objects.quote_validator(request.POST)
    print(result)
    if len(result) > 0:
        for key, value in result.items():
            # messages.error(request, value) alternate method to line below for errors
            messages.add_message(request, messages.ERROR, value)
        return redirect('/add')
    else:
        quote = Quote.objects.create(
            title=request.POST['title'], addedby_id=request.session['userid'])
        user = User.objects.get(id=request.session['userid'])
        user.favorites.add(quote)
        return redirect('/dashboard')

def login(request):
    result = User.objects.loginvalidator(request.POST)
    if len(result) > 0:
        for key, value in result.items():
            messages.add_message(request, messages.ERROR, value)
        return redirect('/')
    else:
        user = User.objects.get(name=request.POST['name'], email=request.POST['email'])
        request.session['userid'] = user.id
        return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')
