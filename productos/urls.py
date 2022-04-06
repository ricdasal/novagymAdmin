from django.urls import path
from .views import *
from .apps import ProductosConfig

app_name = ProductosConfig.name


urlpatterns = [
     path('categoria/create/',createCategoria,name='createCategoria'),
     path('create/',createProducto,name='createProducto'),
     path('inventario/create/',createInventario,name='createInventario'),
     path('descuento/create/',createDescuento,name='createDescuento'),

     #Producto
     path('deleteProducto/<int:id>', deleteProducto, name='deleteProducto'),
     path('UpdateProducto/<int:pk>', UpdateProducto.as_view(), name='UpdateProducto'),
     path('CrearProducto/', CrearProducto.as_view(), name='CrearProducto'),
     path('listarProductos/', ListarProductos.as_view(), name='listarProductos'),
     path('getProducts/', getAllProducts, name='getProducts'),
     #Categoria
     
     path('deleteCategoria/<int:id>', deleteCategoria, name='deleteCategoria'),
     path('listarCategoria/', ListarCategoria.as_view(), name='listarCategoria'),
     path('crearCategoria/', crearCategoria.as_view(), name='crearCategoria'),
     path('editarCategoria/<str:pk>', editarCategoria.as_view(), name='editarCategoria'),
]
