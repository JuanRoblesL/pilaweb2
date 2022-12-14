from django.contrib import admin
from .models import Categorias, Comentarios, Productos

# Register your models here.

admin.site.register(Categorias)
admin.site.register(Comentarios)
admin.site.register(Productos)

