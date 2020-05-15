from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ShopUser
from shop.models import Shop
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=32, help_text='Required')

    class Meta:
        model = ShopUser
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign up'))


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=32, help_text='Required')
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Log in'))


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(max_length=32)
    shops = forms.ModelMultipleChoiceField(queryset=Shop.objects.all(),
                                           widget=forms.CheckboxSelectMultiple,
                                           required=False, label="Shops owned by user")
    is_admin = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save changes'))

    class Meta:
        model = ShopUser
        fields = ('email', 'shops', 'is_admin')

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)

        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.shops.set(self.cleaned_data['shops'])

        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()

        return instance