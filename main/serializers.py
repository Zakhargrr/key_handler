from rest_framework import serializers

from main.models import Secret


class SecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = '__all__'


class DocumentationGenerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ['secret_string', 'code_phrase']


class DocumentationSecretsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ['code_phrase']


class DocumentationSuccessSecretsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ['secret_string']


class DocumentationSuccessGenerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ['secret_string']
