# Trabajo practico: Sistema de Gestión de recetas de cocina

### *Enunciado:* 

Desarrollar un sistema de gestión de recetas de cocina, donde los usuarios puedan **registrar,organizar y compartir sus recetas**. El sistema permitirá **buscar recetas por categorías y dificultad**, además de **crear listas de compras con los ingredientes necesarios**. Se deben aplicar los conceptos de Programación Orientada a Objetos (POO), persistencia de datos, pruebas (tests) y el patrón Modelo-Vista-Template (MVT) de Django.

## Requisitos generales:

- El sistema debe ser implementado en Django siguiendo las buenas prácticas de desarrollo.
- Se deben utilizar clases y conceptos de POO para organizar el código.
- La persistencia de datos se realizará a través de un sistema de base de datos relacional.
- Se deben escribir pruebas (tests) para verificar el funcionamiento correcto del sistema.
- Aplicar el patrón Modelo-Vista-Template (MVT) de Django correctamente.

### Requisitos del sistema:

1. **Registro y Organización de Recetas:**
    -  Los usuarios podrán registrar nuevas recetas con campos como *título, descripción, ingredientes, pasos de preparación, tiempo de cocción y dificultad.*
    -  Cada receta deberá tener una **categoría** (por ejemplo: desayuno, almuerzo, cena, postre).
    - Los usuarios deben poder *visualizar y editar sus propias recetas*.

2. **Categorización y Búsqueda:**
    - Los usuarios podrán *buscar recetas* usando palabras clave (título o ingrediente).
    - Además, podrán *filtrar las recetas* por categorías o nivel de dificultad.

3. **Carga de Imágenes:**
    - Los usuarios podrán *añadir imágenes* relacionadas con la receta (por ejemplo, una foto del plato terminado).
    - Las imágenes asociadas a cada receta deben ser visibles dentro del sistema.

4. **Valoración y Comentarios:**
    - Los **usuarios** tendrán la opción de *valorar recetas* mediante un sistema de *estrellas (de 1 a 5)*.
    - También podrán *dejar comentarios* en las **recetas** para *compartir sugerencias* o variaciones.

5. **Lista de Compras:**
    - Los usuarios podrán generar una *lista de compras* automática con los ingredientes necesarios para una o varias recetas seleccionadas. (Opcional, integrar con sistema para mandar la lista por mail).
    - La lista de compras se podrá marcar como comprada, vaciándose     automáticamente para futuras compras.

6. **Recetas Favoritas:**
    - Los usuarios podrán marcar sus *recetas favoritas* para tener acceso rápido a ellas.
    - Habrá una sección dedicada para que los usuarios visualicen todas sus recetas favoritas.

7. **Historial de Cocinados:**
    - El sistema llevará un **registro** de cuándo el usuario ha cocinado una receta (de forma opcional, el usuario podrá registrar esta información).
    - Los usuarios podrán *ver un historial de las recetas que han cocinado*.

8. **Estadísticas y Reportes (Opcional):**
    - Los usuarios tendrán acceso a estadísticas sobre sus recetas más cocinadas, categorías más populares, entre otros datos.
    - Será posible exportar estas estadísticas en formato CSV.

9. **Notificaciones (Opcional):**
    - Los usuarios recibirán notificaciones cuando alguien valore o comente en una de sus recetas.

10. **Autenticación y Seguridad:**
    - Los usuarios deberán iniciar sesión para acceder al sistema.
    - Las contraseñas se almacenarán en forma de hashes y deberán cumplir con ciertos requisitos de complejidad.



## Para resolver el modelado.
Usando plantuml 

**DIAGRAMA DE CLASES**

![Diagrama de clase](https://cdn-0.plantuml.com/plantuml/png/TLHBZjim3Dtx55wwYzoWYxb9m96PZ0fRCYXwCEsWH-gYw15oiTBwY4oDha8-KNoFZt9U4WFnlYx3u1P8QTpJ3kJZ-3cCOuZhAs4FhlLC01S34oHy_0R95f_uIkYG8RNK0P7dsFCRlCSdWF0kFoI087Ti3QOlakBiDS_70GceDSqOtAK3a3QUoeLIRmXpTMK3CbNlIDStGQKCbgaXc1XcGRshMZwsI0p_7lniXfL-sIz-_E9zYHBDc1pvpVd7dz06za4Kpnu3OpTXWvGTOO_h5gykkdPbzZVlzaKe9N70U3zaIknN43iEiR140kTZk6uKLsaTk_cI1WRoqhpQQJrxaZATnDdAB71IhSrTziUaKqlDzOvrqHtHcJAK1D8Xh40pmAIXCTtmFRzK1u7zd4tRGmugTwcmYsiFC3SeMvJWXkuDSaU6qzEiQQxfMQwqZUihpNtFczSfMzloyv_zJ2REp_4RkfsBHHk1vLKlCpKc9bpaH68rKHBzZ0jpcx9VwAFfjGxLovPNgp8lumUVQTJSHfVhpdsjnuK5NXCJEDRFOFpiv3Cc-Bw7M5DOrXtfHqiT1gZX5e_nXg4IZPTBqwL8MzrGJWHHpa7PlrwKrg8NGs_XAiD2JOuIwPujgZire1fkjRVtFBnWc8z_zBy0)

**DER**

![Diagrama de clase](https://cdn-0.plantuml.com/plantuml/png/fLRHZjCw47tFLrXvkHUa_i0-RLMsOWKKgUfMl5LJPrgC4ZkodGgqvQFu1duCkx56ute9WhwibEFZCyTdEgEzTnwi7xgsGksL_oRg9pU0LQOMpvKGhuLgTiE8Y3lnkDe4S3OBVxJfzXO3jfsl5s_dQuA8pe-aqTw2mvy_WE7VAwgwHeaUM55x0VAQWJgqkN23JbhLIsLqm3SFdpON7dQzsKaZ8quQZJeeERGU6e9K1qVKcU89McCXNjprrdJON9woVFznJZwMxufO29NWyMYiIjRv6n_rqGQvy8dieOfG_6F2WrODD2ydk4Y5AKHkPaAvaB5MUSD5HYINyCP3oxsxT3uHKTRketBUyZ8sGRdE0UNdwFxDVFDmSUx1KQEdkr7yYbZzBJMPEJWHc7j0vossBJY2fUc2KgftgvS5YV7G2RpA7RzwLfJ7SuE7D7vBE1chiZ4yZ53IkQN4olWuVzUXQmPVJtkVptg7si4N_9lNaul_n0RsBGYbFTeur21wi236XmiKR3Z5_wkx3w-kic7dnPRw_GoNaH3uqXq9siS9fuKpuJmDwgJrn664SgwdpHFjdzsliRqq5rtrbBfoFizcvZbb7zYrj0XrbRxvAOyz4WSNU1oR8gEBINaK3MRYvxEWPHbvFGQI3kS2wj8ZRQLQ6gbqITdojL6FIwGWqP2FIkCNTrKgMPHgdpilXBn2ZLICNaSjgtlZC10IGYB5xs9qfPCUFvYymYCke-Cx9R8xi1BYyZJYaE3Y5byJF8Ng7dKJ_q_v1G00)
