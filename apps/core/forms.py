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