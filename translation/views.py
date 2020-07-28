from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .helpers import get_new_items_as_dict, map_to_source_dict, add_to_translation_dict
from . import serializers


class TranslationViewset(viewsets.ViewSet):

    serializer_class = serializers.TranslationSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                diffed_dict = get_new_items_as_dict(
                    serializer.data["translated_text"], serializer.data["original_text"]
                )
            except:
                return Response(
                    data={"message": "Files seem to be update to date"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            new_structure = map_to_source_dict(
                diffed_dict, serializer.data["original_text"]
            )
            serializer.data["translated_text"] = add_to_translation_dict(
                new_structure,
                serializer.data["translated_text"],
                serializer.data["language_code"],
            )
            return Response(
                data=serializer.data["translated_text"], status=status.HTTP_200_OK
            )
        else:
            print(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
