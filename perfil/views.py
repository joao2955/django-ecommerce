from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from . import models, forms
from django.contrib.auth.models import User
import copy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super_setup = super().setup(request, *args, **kwargs)
        
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        if request.user.is_authenticated:
            
            self.perfil = models.Perfil.objects.filter(
                usuario=self.request.user
            ).first()
            
            context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil
                )
            }
        else:
            context = {
                'userform': forms.UserForm(
                    data = request.POST or None,
                ),
                'perfilform': forms.PerfilForm(
                    data = self.request.POST or None,
                )
            }

        self.userform:forms.UserForm = context['userform']
        self.perfilform: forms.PerfilForm = context['perfilform']

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        self.renderizar = render(request, self.template_name, context)

        return super_setup
    
    def get(self, *args, **kwargs):
        return self.renderizar

class Criar(BasePerfil):
    def post(self, request, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid() :
            messages.error(
                self.request,
                'Existem erros no formulário de cadastro. Verifique se todos '
                'os campos foram preenchidos corretamente'
            )
            return self.renderizar
        
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)

            if password:
                usuario.set_password(password)

            usuario.username = username
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.email = email

            usuario.save()

            if not self.perfil:
                perfil:models.Perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()
            else:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

        else:
            usuario:models.User = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil:models.Perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

            messages.success(
            self.request,
            'Seu cadastro foi criado ou atualizado com sucesso.'
        )

        if password:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=password
                )
            
            if autentica:
                login(self.request, user=usuario)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        messages.success(
            self.request,
            'Você fez login e pode concluir sua compra.'
        )

        return redirect('perfil:criar')

class Login(View):
    def post(self, request, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(self.request,
                       'Senha ou nome de usuário inválidos.')
            return redirect('perfil:criar')

        autentica = authenticate(self.request,
                                username=username,
                                password=password)
        
        if not autentica:
            messages.error(self.request,
                        'Senha ou nome de usuário inválidos.')
            return redirect('perfil:criar')

        user = User.objects.filter(username=username).first()
        login(request, user)
        messages.success(
            self.request,
            'Você fez login no sistema e pode concluir sua compra.'
        )
        return redirect('produto:carrinho')

class Logout(View):
    def get(self, request, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho'))

        logout(request)

        self.request.session['carrinho'] = carrinho

        self.request.session.save()

        return redirect('produto:lista')
