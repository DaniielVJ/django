# Modulo donde definiremos todos nuestros formularios usados para esta app
from django import forms
from .models import Review, Book
from django.contrib import messages

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
    
    would_recommend = forms.BooleanField(
        label="¿Recomendarias este Libro?", required=False)

    class Meta:
        # El formulario creara su estructura de forma automatica para poder recibir y procesar datos del modelo Review
        # que reciba desde el navegador a traves de un request.
        model = Review 
        fields = ['rating', 'text'] 
        exclude = ['id', 'user', 'book', 'created_at']
        widgets = {
            "rating": forms.NumberInput(attrs={
                "class": "form-control", 
                "min-value": 1, 
                "max-value": 5,
                "placeholder": "Califica con 1 estrella a 5 estrellas"}),
            "text": forms.Textarea(attrs={"class": "form-control", "row": "4"})
        }

    # Aqui recibo primero mi nuevo parametro, luego los demas en una lista en el args y los clave valor en un diccionario que es el kwargs
    def __init__(self, request=None, *args, **kwargs):
        # pero al pasarlos a un metodo con los asteriscos se desempaquetan, entonces todos los argumentos que puse en orden para args
        # se pasaran uno por uno de forma independiente desampaquetados al constructor del padre y si los pase con clave valor
        # el kwargs los desempaquetara en la interfaz del init como parametro1=valor1 no pasara el diccionario lo que lo hace muy
        # compatible.
        super().__init__(*args, **kwargs)
        self.request = request


    # el save debe ejecutarse despues de validar el formulario, si no el cleaned_data ira vacio dentro de la instancia
    def save(self, *args, **kwargs):
        # Esta llamada del padre es simplemente para obtener la instancia con los datos del cleaned_data o ya validados
        # y maniparla aqui dentro, pero el segundo save que tiene el return al final es el que ejecutara la logica del save
        # que se quiera fuera de la clase en la view.
        review = super().save(commit=False) # no tiene sentido usar la instancia en esta logica jajaja pero ver que se puede llamar

        # Logica para nuestro campo personalizado o la que queramos para nuestra instancia o formulario antes de guardarlo.
        if self.cleaned_data.get('would_recommend'):
            messages.success(self.request, "Gracias por recomendarlo")
        # Es logico que el save del padre debemos ejecutarlo despues de nuestra logica ya que este save guarda y crea
        # el objeto del modelo, asi que antes que haga eso ejecutar la logica con nuestro campo personalizado
        return super().save(*args, **kwargs)

    

    # VALIDACIONES PERSONALIZADAS - al momento de .is_valid() cada campo se va pasando a uno de estos metodos para validarlos
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not (rating >= 1 and rating <= 5):
            raise forms.ValidationError("La calificacion debe ser entre 1 y 5 MONDONGO")
        messages.success(self.request, "Rating ingresado correctamente")
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



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'cover', 'pages', 'isbn', 'author', 'genres', 'publication_date']


    
    # Creamos metodo clean que ejecute is_valid para el campo cover que es de tipo File
    def clean_cover(self):
        file = self.cleaned_data.get('cover')
        if not file:
            return file
        
        # El size viene en bytes, entonces 2 bytes por 1024 son 2048bytes == 2KB y estos por 1024 es igual a 2MB y 1024 mas 2GB y asi.
        if file.size > 2 * 1024 * 1024:
            raise forms.ValidationError("El archivo no debe superar los 2MB")
        
        # Validar el formato de la imagen, si no se encuentra en los que solicitamos no dejar subir al servidor

        if not file.content_type in ['image/jpeg', 'image/png']:
            raise forms.ValidationError("Solo se aceptan imagenes en formato jpeg y png")
        
        return file