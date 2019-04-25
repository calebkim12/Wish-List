from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request, 'myapp/index.html')

def register(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password= hash)
        
        request.session['id'] = user.id
        return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(username=request.POST['username'])
        request.session['id'] = user.id
        return redirect('/dashboard')

def dashboard(request):
    if 'id' not in request.session:
        messages.error(request, 'Please log in to enter')
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['id'])
        allitems = Item.objects.all()
        myitems = user.items.all()
        otheritems = allitems.difference(myitems)
        context = {
            'user': user,
            'myitems': myitems,
            'otheritems': otheritems,
        }
        return render(request, 'myApp/dashboard.html', context)
        
def make_item(request):
    return render(request, 'myapp/create.html')

def create(request):
    user = User.objects.get(id=request.session['id'])
    errors = Item.objects.item_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/make_item')
    else:
        item = Item.objects.create(item=request.POST['item'], creator=user)
        user.items.add(item)
    return redirect('/dashboard')

def destroy(request, item_id):
    item = Item.objects.get(id = item_id)
    item.delete()
    return redirect('/dashboard')

def remove(request, item_id):
    user = User.objects.get(id = request.session['id'])
    item = Item.objects.get(id = item_id)
    user.items.remove(item)
    return redirect('/dashboard')

def add_item(request, item_id):
    user = User.objects.get(id=request.session['id'])
    item = Item.objects.get(id=item_id)
    user.items.add(item)
    return redirect('/dashboard')

def show(request, item_id):
    item = Item.objects.get(id=item_id)
    user = User.objects.get(id=item.creator.id)
    others = item.users.all().exclude(id=user.id)
    context = {
        'item' : item,
        "others" : others,
    }
    return render(request, 'myapp/show.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')