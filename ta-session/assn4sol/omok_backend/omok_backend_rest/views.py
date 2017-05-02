from django.shortcuts import render
from django.contrib.auth.models import User
from omok_backend_rest.models import *
from omok_backend_rest.serializers import *
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import permissions
from omok_backend_rest.permissions import RoomsPermission

@api_view(['GET', 'POST'])
def room_list(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if request.user == None or request.user.username != "omok_admin":
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = RoomSerializer(data={})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def room_detail(request, pk):
    try:
        room = Room.objects.get(pk = pk)
    except Room.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = RoomSerializer(room)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def room_players_list(request, pk):
    try:
        room = Room.objects.get(pk = pk)
    except Room.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    serializer = PlayerSerializer(room)
    if request.method == 'GET':
        return Response(serializer.data)
    elif request.method == 'POST':
        if room.player1 == None:
            room.player1 = request.user
            room.save()
        elif room.player2 == None:
            room.player2 = request.user
            room.save()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def room_history_list(request, pk):
    try:
        room = Room.objects.get(pk = pk)
    except Room.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    histories = History.objects.filter(room = room)
    if request.method == 'GET':
        serializer = HistorySerializer(histories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        u = None
        if len(histories) % 2 == 0:
            u = room.player1
        else:
            u = room.player2
        
        if request.user != u:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        
        serializer = HistorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(player=request.user, room=room)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
