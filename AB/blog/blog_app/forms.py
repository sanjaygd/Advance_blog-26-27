from django import forms

from pagedown.widgets import PagedownWidget


from .models import Post




class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget) # Added in AD - 4
    publish = forms.DateField(widget=forms.SelectDateWidget) # Added in AD - 4
    class Meta:
        model = Post
        fields = [
            'title',
            'user',
            'content',
            'image',
            'draft',
            'publish',
            
        ]