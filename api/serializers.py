from rest_framework import serializers

from api.models import Image, ExpirableLink, Thumbnail, ThumbnailSize


class ImageSerializer(serializers.ModelSerializer):
    uploader = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Image
        fields = '__all__'


class ExpirableLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpirableLink
        fields = '__all__'

    def validate_image(self, image):
        if self.context['request'].user != image.uploader:
            raise serializers.ValidationError('image does not balong this user')
        return image


class ThumnailSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThumbnailSize
        fields = '__all__'


class ThumbnailSerializer(serializers.ModelSerializer):
    thumbnail_size = ThumnailSizeSerializer(read_only=True)

    class Meta:
        model = Thumbnail
        exclude = ['original_image']
