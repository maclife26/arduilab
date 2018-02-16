from django import forms
 
class UploadForm(forms.Form):
 filename = forms.CharField(max_length=100)
 docfile = forms.FileField(
        label='Selecciona un archivo'
    )