from typing import Any
from django import forms 
from . import models
from django.contrib.auth.models import User

class PerfilForm(forms.ModelForm):
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)

class UserForm(forms.ModelForm):

    password = forms.CharField(
        required=False,
        label = 'Senha',
        widget=forms.PasswordInput()
    )

    password2 = forms.CharField(
        required=False,
        label='Confirmação senha',
        widget=forms.PasswordInput()
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'email')

    def clean(self) -> dict[str, Any]:
        data = self.data
        cleaned:dict = self.cleaned_data
        validations_error_msgs = {}

        usuario_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')
        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        if email_db:
            email_db = email_db.email

        
        has_user = bool(self.usuario)

        if has_user:

            user = User.objects.filter(username=self.usuario.username).first()

            if usuario_db and self.usuario != usuario_db:
                validations_error_msgs['username'] = 'Usuário já existe'
                
            # Email
            if email_db != user.email:
                validations_error_msgs['email'] = 'Email já está cadastrado na base de dados.'

            if password_data or password2_data:
                if password_data != password2_data:
                    validations_error_msgs['password2'] = 'Deve ser igual ao campo de entrada de senha.'

        else:
            # Não logado
            if usuario_db:
                validations_error_msgs['username'] = 'Usuário já existe'

            if email_db:
                validations_error_msgs['email'] = 'Email já está cadastrado na base de dados.'
            
            if password_data != password2_data:
                validations_error_msgs['password2'] = 'Deve ser igual ao campo de entrada de senha.'

            if not password_data:
                validations_error_msgs['password'] = 'Esse campo é obrigatório'

        if len(password_data) < 6 and len(password_data) > 0:
                validations_error_msgs['password'] = 'Sua senha precisa de pelo menos 6 caracteres'

        if validations_error_msgs:
            raise forms.ValidationError(validations_error_msgs)

        return super().clean()