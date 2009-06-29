from django import forms
from django.conf import settings
from basic.media.widgets import AdminImageWidget
 
class PhotoUploadForm(forms.ModelForm):
    photo = forms.FileField(widget=AdminImageWidget, required=True)