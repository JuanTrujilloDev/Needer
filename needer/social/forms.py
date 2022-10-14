from django import forms
from .models import Comentarios, Publicacion
from tinymce import widgets as tinymce_widgets


class CrearPublicacionForm(forms.ModelForm):
    
    descripcion = forms.CharField(required=False, widget=tinymce_widgets.AdminTinyMCE(attrs={'placeholder':'Cuentale a tu publico de ti... (Maximo 280 caracteres)',}))
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
        if not 'descripcion' in cleaned_data:
            cleaned_data['descripcion'] = ''
        else:
            if len(cleaned_data['descripcion']) > 2200:
                raise forms.ValidationError('La descripcon debe tener menos de 280 caracteres')

        # Si ambos campos van vacios tirara error.
        if len(cleaned_data['descripcion']) == 0 and not cleaned_data["archivo"]:
            raise forms.ValidationError('Debes agregar una descripcion o un archivo a la publicacion.')

        return cleaned_data


class CrearComentarios(forms.ModelForm):
    comentario = forms.CharField(max_length=120, widget=forms.Textarea(attrs={'placeholder':'Escribe tu comentario','rows':1, 'cols':1}))

    class Meta:
        model = Comentarios
        fields = ['comentario']
        
    def __init__ (self, *args, **kwargs):
        super(CrearComentarios, self).__init__(*args, **kwargs)
        self.fields['comentario'].widget.attrs['class'] = 'form-control mt-3'
        self.fields['comentario'].widget.attrs['style'] = 'resize:none;'
