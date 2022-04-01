from gc import get_objects
from django.contrib.auth import login
from django.contrib.auth.models import Group
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

# API


class RegistrarAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrarSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.groups.add(Group.objects.get_or_create(name='Todos')[0])
        return Response({
            "user": DetalleSerializer(user.detalles, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def get_post_response_data(self, request, token, instance):
        data = super().get_post_response_data(request, token, instance)
        try:
            usuario = UserDetails.objects.get(usuario=request.user)
            usuario_serializer = DetalleSerializer(usuario).data
            data['user']['detalles'] = usuario_serializer
        except UserDetails.DoesNotExist:
            print("No existe el usuario.")
        return data

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_active:
            return Response({
                "detail": 'Usuario deshabilitado. Contácte Administración'
            }, status=status.HTTP_423_LOCKED)
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class DetallesViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UsuarioDetallesSerializer

    def get_object(self):
        obj = generics.get_object_or_404(
            self.get_queryset(), usuario=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        queryset = UserDetails.objects.filter(
            usuario=self.request.user)
        return queryset

    def update(self, request, *args, **kwargs):
        request.data['usuario'] = request.user.detalles.pk
        return super().update(request, *args, **kwargs)


class ChangePasswordView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()

    def get_object(self):
        obj = generics.get_object_or_404(
            self.queryset, username=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "detail": "Su contraseña se ha actualizado exitosamente"
        })
