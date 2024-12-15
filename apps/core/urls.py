from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('holamundo/', HolaMundoView.as_view(), name='holamundo'),
    path('login/', IngresarView.as_view(), name='login'),
    path('logout/', SalirView.as_view(), name='logout'),
    path('register/', RegistrarseView.as_view(), name='register'),
    path('recetas/agregar/', AgregarRecetaView.as_view(), name='agregar_receta'),
    path('recetas/', ListaRecetasView.as_view(), name='lista_recetas'),
    path('recetas/<int:receta_id>/ingredientes/agregar/', AgregarIngredienteView.as_view(), name='agregar_ingrediente'),
    path('recetas/<int:receta_id>/ingredientes/crear/', CrearIngredienteView.as_view(), name='crear_ingrediente'),
    path('recetas/<int:pk>/', DetalleRecetaView.as_view(), name='detalle_receta'),
    path('recetas/<int:pk>/editar/', EditarRecetaView.as_view(), name='editar_receta'),
    path('recetas/<int:pk>/eliminar/', EliminarRecetaView.as_view(), name='eliminar_receta'),
    path('ingredientes/<int:pk>/eliminar/', EliminarIngredienteView.as_view(), name='eliminar_ingrediente'),
    path('mis-recetas/', MisRecetasView.as_view(), name='mis_recetas'),
]

# Agregar rutas para archivos estáticos y de medios
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)