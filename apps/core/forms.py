from django import forms
from .models import *

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['titulo', 'descripcion', 'tiempo_coccion', 'dificultad', 'imagen', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'tiempo_coccion': forms.NumberInput(attrs={'class': 'form-control'}),
            'dificultad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }
        
class IngredienteRecetaForm(forms.ModelForm):
    class Meta:
        model = RecetaIngrediente
        fields = ['ingrediente', 'cantidad']
        
IngredienteFormSet = forms.inlineformset_factory(
    Receta,
    RecetaIngrediente,
    form=IngredienteRecetaForm,
    extra=1,
    can_delete=True
)

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre', 'unidad']

class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['estrellas', 'comentario']
        widgets = {
            'estrellas': forms.RadioSelect(choices=[(i, f"{i} estrellas") for i in range(1, 6)]),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu comentario aquí...'}),
        }