from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from apps.core.models import Registro, Receta
from apps.core.views import HistorialCocinadosView
from datetime import date

class RegistroModelTest(TestCase):
    def setUp(self):
        """Configuración previa a los tests"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.receta = Receta.objects.create(
            titulo='Receta Test',
            descripcion='Descripción de prueba',
            tiempo_coccion=30,
            dificultad=2,
            usuario=self.user
        )
        self.registro = Registro.objects.create(
            usuario=self.user,
            receta=self.receta,
            fecha=date.today(),
            notas='Notas de prueba'
        )

    def test_registro_str(self):
        """Prueba que el método __str__ del modelo Registro funcione correctamente"""
        self.assertEqual(
            str(self.registro),
            f"{self.receta.titulo} cocinada por {self.user.username} el {self.registro.fecha}"
        )

class HistorialCocinadosViewTest(TestCase):
    def setUp(self):
        """Configuración previa"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.receta = Receta.objects.create(
            titulo='Receta Test',
            descripcion='Descripción de prueba',
            tiempo_coccion=30,
            dificultad=2,
            usuario=self.user
        )
        Registro.objects.create(
            usuario=self.user,
            receta=self.receta,
            fecha=date.today(),
            notas='Notas de prueba'
        )

    def test_historial_cocinados_view(self):
        """Prueba que la vista de historial de cocinados funcione correctamente"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('historial_cocinados'))

        # Verifica que la vista se carga correctamente
        self.assertEqual(response.status_code, 200)

        # Verifica que se renderiza el template correcto (ruta corregida)
        self.assertTemplateUsed(response, 'historial/historial_cocinados.html')

        # Verifica que el contenido esperado está presente
        self.assertContains(response, 'Receta Test')
        self.assertContains(response, 'Notas de prueba')


class UrlsTest(SimpleTestCase):
    def test_historial_cocinados_url(self):
        """Prueba que la URL de historial de cocinados resuelve correctamente"""
        url = reverse('historial_cocinados')
        self.assertEqual(resolve(url).func.view_class, HistorialCocinadosView)

class ListaRecetasViewTest(TestCase):
    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.receta1 = Receta.objects.create(
            titulo='Receta 1',
            descripcion='Descripción de la receta 1',
            tiempo_coccion=15,
            dificultad=2,
            usuario=self.user
        )
        self.receta2 = Receta.objects.create(
            titulo='Receta 2',
            descripcion='Descripción de la receta 2',
            tiempo_coccion=25,
            dificultad=3,
            usuario=self.user
        )

    def test_lista_recetas_view(self):
        """Prueba que la vista de lista de recetas funcione correctamente"""
        response = self.client.get(reverse('lista_recetas'))

        # Verifica que el código de respuesta sea 200
        self.assertEqual(response.status_code, 200)

        # Verifica que el template utilizado sea el correcto
        self.assertTemplateUsed(response, 'recetas/lista_recetas.html')

        # Verifica que las recetas creadas están en el contexto
        self.assertContains(response, 'Receta 1')
        self.assertContains(response, 'Receta 2')

class RecetaModelTest(TestCase):
    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.receta = Receta.objects.create(
            titulo='Receta Test',
            descripcion='Descripción de prueba',
            tiempo_coccion=30,
            dificultad=4,
            usuario=self.user
        )

    def test_receta_creation(self):
        """Prueba que el modelo Receta se cree correctamente"""
        self.assertEqual(self.receta.titulo, 'Receta Test')
        self.assertEqual(self.receta.descripcion, 'Descripción de prueba')
        self.assertEqual(self.receta.tiempo_coccion, 30)
        self.assertEqual(self.receta.dificultad, 4)
        self.assertEqual(self.receta.usuario, self.user)

    def test_receta_str(self):
        """Prueba el método __str__ del modelo Receta"""
        self.assertEqual(str(self.receta), 'Receta Test')
