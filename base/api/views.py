from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializer import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET/api',
        'GET/api/rooms',
        'GET/api/rooms/:id'
    ]


    return Response(routes)

@api_view(['GET'])
def getRoooms(request):
    rooms = Room.objects.all()
    Serializers = RoomSerializer(rooms ,many= True)
    return Response(Serializers.data)