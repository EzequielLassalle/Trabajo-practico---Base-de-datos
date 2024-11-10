from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .modelo import Datos
from django.views.decorators.http import require_http_methods
import json


#GET DE TODOS
@require_http_methods(["GET"])
def obtener_datos(request):
    dato = Datos.objects.all()
    lista_Datos = list(dato.values())  
    return JsonResponse(lista_Datos, safe=False)

#GET INDIVIDUAL
@require_http_methods(["GET"])
def obtener_producto(request, pk):
        dato = Datos.objects.get(pk=pk)
        return JsonResponse({'nombre': dato.nombre, 'descripcion': dato.descripcion, 'valor': str(dato.valor)})


#POST 
@csrf_exempt  
@require_http_methods(["POST"])
def crear_producto(request):
    try:
        data = json.loads(request.body)  
        dato = Datos.objects.create(
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            valor=data['valor']
        )
        return JsonResponse({'nombre': dato.nombre, 'descripcion': dato.descripcion, 'valor': str(dato.valor)}, status=201)
    except KeyError:
        return JsonResponse({'error': 'Faltan datos'}, status=400)


@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_producto(request, pk):
    try:
        data = json.loads(request.body)
        producto = Producto.objects.get(pk=pk)
        producto.nombre = data['nombre']
        producto.descripcion = data['descripcion']
        producto.precio = data['precio']
        producto.save()  
        return JsonResponse({'id': producto.id, 'nombre': producto.nombre, 'descripcion': producto.descripcion, 'precio': str(producto.precio)})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except KeyError:
        return JsonResponse({'error': 'Faltan datos'}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_producto(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
        producto.delete()
        return JsonResponse({'message': 'Producto eliminado correctamente'})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)