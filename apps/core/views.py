from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Avg
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, View, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView, FormMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .forms import *
from .models import *

# ============================
# VISTAS GENERALES Y ESTÁTICAS
# ============================

# Vista de inicio
class IndexView(TemplateView):
    # Renderiza la página principal estática
    template_name = 'index.html'

# Vista de ejemplo "Hola Mundo"
class HolaMundoView(TemplateView):
    # Renderiza una página de prueba
    template_name = 'holamundo.html'


# ============================
# GESTIÓN DE USUARIOS
# ============================

# Vista para ingresar (login)
class IngresarView(LoginView):
    # Renderiza el formulario de inicio de sesión
    template_name = 'registro/login.html'
    redirect_authenticated_user = True  # Redirige si ya está autenticado
    next_page = '/'  # Redirige al inicio después del login

    def form_valid(self, form):
        # Si el login es válido, muestra un mensaje de bienvenida
        messages.success(self.request, f"¡Bienvenido, {form.get_user().username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Si el login falla, muestra un mensaje de error
        messages.error(self.request, "Usuario o contraseña incorrectos.")
        return super().form_invalid(form)


# Vista para salir (logout)
class SalirView(LoginRequiredMixin, LogoutView):
    next_page = '/'  # Redirige al inicio después del logout

    def dispatch(self, request, *args, **kwargs):
        # Cierra la sesión y muestra un mensaje de despedida
        logout(request)
        messages.success(request, "Has cerrado sesión correctamente.")
        return HttpResponseRedirect('/')


# Vista para registrarse
class RegistrarseView(View):
    def get(self, request):
        # Renderiza el formulario de registro
        return render(request, 'registro/register.html', {"form": UserCreationForm()})

    def post(self, request):
        # Procesa el registro de un nuevo usuario
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # Crea un nuevo usuario
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"]
                )
                user.save()
                login(request, user)  # Inicia sesión automáticamente
                messages.success(self.request, f"¡Bienvenido, {user.username}!")
                return redirect('home')
            except IntegrityError:
                # Maneja usuarios duplicados
                messages.error(self.request, "El nombre de usuario ya existe.")
        else:
            # Maneja contraseñas que no coinciden
            messages.error(self.request, "Las contraseñas no coinciden.")
        return render(request, 'register.html', {"form": UserCreationForm()})


# ============================
# GESTIÓN DE RECETAS
# ============================

