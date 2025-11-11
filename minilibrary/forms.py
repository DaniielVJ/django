# Modulo donde definiremos todos nuestros formularios usados para esta app
from django import forms
from .models import Review

# Una clase que hereda de Form representa a un formulario
class ReviewSimpleForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5, 
                                widget=forms.NumberInput(attrs={
                                    'placeholder': 'Califica del 1 al 5',
                                    'class': 'form-control'
                                }), label="Ingresa el rating")
    
    text = forms.CharField(max_length=500, 
                           widget=forms.Textarea(attrs={
                               'placeholder': "Escribe tu rezeña del libro",
                               'class': 'form-control',
                               'rows': 4
                           }))



BAD_WORDS = ('hijo de puta', 'conchetumare', 'aweonao', 'hijo de la marrana', 'enfermo culiao', 'weon', 'culiao')


class ReviewModelForm(forms.ModelForm):
    
    class Meta:
        # El formulario creara su estructura de forma automatica para poder recibir y procesar datos del modelo Review
        # que reciba desde el navegador a traves de un request.
        model = Review 
        fields = ['rating', 'text'] 
        exclude = ['id', 'user', 'book', 'created_at']
        widgets = {
            "rating": forms.NumberInput(attrs={"class": "form-control", "min-value": 1, "max-value": 5}),
            "text": forms.Textarea(attrs={"class": "form-control"})
        }
        
    # VALIDACIONES PERSONALIZADAS - al momento de .is_valid() cada campo se va pasando a uno de estos metodos para validarlos
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not (rating >= 1 and rating <= 5):
            raise forms.ValidationError("La calificacion debe ser entre 1 y 5 MONDONGO")
        return rating


    def clean_text(self):
        text = self.cleaned_data.get('text')

        for badword in BAD_WORDS:
            if badword in text.lower():
                raise forms.ValidationError(f"No puedes ingresar esa mala palabra -> <b>{badword}</b>")
        return text
        

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')
        text = cleaned_data.get('text')
        # si vienen vacios no vale la pena validar, pq significa que un clean ya los valido
        # y ya hubo un valor invalido, por ende el formulario esta incorrecto para procesar los datos.
        if rating and text:
            if rating == 1 and len(text) < 10:
                raise forms.ValidationError("Si la calificacion es de una estrella estas obligado a dejar una reseña")





