from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Productos, Comentarios
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import threading

# Create your views here.

def home(request):
    return render(request, 'index.html')

def about(request):
    #print(request.user.get_full_name)
    return render(request, 'about.html')


def signup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form':UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                print(request.POST)
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], 
                email=request.POST['email'])
                user.save()
                user2 = authenticate(request, username=request.POST['username'], password=request.POST['password1'])

                if user2 is not None:
                    thread = threading.Thread(target=send_welcome_mail, 
                    args=(user2,))
                    thread.start()
                    login(request, user2)
                    
                    return redirect('home')
            except:
                return render(request, 'signup.html', {
                    'error':'El usuario ya existe' 
                    })
        else:
            return render(request, 'signup.html', {
                    'error':'Las contraseñas no coinciden' 
                    })

def signout(request):
    logout(request)
    return redirect('home')

def send_welcome_mail(user):
    email = create_mail(
        user.email,
        'Bienvenido a la plataforma 🥳',
        'layouts/mail.html',
        {
            'user': user
        }
    )

    email.send(fail_silently=False)

def create_mail(user_mail, subject, template_name, context):
    template = get_template(template_name)
    content = template.render(context)
    user = user_mail

    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email='car22180@gmail.com',
        to=[
            user_mail
        ],
        cc=[]
    )

    message.attach_alternative(content, 'text/html')
    return message

def products(request):

    products = Productos.objects.all()

    return render(request, 'products.html',{
        'products': products
    }
    )

def product(request, id):

    product = Productos.objects.get(id=id)
    comentarios = Comentarios.objects.filter(product = id)

    if request.method == 'GET':
        return render(request, 'product.html',{
            'product': product,
            'comments':comentarios
        })
    else:
        comentario = Comentarios.objects.create(comment=request.POST['comment'], product=Productos.objects.get(id=id), date=datetime.now(),
        author=request.user.username)

        print(request.user)
        comentario.save()

        return render(request, 'product.html',{
            'product': product,
            'comments':comentarios
        })

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form':AuthenticationForm
        })
    else:
        print(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form':AuthenticationForm,
                'error':'Usuario o Contraseña incorrecto'
            })
        else:
            login(request, user)
            return redirect('home')
        
    
