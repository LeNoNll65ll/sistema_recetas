from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, View, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
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
    template_name = 'login.html'
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
        return render(request, 'register.html', {"form": UserCreationForm()})

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
    template_name = 'agregar_receta.html'
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
    template_name = 'lista_recetas.html'
    context_object_name = 'recetas'
    paginate_by = 3  # Número de recetas por página

    def get_queryset(self):
        # Ordena las recetas de más recientes a más antiguas
        return Receta.objects.all().order_by('-id')


# Vista para los detalles de una receta
class DetalleRecetaView(DetailView):
    # Muestra los detalles de una receta específica
    model = Receta
    print(model)
    template_name = 'detalle_receta.html'
    context_object_name = 'receta'

    def get_context_data(self, **kwargs):
        # Incluye los ingredientes de la receta en el contexto
        context = super().get_context_data(**kwargs)
        context['ingredientes'] = self.object.ingredientes.all()
        return context


# Vista para editar recetas
class EditarRecetaView(UpdateView):
    # Renderiza un formulario para editar recetas
    model = Receta
    fields = ['titulo', 'descripcion', 'categoria', 'tiempo_coccion', 'dificultad', 'imagen']
    template_name = 'editar_receta.html'

    def get_success_url(self):
        # Redirige al detalle de la receta después de editar
        return reverse_lazy('detalle_receta', kwargs={'pk': self.object.id})


# Vista para eliminar recetas
class EliminarRecetaView(DeleteView):
    # Renderiza una página para confirmar la eliminación de recetas
    model = Receta
    template_name = 'eliminar_receta.html'
    success_url = reverse_lazy('lista_recetas')  # Redirige a la lista de recetas después de eliminar


# ============================
# GESTIÓN DE INGREDIENTES
# ============================

# Vista para agregar ingredientes a una receta
class AgregarIngredienteView(LoginRequiredMixin, CreateView):
    # Renderiza un formulario para agregar ingredientes
    model = RecetaIngrediente
    form_class = IngredienteRecetaForm
    template_name = 'agregar_ingredientes.html'

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
    template_name = 'confirmar_eliminar_ingrediente.html'

    def get_object(self, queryset=None):
        # Verifica si el usuario tiene permiso para eliminar el ingrediente
        ingrediente = super().get_object(queryset)
        if ingrediente.receta.usuario != self.request.user:
            raise HttpResponseForbidden("No tienes permiso para eliminar este ingrediente.")
        return ingrediente

    def get_success_url(self):
        # Redirige al detalle de la receta después de eliminar el ingrediente
        return reverse('detalle_receta', kwargs={'pk': self.object.receta.id})