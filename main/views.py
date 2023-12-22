import secrets

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response

from main.models import Secret
from main.serializers import SecretSerializer, DocumentationSecretsSerializer, DocumentationGenerateSerializer, \
    DocumentationSuccessSecretsSerializer, DocumentationSuccessGenerateSerializer
from rest_framework.decorators import api_view
import hashlib


# Create your views here.

@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary="Create a secret",
    request_body=DocumentationGenerateSerializer,
    responses={
        400: "Bad request",
        201: openapi.Response('Created', DocumentationSuccessGenerateSerializer)
    }
))
class SecretCreateAPIView(generics.CreateAPIView):
    serializer_class = SecretSerializer

    def create(self, request, *args, **kwargs) -> Response:
        context = {
            'request': request
        }

        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        secret_key = self.perform_create(serializer)

        return Response({
            'secret_key': secret_key
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer) -> str:
        secret_key = secrets.token_urlsafe(12)

        new_secret = serializer.save()
        code_phrase = new_secret.code_phrase

        hash_secret_key = hashlib.new('md5')
        hash_code_phrase = hashlib.new('md5')

        hash_secret_key.update(secret_key.encode())
        hash_code_phrase.update(code_phrase.encode())

        new_secret.secret_key = hash_secret_key.hexdigest()
        new_secret.code_phrase = hash_code_phrase.hexdigest()

        new_secret.save()

        return secret_key


@swagger_auto_schema(
    method="POST",
    operation_summary="Get secret by code phrase",
    request_body=DocumentationSecretsSerializer,
    responses={
        404: "Not found",
        400: "Bad request",
        403: "Forbidden",
        200: openapi.Response('OK', DocumentationSuccessSecretsSerializer),
    }
)
@api_view(['POST'])
def show_secret(request, secret_key) -> Response:
    hash_secret_key = hashlib.new('md5')
    hash_secret_key.update(secret_key.encode())
    try:
        current_secret = Secret.objects.get(secret_key=hash_secret_key.hexdigest())
    except ObjectDoesNotExist:
        return Response({
            'message': 'такого секрета нет'
        }, status=status.HTTP_404_NOT_FOUND)

    else:
        try:
            code_phrase = request.data['code_phrase']
        except KeyError:
            return Response({
                'message': 'не предоставлено кодовое слово'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            hash_code_phrase = hashlib.new('md5')
            hash_code_phrase.update(code_phrase.encode())
            if current_secret.code_phrase != hash_code_phrase.hexdigest():
                return Response({
                    'message': 'неверное кодовое слово'
                }, status=status.HTTP_403_FORBIDDEN)
            else:
                if current_secret.counter == 1:
                    return Response({
                        'message': 'секрет уже просматривался'
                    }, status=status.HTTP_403_FORBIDDEN)
                else:
                    current_secret.counter += 1
                    current_secret.save()
                    return Response({
                        'secret_string': current_secret.secret_string
                    })
