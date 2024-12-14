from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Receta(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    tiempo_coccion = models.IntegerField()
    dificultad = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    imagen = models.ImageField(upload_to='recetas/', blank=True, null=True)
    valoracion_promedio = models.FloatField(default=0)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recetas')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='recetas')

    def __str__(self):
        return self.titulo


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=255)
    unidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class RecetaIngrediente(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='ingredientes')
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE, related_name='recetas')
    cantidad = models.FloatField()

    def __str__(self):
        return f"{self.cantidad} {self.ingrediente.unidad} de {self.ingrediente.nombre} en {self.receta.titulo}"


class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrito')

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class CarritoIngrediente(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='ingredientes')
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE, related_name='carritos')
    cantidad = models.FloatField()

    def __str__(self):
        return f"{self.cantidad} {self.ingrediente.unidad} de {self.ingrediente.nombre}"


class Registro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registros')
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='registros')
    fecha = models.DateField()
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.receta.titulo} cocinada por {self.usuario.username} el {self.fecha}"


class Valoracion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='valoraciones')
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='valoraciones')
    estrellas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Valoración de {self.estrellas} estrellas para {self.receta.titulo} por {self.usuario.username}"


class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.receta.titulo}"


class RecetaFavorita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='favoritos')

    def __str__(self):
        return f"{self.receta.titulo} es favorita de {self.usuario.username}"


class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=50)
    mensaje = models.TextField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.usuario.username}: {self.tipo}"