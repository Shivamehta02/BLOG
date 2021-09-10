from django.forms import fields
from blog.models import comment
from django import forms

#using fields from models 
class Commentform(forms.ModelForm):
    class Meta:
        model = comment
        # we don't want user to make changes to post
        exclude = ["post"]
        labels ={
            "user_name":"Your Name",
            "user_email":"Your Email",
            "text": "your comment"
        } 