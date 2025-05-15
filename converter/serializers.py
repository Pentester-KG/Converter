from rest_framework import serializers

class FileConvertSerializer(serializers.Serializer):
    file = serializers.FileField()
    target_format = serializers.ChoiceField(choices=['pdf', 'jpg', 'png', 'jpeg'])

