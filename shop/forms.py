from django import forms
from .models import Shop, ShopUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ShopEditForm(forms.ModelForm):
    name = forms.CharField(max_length=64)
    users = forms.ModelMultipleChoiceField(queryset=ShopUser.objects.all(),
                                           widget=forms.CheckboxSelectMultiple,
                                           label="Owners")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

    class Meta:
        model = Shop
        fields = ('name', 'users')

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)

        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.users.set(self.cleaned_data['users'])

        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()

        return instance
