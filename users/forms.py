from django import forms

from users.models import CustomerUser


class RegisterForm(forms.ModelForm):

    class Meta:
        model = CustomerUser
        fields = ('username','first_name','last_name','email','user_picture','password')


    def save(self, commit=True):
        hash = super().save(commit)
        hash.set_password(self.cleaned_data['password'])
        hash.save()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerUser
        fields = ('username','first_name','last_name','email','user_picture')


class UsersProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomerUser
        fields = ('username','is_superuser')