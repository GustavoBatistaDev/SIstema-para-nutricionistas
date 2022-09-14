
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from nutrilab.settings import BASE_DIR
from .utils import password_is_valid, email_html
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages, auth
from django.contrib.messages import constants
from hashlib import sha256
from pathlib import Path
from .models import Ativacao


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        return render(request, 'cadastro.html')

    elif request.method == 'POST':
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not password_is_valid(request, senha, confirmar_senha):
            return redirect('cadastro')

        
        query = Q(
            Q(email=email)|Q(username=usuario)
               )
        user_verification= User.objects.filter(query)



        try:

            if not len(user_verification) > 0:

                user = User.objects.create_user(username=usuario,
                                                email=email,
                                                password=senha,
                                                is_active=False)
                user.save()

                messages.add_message(request, constants.SUCCESS, 'Usuario cadastrado com sucesso. Verifique seu email para ativar a conta.')

                token = sha256(f'{usuario}{email}'.encode()).hexdigest()
                path_template = Path(BASE_DIR, 'templates/emails/email.html')

                ativacao = Ativacao(token=token, user=user)
                ativacao.save()

                email_html(path_template, 'Email cadastrado com sucesso', [email], link_ativacao=f'http://127.0.0.1:8000/auth/ativar_conta/{token}', nome=usuario)

                
                return redirect('/auth/login')

            else:
                messages.add_message(request, constants.ERROR, 'Usuario ja cadastrado.')
                return redirect('/auth/cadastro')
                
          
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema. Tente novamente.')
            return redirect('/auth/cadastro')
        
        

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        return render(request, 'login.html')

    else:
        if request.method == 'POST':
            usuario = request.POST.get('usuario')
            senha = request.POST.get('senha')
            usuario = auth.authenticate(username=usuario, password=senha)
            
            if not usuario:
                messages.add_message(request, constants.ERROR, 'Usuario ou senha invalidos.')
                return redirect('login')
            
            else:
                if usuario:
                    auth.login(request, usuario)
                    return redirect('/pacientes/')
                   

def sair(request):
    auth.logout(request)
    return redirect('login')


def ativar_conta(request, token):
    if request.method == 'GET':
        user = get_object_or_404(Ativacao, token=token)
        if user.ativo:
            messages.add_message(request, constants.ERROR, 'A conta ja se encontra ativa.')
            return redirect('/auth/login')
        usuario = User.objects.get(username=user)
        
        user.ativo = True
        user.save() 
        usuario.is_active = True
        usuario.save()
        messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso. Faca login.')
        return redirect('/auth/login') 

