from django import forms
from .models import photos

class PictureForm(forms.ModelForm):
    class Meta:
        model=photos
        fields='__all__'