from django import forms

class Follow(forms.Form):
    btn = forms.CharField()

class Unfollow(forms.Form):
    btn = forms.CharField()



