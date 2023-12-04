from django import forms
from .models import ChampFormulaire

class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        champs = kwargs.pop('champs', [])
        super(DynamicForm, self).__init__(*args, **kwargs)

        for champ in champs:
            if champ.type_de_champ == 'texte':
                self.fields[champ.label] = forms.CharField(required=champ.obligatoire)
            elif champ.type_de_champ == 'fichier':
                self.fields[champ.label] = forms.FileField(required=champ.obligatoire)
