from rest_framework import serializers
from django.contrib.auth.models import User
from omok_backend_rest.models import *

def is_row(pane, i, j, diri, dirj):
    N = len(pane)
    for s in range(0, 5):
        ii = i + diri * s
        jj = j + dirj * s
        if ii < 0 or N <= ii:
            return False
        elif jj < 0 or N <= jj:
            return False
        if pane[i][j] != pane[ii][jj]:
            return False
    return True

def get_win(pane):
    N = len(pane)
    for i in range(0, N):
        for j in range(0, N):
            if pane[i][j] == 0:
                continue
            for (diri, dirj) in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                if is_row(pane, i, j, diri, dirj):
                    return pane[i][j]
    return 0

class PlayerSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        l1 = ([ obj.player1.id ] if obj.player1 else [])
        l2 = ([ obj.player2.id ] if obj.player2 else [])
        return l1 + l2

    class Meta:
        model = Room

class RoomSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        pane = []
        N = 19
        for i in range(0, N):
            pane.append([0] * N)
        hs = History.objects.filter(room = obj.id)
        for ht in hs:
            pane[ht.place_i][ht.place_j] = (1 if ht.player == obj.player1 else 2)
        return {
            "id":obj.id,
            "player1":(None if obj.player1 == None else obj.player1.id),
            "player2":(None if obj.player2 == None else obj.player2.id),
            "turn":(1 if len(hs) % 2 == 0 else 2),
            "win":get_win(pane),
            "pane":pane
        }
    def to_internal_value(self, data):
        return {}
    def create(self, data):
        return Room.objects.create()

    class Meta:
        model = Room
        fields = ('id', 'player1', 'player2', 'turn', 'win', 'pane')

class HistorySerializer(serializers.ModelSerializer):
    player = serializers.ReadOnlyField(source='player.id')
    room = serializers.ReadOnlyField(source='room.id')
    class Meta:
        model = History
        fields = ('player', 'room', 'place_i', 'place_j')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
