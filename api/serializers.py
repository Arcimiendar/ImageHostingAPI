from rest_framework import serializers

from api.models import Image, ExpirableLink, Thumbnail, ThumbnailSize


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


class ImageSerializer(serializers.ModelSerializer):
    uploader = serializers.HiddenField(default=serializers.CurrentUserDefault())
    thumbnails = ThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ImageSerializer, self).to_representation(instance)
        if not instance.uploader.account_plan_assignement.account_plan.have_access_to_original_link:
            representation.pop('image_file')
        return representation
