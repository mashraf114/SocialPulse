from rest_framework import serializers

class VideoSerializer(serializers.Serializer):
    video = serializers.FileField(allow_empty_file=False)
    title = serializers.CharField()
    description = serializers.CharField()
    privacy = serializers.ChoiceField(["private", "public", "listed"])
    category = serializers.CharField()