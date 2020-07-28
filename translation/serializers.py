from rest_framework import serializers


class TranslationSerializer(serializers.Serializer):
    """Translation Serializer

    The serializer responsible for managing the incoming and outgoing JSON
    data.

    This serializer will recieve JSON information with any potential structure
    so in order to accomodate this, we'll use the JSONField serializer for
    both incoming and outgoing data.
    """
    language_code = serializers.CharField(required=True)
    original_text = serializers.JSONField(required=True)
    translated_text = serializers.JSONField(required=True)