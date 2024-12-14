from django.contrib import admin
from .models import *

# Personalización para Receta en el panel de administración
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'categoria', 'valoracion_promedio')
    search_fields = ('titulo', 'descripcion')
    list_filter = ('categoria', 'dificultad')

# Personalización para Comentario en el panel de administración
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('receta', 'usuario', 'fecha')
    search_fields = ('texto',)

# Registro básico o personalizado de modelos
admin.site.register(Categoria)
admin.site.register(Receta, RecetaAdmin)  # Usando RecetaAdmin
admin.site.register(Ingrediente)
admin.site.register(RecetaIngrediente)
admin.site.register(Carrito)
admin.site.register(CarritoIngrediente)
admin.site.register(Registro)
admin.site.register(Valoracion)
admin.site.register(Comentario, ComentarioAdmin)  # Usando ComentarioAdmin
admin.site.register(RecetaFavorita)
admin.site.register(Notificacion)