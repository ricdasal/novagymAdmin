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

     path('producto-list/', productoList, name='producto-overview'),
     path('producto-detail/<str:id>', productoDetail, name='producto-detail'),
     path('producto-create/', productoCreate, name='producto-create'),
     path('producto-update/<str:id>', productoUpdate, name='producto-update'),
     path('producto-delete/<str:id>', productoDelete, name='producto-delete'),

     #Categoria
     
     path('categoria-list/', categoriaList, name='categoria-overview'),
     path('categoria-detail/<str:id>', categoriaDetail, name='categoria-detail'),
     path('categoria-create/', categoriaCreate, name='categoria-create'),
     path('categoria-update/<str:id>', categoriaUpdate, name='categoria-update'),
     path('categoria-delete/<str:id>', categoriaDelete, name='categoria-delete'),
     
     #Inventario
     
     path('inventario-list/', inventarioList, name='inventario-overview'),
     path('inventario-detail/<str:id>', inventarioDetail, name='inventario-detail'),
     path('inventario-create/', inventarioCreate, name='inventario-create'),
     path('inventario-update/<str:id>', inventarioUpdate, name='inventario-update'),
     path('inventario-delete/<str:id>', inventarioDelete, name='inventario-delete'),

     #Descuento
     
     path('descuento-list/', descuentoList, name='descuento-overview'),
     path('descuento-detail/<str:id>', descuentoDetail, name='descuento-detail'),
     path('descuento-create/', descuentoCreate, name='descuento-create'),
     path('descuento-update/<str:id>', descuentoUpdate, name='descuento-update'),
     path('descuento-delete/<str:id>', descuentoDelete, name='descuento-delete'),
]
