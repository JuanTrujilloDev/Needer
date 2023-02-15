from django import forms
from .models import Thread
from users.models import User

class ThreadForm (forms.ModelForm):

    second_person = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder':'Digita con quien quieres hablar'}))
    class Meta:
        model = Thread
        fields = ['second_person']

    def clean_second_person(self):
        second_person = self.cleaned_data['second_person']

        try:
            second_person = User.objects.get(username = second_person)
        except:
            raise forms.ValidationError('El usuario no se encuentra en la lista')
        
        return second_person
