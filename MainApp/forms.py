from django.db.models import Model
from django.forms import ModelForm, TextInput, Textarea
from MainApp.models import Snippet, Comment
from django.contrib.auth.models import User
from django.forms import CharField, PasswordInput
from django.core.exceptions import ValidationError

class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        # Описываем поля, которые будем заполнять в форме
        fields = ['name', 'lang', 'code', 'is_public']
        labels = {'name':'', 'lang':'', 'code':'', 'is_public':'Public/Private'}
        widgets = {
            'name': TextInput(attrs={
                "class": "form-control",
                "style": "max-width: 300px",
                "placeholder": "Название сниппета"}),
            'code': Textarea(attrs={
                'placeholder': "Код сниппета",
                'rows': 5,
                'class': 'input-large',
                'style': 'width: 50% !important; resize: vertical !important;'
            }),
        }

    def clean_name(self):
        snippet_name = self.cleaned_data.get("name")
        if snippet_name is not None and len(snippet_name) > 3:
            return snippet_name
        raise ValidationError("Snippets name too short")

class UserRegistrationForm(ModelForm):
   class Meta:
       model = User
       fields = ["username", "email"]
   password1 = CharField(label="password", widget=PasswordInput)
   password2 = CharField(label="password confirm", widget=PasswordInput)

   def clean_password2(self):
       pass1 = self.cleaned_data.get("password1")
       pass2 = self.cleaned_data.get("password2")
       if pass1 and pass2 and pass1 == pass2:
           return pass2
       raise ValidationError("Пароли не совпадают или пустые")

   def save(self, commit=True):
       user = super().save(commit=False)
       user.set_password(self.cleaned_data["password1"])
       if commit:
           user.save()
       return user

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {'text': ''}

