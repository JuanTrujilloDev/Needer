from django import forms
from .models import Publicacion



class CrearPublicacionForm(forms.ModelForm):
    

    class Meta:
        model = Publicacion
        fields = ['descripcion', 'archivo', 'nsfw']


    def __init__ (self, *args, **kwargs):

        super(CrearPublicacionForm, self).__init__(*args, **kwargs)


        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control '

        self.fields['descripcion'].widget.attrs['class'] = 'form-control'
        self.fields['archivo'].widget.attrs['class'] = 'form-control'
        self.fields['nsfw'].widget.attrs['class'] = 'form-check-input d-none'



    def clean(self):
        cleaned_data =  super().clean()

        # Si ambos campos van vacios tirara error.
        if len(cleaned_data['descripcion']) == 0 and not cleaned_data["archivo"]:
            raise forms.ValidationError('Debes agregar una descripcion o un archivo a la publicacion.')
        