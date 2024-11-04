from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    patronymic = forms.CharField(max_length=30, required=False, label="Отчество")
    gender = forms.CharField(
        max_length=6,
        widget=forms.RadioSelect(choices=[('male', 'Мужской'), ('female', 'Женский')]),
        required=True,
        label="Пол"
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


from django import forms
from .models import DesignRequest

class RequestForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True, label="Название")
    description = forms.CharField(widget=forms.Textarea, required=True, label="Описание")
    category = forms.ChoiceField(choices=[
        ('3D', '3D дизайн'),
        ('2D', '2D дизайн'),
        ('sketch', 'Эскиз')
    ], label="Категория")
    photo = forms.ImageField(required=True, label="Фото", help_text="Максимальный размер: 2 МБ")

    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'photo']