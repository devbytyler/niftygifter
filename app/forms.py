from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.password_validation import validate_password
from django.urls import reverse
from django.utils.safestring import mark_safe

from app.models import User, Event, Idea

class BaseForm:
    def add_form_control_class(self, fields=None, field_names=None):
        if not fields:
            fields = self.fields
        if not field_names:
            field_names = [field for field in fields]
        for field_name in field_names:
            current_class = fields[field_name].widget.attrs.get('class') or ''
            if not isinstance(fields[field_name], forms.FileField) and not isinstance(fields[field_name].widget, forms.RadioSelect) and not isinstance(fields[field_name].widget, forms.CheckboxSelectMultiple):
                fields[field_name].widget.attrs['class'] = 'form-control' if not current_class else '{} form-control'.format(current_class)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.add_form_control_class(self.fields)


class SigninBaseForm(BaseForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'username': 'Email',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields['username'].help_text = None
        self.fields['username'].widget.attrs['class'] = 'form-control no-shadow'
        self.fields['password'].widget.attrs['class'] = 'form-control no-shadow'


class SigninForm(SigninBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control no-shadow'
        self.fields['password'].widget.attrs['class'] = 'form-control no-shadow'

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(None, username=email, password=password)

        self.cleaned_data['user'] = user
        if not user or not user.is_active:
            raise forms.ValidationError(mark_safe(f'Sorry, the email or password is invalid. Please try again.'))
        return self.cleaned_data


class SignupForm(SigninBaseForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'password',)
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'username': 'Email',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['autocomplete'] = 'new-password'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(mark_safe(f'Email address is already in use. Try <a href="{reverse("login")}">signing in</a>.'))
        return email

    def save(self, *args, **kwargs):
        user = super().save(commit=False, *args, **kwargs)
        user.set_password(self.cleaned_data['password'])
        user.username = user.email
        user.save()
        return user

class EventForm(BaseForm, forms.ModelForm):
    class Meta: 
        model = Event
        fields = ['title', 'exchange_date']

class IdeaForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'description']

class NewRecipientForm(BaseForm, forms.Form):
    email = forms.EmailField(label='Recipient Email')
    # is_anonymous = forms.BooleanField(label="Anonymous")