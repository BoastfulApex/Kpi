from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers, generics, status


class CheckRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    type = serializers.ChoiceField(choices=['check_in', 'check_out'])
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class SimpleCheckAPIView(APIView):
    def post(self, request):
        serializer = CheckRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Validated data
            data = serializer.validated_data

            # Bu yerda siz log qilishingiz, print qilishingiz, 3rd party API'ga uzatishingiz mumkin
            print("Received check-in/out data:", data)

            return Response({"message": "Data received", "data": data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
