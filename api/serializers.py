from rest_framework import serializers

from api.models import Image, ExpirableLink


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ExpirableLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpirableLink
        fields = '__all__'
