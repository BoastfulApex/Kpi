from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers, generics, status
from rest_framework.renderers import JSONRenderer
from .models import Location


def get_distance_meters(lat1, lon1, lat2, lon2):
    from geopy.distance import geodesic
    return geodesic((lat1, lon1), (lat2, lon2)).meters


class CheckRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    type = serializers.ChoiceField(choices=['check_in', 'check_out'])
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class SimpleCheckAPIView(generics.ListCreateAPIView):
    serializer_class = CheckRequestSerializer
    renderer_classes = [JSONRenderer] 
    
    def get_queryset(self):
        return []
    
    
    def create(self, request):
        print("Keldi:", request.data)
        serializer = CheckRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            location = Location.objects.first()
            if not location:
                return Response({"status": "FAIL", "reason": "Location not set"}, status=400)

            distanse = get_distance_meters(
                lat1=data['latitude'],
                lon1=data['longitude'],
                lat2=location.latitude,
                lon2=location.longitude
            )

            print("Masofa:", distanse)

            if distanse < 100:
                data_r = {"status": "SUCCESS"}
            else:
                data_r = {"status": "FAIL"}

            return Response(data_r, status=200)

        print("Xatolik:", serializer.errors)
        return Response(serializer.errors, status=400)