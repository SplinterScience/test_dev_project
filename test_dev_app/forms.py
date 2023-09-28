from django import forms

class UploadJSONForm(forms.Form):
    json_file = forms.FileField()