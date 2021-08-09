from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import viewsets

from django.http import JsonResponse
from django.db import transaction

from . import serializers
from . import models
from src.main import MainManager


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializer
    queryset = models.User.objects.all()

    def list(self, request, *args, **kwargs):
        raise serializers.exceptions.PermissionDenied()

    def retrieve(self, request, *args, **kwargs):
        authorization = request.query_params.get("authorization", None)
        if not authorization:
            raise serializers.exceptions.AuthenticationFailed()
        user = models.User.objects.filter(authorization=authorization).first()
        if not user:
            raise serializers.exceptions.NotAuthenticated()

        return JsonResponse(user.get_data())

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        instance = super().create(request)
        return JsonResponse(models.User.objects.get(id=instance.data['id']).get_data(), status=201)


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return JsonResponse(
            models.User.objects.get(id=serializer.validated_data['id']).get_data()
        )


class FileManagerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FileManagerSerializer
    queryset = models.FileManager.objects.all()

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        instance = super().create(request)
        result = MainManager(instance.data['video'].split('/')[-1]).get_text_from_video()

        return JsonResponse({'data': result})
