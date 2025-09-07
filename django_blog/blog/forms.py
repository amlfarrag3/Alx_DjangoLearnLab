from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget
from blog.models import Post , Comment

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content' , 'tag']
        widgets ={ 
            'tag': TagWidget(attrs={'placeholder': 'Add tags separated by commas', 'class': 'form-control'}),
        }
        TagWidget()
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
