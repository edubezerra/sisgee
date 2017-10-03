from django import forms

from .validators import validate_formato


class ImportForm(forms.Form):
    file = forms.FileField(label='Arquivo', validators=[validate_formato])
