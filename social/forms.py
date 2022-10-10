from django import forms
from .models import Publicacion
from tinymce import widgets as tinymce_widgets


class CrearPublicacionForm(forms.ModelForm):
    
    descripcion = forms.CharField(max_length=280, widget=tinymce_widgets.AdminTinyMCE(attrs={'placeholder':'Cuentale a tu publico de ti... (Maximo 280 caracteres)',}))
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

        if len(cleaned_data['descripcion']) > 280:
            raise forms.ValidationError('La descripcon debe tener menos de 280 caracteres')

        # Si ambos campos van vacios tirara error.
        if len(cleaned_data['descripcion']) == 0 and not cleaned_data["archivo"]:
            raise forms.ValidationError('Debes agregar una descripcion o un archivo a la publicacion.')
        