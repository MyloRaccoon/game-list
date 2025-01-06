from django import forms

from .models import *

class PublisherForm(forms.Form):
    name = forms.CharField(label="Publisher name", max_length=100)
    description = forms.CharField(max_length=5000, required=False,
        widget=forms.Textarea(
            attrs={
                "rows":"10",
                "class": "form-control"
            }
        )
    )
    image = forms.ImageField(required=False)

    def fill(self, pk):
        publisher = Publisher.objects.get(pk=pk)
        self.initial['name'] = publisher.name
        self.initial['description'] = publisher.description

class PlatformForm(forms.Form):
    name = forms.CharField(label="Platform name", max_length=100)
    release_date = forms.IntegerField(required=False)
    owner = forms.ModelChoiceField(queryset=Publisher.objects.all() , label="Owner", required=False)
    description = forms.CharField(max_length=5000, required=False,
        widget=forms.Textarea(
            attrs={
                "rows":"10",
                "class": "form-control"
            }
        )
    )
    image = forms.ImageField(required=False)

    def fill(self, pk):
        platform = Platform.objects.get(pk=pk)
        self.initial['name'] = platform.name
        self.initial['release_date'] = platform.release_date
        self.initial['owner'] = platform.owner
        self.initial['description'] = platform.description

class GameForm(forms.Form):
    title = forms.CharField(label="Title", max_length=200)
    genre = forms.CharField(label="Genre", max_length=200, required=False)
    publisher = forms.ModelChoiceField(queryset=Publisher.objects.all(), label="Publisher", required=False)
    platform = forms.ModelChoiceField(queryset=Platform.objects.all(), label="Platform", required=False)
    release_date = forms.IntegerField(required=False)
    description = forms.CharField(max_length=5000, required=False,
        widget=forms.Textarea(
            attrs={
                "rows":"10",
                "class": "form-control"
            }
        )
    )
    image = forms.ImageField(required=False)

    def fill(self, pk):
        game = Game.objects.get(pk=pk)
        self.initial['title'] = game.title
        self.initial['genre'] = game.genre
        self.initial['publisher'] = game.publisher
        self.initial['platform'] = game.platform
        self.initial['release_date'] = game.release_date
        self.initial['description'] = game.description


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
            }
        ))
    email = forms.EmailField(max_length=254, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
            }
        ))
    password = forms.CharField(max_length=32, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
            }
        )) 

class GameListForm(forms.ModelForm):
    class Meta:
        model = GameList
        fields = ['state']  
        widgets = {
            'state': forms.Select(attrs={'class': 'form-control'})
        }