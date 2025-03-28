from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


#
# Solicitud de información de producto
#
class ProductInfoRequest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='product_requests/', null=True, blank=True)
    
    # Usuario y proyecto asociados, si se desea llevar un registro
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

    # Estado general de la solicitud
    STATUS_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('completado', 'Completado'),
        ('error', 'Error'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


#
# Almacena los medios (imágenes, videos, GIFs) relacionados con la solicitud
#
class ProductMedia(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('imagen', 'Imagen'),
        ('video', 'Video'),
        ('gif', 'GIF'),
    )

    product_request = models.ForeignKey(
        ProductInfoRequest, related_name='medias', on_delete=models.CASCADE
    )
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='product_media/')
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.get_media_type_display()} - {self.product_request.title}"


#
# Reseñas (con calificación 1-5 estrellas); puede haber reseñas externas (is_external=True)
#
class ProductReview(models.Model):
    product_request = models.ForeignKey(
        ProductInfoRequest, related_name='reviews', on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField()  # Valor de 1 a 5
    comment = models.TextField()
    is_external = models.BooleanField(default=False)
    source = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña ({self.rating} estrellas) - {self.product_request.title}"


#
# Tareas internas (subtareas) para la lógica de AI o automatización
#
class Task(models.Model):
    """
    Modelo genérico para gestionar subtareas internas ligadas a una solicitud de información de producto
    (por ejemplo, 'buscar imágenes', 'extraer reseñas de Amazon', etc.).
    """

    title = models.CharField(max_length=200)
    description = models.TextField()
    done = models.BooleanField(default=False)

    # Relación opcional con Project y User (como metadatos)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Relación con la solicitud de información de producto; este campo es nulo en tareas anteriores
    product_request = models.ForeignKey(
        ProductInfoRequest, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"Tarea interna: {self.title} (done={self.done})"

    