# Vista para agregar recetas
class AgregarRecetaView(LoginRequiredMixin, CreateView):
    # Renderiza un formulario para agregar recetas
    template_name = 'recetas/agregar_receta.html'
    form_class = RecetaForm

    def form_valid(self, form):
        # Asocia la receta al usuario actual antes de guardarla
        receta = form.save(commit=False)
        receta.usuario = self.request.user
        receta.save()
        messages.success(self.request, "Receta agregada con éxito.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Muestra un mensaje de error si la receta no es válida
        messages.error(self.request, "Hubo un error al agregar la receta.")
        return super().form_invalid(form)

    def get_success_url(self):
        # Redirige a la vista para agregar ingredientes
        return reverse('agregar_ingrediente', kwargs={'receta_id': self.object.id})


# Vista para listar recetas
class ListaRecetasView(ListView):
    # Muestra todas las recetas en una lista paginada
    model = Receta
    template_name = 'recetas/lista_recetas.html'
    context_object_name = 'recetas'
    paginate_by = 3  # Número de recetas por página

    def get_queryset(self):
        # Ordena las recetas de más recientes a más antiguas
        return Receta.objects.all().order_by('-id')


# Vista para los detalles de una receta
class DetalleRecetaView(FormMixin, DetailView):
    model = Receta
    template_name = 'recetas/detalle_receta.html'
    context_object_name = 'receta'
    form_class = ValoracionForm  # Formulario para valoraciones
    comentario_form = ComentarioForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['valoraciones'] = self.object.valoraciones.all()
        context['promedio_valoraciones'] = self.object.valoraciones.aggregate(promedio=Avg('estrellas'))['promedio'] or 0
        context['form'] = self.get_form()
        context['comentarios'] = self.object.comentarios.all()  # Traer todos los comentarios de la receta
        context['comentario_form'] = ComentarioForm()  # Formulario para nuevos comentarios
        context['ingredientes'] = self.object.ingredientes.all()  # Traer todos los ingredientes relacionados
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        # Manejar valoraciones
        if 'estrellas' in request.POST:
            form = self.get_form()
            if form.is_valid():
                # Intentar obtener o crear la valoración
                valoracion, creada = Valoracion.objects.get_or_create(
                    usuario=request.user,
                    receta=self.object,
                    defaults={
                        'estrellas': form.cleaned_data['estrellas'],
                        'comentario': form.cleaned_data['comentario']
                    }
                )
                if not creada:
                    # Si ya existía, actualizar los campos
                    valoracion.estrellas = form.cleaned_data['estrellas']
                    valoracion.comentario = form.cleaned_data['comentario']
                    valoracion.save()

                # Actualizar el promedio de valoraciones
                self.object.valoracion_promedio = self.object.valoraciones.aggregate(promedio=Avg('estrellas'))['promedio'] or 0
                self.object.save()

                return self.form_valid(form)
            else:
                return self.form_invalid(form)

        # Manejar comentarios
        elif 'comentario' in request.POST:
            comentario_form = ComentarioForm(request.POST)
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.usuario = request.user
                comentario.receta = self.object
                comentario.save()
                return redirect(self.get_success_url())

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('recetas/detalle_receta', kwargs={'pk': self.object.pk})



# Vista para editar recetas
class EditarRecetaView(UpdateView):
    # Renderiza un formulario para editar recetas
    model = Receta
    fields = ['titulo', 'descripcion', 'categoria', 'tiempo_coccion', 'dificultad', 'imagen']
    template_name = 'recetas/editar_receta.html'

    def get_success_url(self):
        # Redirige al detalle de la receta después de editar
        return reverse_lazy('detalle_receta', kwargs={'pk': self.object.id})


# Vista para eliminar recetas
class EliminarRecetaView(DeleteView):
    # Renderiza una página para confirmar la eliminación de recetas
    model = Receta
    template_name = 'recetas/eliminar_receta.html'
    success_url = reverse_lazy('lista_recetas')  # Redirige a la lista de recetas después de eliminar

# Vista de recetas por usuario
class MisRecetasView(LoginRequiredMixin, ListView):
    model = Receta
    template_name = 'recetas/mis_recetas.html'  # Template que se usará
    context_object_name = 'recetas'
    paginate_by = 3  # Mostrar solo 3 recetas por página

    def get_queryset(self):
        # Filtra las recetas que pertenecen al usuario autenticado
        return Receta.objects.filter(usuario=self.request.user).order_by('-id')


# ============================
# GESTIÓN DE INGREDIENTES
# ============================

# Vista para agregar ingredientes a una receta
class AgregarIngredienteView(LoginRequiredMixin, CreateView):
    # Renderiza un formulario para agregar ingredientes
    model = RecetaIngrediente
    form_class = IngredienteRecetaForm
    template_name = 'ingredientes/agregar_ingredientes.html'

    def get_context_data(self, **kwargs):
        # Incluye la receta en el contexto
        context = super().get_context_data(**kwargs)
        receta_id = self.kwargs['receta_id']
        context['receta'] = get_object_or_404(Receta, id=receta_id)
        return context

    def form_valid(self, form):
        # Asocia el ingrediente a la receta antes de guardarlo
        receta_id = self.kwargs['receta_id']
        receta = get_object_or_404(Receta, id=receta_id)
        ingrediente_receta = form.save(commit=False)
        ingrediente_receta.receta = receta
        ingrediente_receta.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Redirige al detalle de la receta después de agregar un ingrediente
        return reverse('detalle_receta', kwargs={'pk': self.kwargs['receta_id']})


# Vista para eliminar ingredientes
class EliminarIngredienteView(LoginRequiredMixin, DeleteView):
    # Renderiza una página para confirmar la eliminación de ingredientes
    model = RecetaIngrediente
    template_name = 'ingredientes/confirmar_eliminar_ingrediente.html'

    def get_object(self, queryset=None):
        # Verifica si el usuario tiene permiso para eliminar el ingrediente
        ingrediente = super().get_object(queryset)
        if ingrediente.receta.usuario != self.request.user:
            raise PermissionDenied("No tienes permiso para eliminar este ingrediente.")
        return ingrediente

    def get_success_url(self):
        # Redirige al detalle de la receta después de eliminar el ingrediente
        return reverse('detalle_receta', kwargs={'pk': self.object.receta.id})
    
# Vista para crear un nuevo ingrediente
class CrearIngredienteView(LoginRequiredMixin, CreateView):
    model = Ingrediente
    form_class = IngredienteForm
    template_name = 'ingredientes/crear_ingrediente.html'

    def get_success_url(self):
        receta_id = self.kwargs.get('receta_id')
        if not receta_id:  # Verificar si receta_id es válido
            raise ValueError("El receta_id no fue proporcionado correctamente a get_success_url.")
        print(f"Receta ID en get_success_url: {receta_id}")  # Depuración
        return reverse('agregar_ingrediente', kwargs={'receta_id': receta_id})
