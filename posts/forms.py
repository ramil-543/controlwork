from django import forms
from posts.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "rate", "image"]

    def clean_title(self):
        data = self.cleaned_data["title"]
        if "war" in data:
            raise forms.ValidationError("this is banned word!")
        return data

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "rate", "image"]

    def clean_title(self):
        data = self.cleaned_data["title"]
        if "war" in data:
            raise forms.ValidationError("this is banned word!")
        return data