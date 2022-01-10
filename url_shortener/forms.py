from django import forms


class URLForm(forms.Form):
    request_body = forms.CharField(widget=forms.Textarea)
